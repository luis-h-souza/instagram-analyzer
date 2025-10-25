from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from services.instagram_service import InstagramService
from services.ai_service import AIService
from services.report_service import ReportService
from datetime import datetime, timedelta
from typing import Dict, Optional
import asyncio

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI(title="Instagram Analyzer API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
instagram_service = InstagramService()
ai_service = AIService()
report_service = ReportService()


# Sistema de controle de rate limiting global
class RateLimiter:
    def __init__(self, instagram_service):
        self.instagram_service = instagram_service
        self.last_requests: Dict[str, datetime] = {}
        self.request_cache: Dict[str, tuple] = {}
        self.min_interval = 10  # segundos entre requisições do mesmo perfil
        self.cache_duration = timedelta(hours=1)  # Cache de 1 hora
        self.global_blocked_until: Optional[datetime] = None

    def check_rate_limit(self, username: str) -> tuple[bool, Optional[int]]:
        """Verifica se pode fazer requisição. Retorna (pode_fazer, tempo_espera)"""

        # Verificar rate limit do InstagramService primeiro
        if self.instagram_service.rate_limit_until:
            if datetime.now() < self.instagram_service.rate_limit_until:
                wait_time = int(
                    (self.instagram_service.rate_limit_until - datetime.now()).total_seconds()
                )
                print(f"⚠️ Instagram rate limit ativo: aguarde {wait_time}s")
                return False, wait_time

        # Verificar se há bloqueio global
        if self.global_blocked_until:
            if datetime.now() < self.global_blocked_until:
                wait_time = int(
                    (self.global_blocked_until - datetime.now()).total_seconds()
                )
                return False, wait_time
            else:
                self.global_blocked_until = None

        # Verificar cache
        if username in self.request_cache:
            cached_data, timestamp = self.request_cache[username]
            if datetime.now() - timestamp < self.cache_duration:
                return True, 0  # Pode usar cache

        # Verificar rate limit por perfil
        if username in self.last_requests:
            elapsed = (datetime.now() - self.last_requests[username]).total_seconds()
            if elapsed < self.min_interval:
                wait_time = int(self.min_interval - elapsed)
                return False, wait_time

        return True, 0

    def register_request(self, username: str, data: dict = None):
        """Registra uma requisição bem-sucedida"""
        self.last_requests[username] = datetime.now()
        if data:
            self.request_cache[username] = (data, datetime.now())

    def get_cached_data(self, username: str) -> Optional[dict]:
        """Obtém dados do cache se disponível"""
        if username in self.request_cache:
            cached_data, timestamp = self.request_cache[username]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data
        return None

    def set_global_block(self, seconds: int):
        """Define um bloqueio global"""
        self.global_blocked_until = datetime.now() + timedelta(seconds=seconds)
        print(f"🔴 Bloqueio global ativado por {seconds} segundos")


# Criar rate limiter passando o instagram_service
rate_limiter = RateLimiter(instagram_service)


class UsernameRequest(BaseModel):
    username: str


@app.get("/")
async def root():
    return {
        "message": "Instagram Analyzer API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "analisar": "/analisar/{username}",
            "perfil": "/perfil/{username}",
            "mock": "/analisar-mock/{username}",
            "pdf": "/gerar-pdf/{username}",
            "status": "/status",
        },
    }


@app.get("/status")
async def check_status():
    """Verifica o status do sistema e rate limiting"""
    blocked_until = rate_limiter.global_blocked_until
    is_blocked = blocked_until and datetime.now() < blocked_until
    
    # Verificar também o rate limit do Instagram Service
    instagram_blocked = instagram_service.rate_limit_until and datetime.now() < instagram_service.rate_limit_until

    return {
        "status": "blocked" if (is_blocked or instagram_blocked) else "online",
        "rate_limited": is_blocked or instagram_blocked,
        "api_blocked_until": blocked_until.isoformat() if is_blocked else None,
        "instagram_blocked_until": instagram_service.rate_limit_until.isoformat() if instagram_blocked else None,
        "cache_entries": len(rate_limiter.request_cache),
        "message": (
            "Sistema operacional" if not (is_blocked or instagram_blocked) else "Sistema em rate limiting"
        ),
    }


@app.get("/analisar/{username}")
async def analisar_perfil(username: str, force_mock: bool = False):
    """
    Analisa um perfil do Instagram e retorna dados + métricas

    Parâmetros:
    - username: Nome do perfil (sem @)
    - force_mock: Se True, usa dados mock diretamente (opcional)
    """
    try:
        # Verificar se deve usar dados mock forçadamente
        if force_mock:
            print(f"⚠️ Modo mock forçado para @{username}")
            instagram_service.use_mock = True
            dados_perfil = await instagram_service.get_profile_data(username)
            metricas = instagram_service.calcular_metricas(dados_perfil)
            dados_perfil["_mock_data"] = True
            dados_perfil["_mock_reason"] = "forced"
            relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

            return {
                "perfil": f"@{username}",
                "dados": dados_perfil,
                "metricas": metricas,
                "relatorio_ia": relatorio_ia,
                "status": "success",
                "data_source": "mock",
            }

        # Verificar rate limiting
        can_proceed, wait_time = rate_limiter.check_rate_limit(username)

        if not can_proceed and wait_time > 0:
            # Verificar se tem dados em cache
            cached_data = rate_limiter.get_cached_data(username)
            if cached_data:
                print(f"📦 Usando dados do cache para @{username}")
                return {
                    **cached_data,
                    "cached": True,
                    "cache_age_minutes": int(
                        (
                            datetime.now() - rate_limiter.request_cache[username][1]
                        ).total_seconds()
                        / 60
                    ),
                }

            # Sem cache, retornar erro de rate limiting
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "rate_limited",
                    "message": f"Por favor, aguarde {wait_time} segundos antes de tentar novamente",
                    "retry_after": wait_time,
                    "suggestion": "Use o endpoint /analisar-mock/{username} para dados de demonstração",
                },
            )

        # Tentar coletar dados reais do Instagram
        try:
            print(f"🔍 Tentando coletar dados reais do perfil @{username}")

            # Adicionar delay antes da requisição
            await asyncio.sleep(2)

            dados_perfil = await instagram_service.get_profile_data(username)
            metricas = instagram_service.calcular_metricas(dados_perfil)
            dados_perfil["_real_data"] = True

            # Verificar se conseguiu coletar posts
            if not dados_perfil.get("posts") or len(dados_perfil.get("posts", [])) == 0:
                print(
                    f"⚠️ Perfil coletado mas sem posts - Instagram pode estar bloqueando"
                )
                # Adicionar aviso
                dados_perfil["_partial_data"] = True
                dados_perfil["_partial_reason"] = "posts_blocked"

            print(f"✅ Dados reais coletados com sucesso para @{username}")

            # Gerar relatório com IA
            relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

            # Registrar requisição bem-sucedida
            response_data = {
                "perfil": f"@{username}",
                "dados": dados_perfil,
                "metricas": metricas,
                "relatorio_ia": relatorio_ia,
                "status": "success",
                "data_source": "instagram",
            }
            rate_limiter.register_request(username, response_data)

            return response_data

        except Exception as instagram_error:
            error_msg = str(instagram_error).lower()

            # Perfil não encontrado ou privado
            if (
                "não encontrado" in error_msg
                or "privado" in error_msg
                or "not found" in error_msg
            ):
                print(f"⚠️ Perfil não encontrado/privado, usando mock")
                instagram_service.use_mock = True
                dados_perfil = await instagram_service.get_profile_data(username)
                metricas = instagram_service.calcular_metricas(dados_perfil)
                dados_perfil["_mock_data"] = True
                dados_perfil["_mock_reason"] = "perfil_nao_encontrado"
                relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

                return {
                    "perfil": f"@{username}",
                    "dados": dados_perfil,
                    "metricas": metricas,
                    "relatorio_ia": relatorio_ia,
                    "status": "success",
                    "data_source": "mock",
                    "warning": "Perfil não encontrado ou privado - usando dados de demonstração",
                }

            # Rate limiting detectado
            elif (
                "rate limiting" in error_msg
                or "aguarde" in error_msg
                or "wait" in error_msg
            ):
                print(f"🔴 Rate limiting detectado: {instagram_error}")

                # Ativar bloqueio global
                rate_limiter.set_global_block(300)  # 5 minutos

                # Usar dados mock como fallback
                instagram_service.use_mock = True
                dados_perfil = await instagram_service.get_profile_data(username)
                metricas = instagram_service.calcular_metricas(dados_perfil)
                dados_perfil["_mock_data"] = True
                dados_perfil["_mock_reason"] = "rate_limited"
                relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

                return {
                    "perfil": f"@{username}",
                    "dados": dados_perfil,
                    "metricas": metricas,
                    "relatorio_ia": relatorio_ia,
                    "status": "limited",
                    "data_source": "mock",
                    "warning": "Instagram está limitando requisições. Usando dados de demonstração.",
                    "retry_after": 300,
                }

            # Acesso bloqueado (401, 403)
            elif (
                "bloqueou" in error_msg or "blocked" in error_msg or "401" in error_msg
            ):
                print(f"🚫 Acesso bloqueado: {instagram_error}")
                rate_limiter.set_global_block(1800)  # 30 minutos

                # Retornar dados mock ao invés de erro
                instagram_service.use_mock = True
                dados_perfil = await instagram_service.get_profile_data(username)
                metricas = instagram_service.calcular_metricas(dados_perfil)
                dados_perfil["_mock_data"] = True
                dados_perfil["_mock_reason"] = "access_blocked"
                relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

                return {
                    "perfil": f"@{username}",
                    "dados": dados_perfil,
                    "metricas": metricas,
                    "relatorio_ia": relatorio_ia,
                    "status": "blocked",
                    "data_source": "mock",
                    "warning": "Acesso ao Instagram temporariamente bloqueado. Usando dados de demonstração.",
                    "retry_after": 1800,
                }

            # Outros erros - usar mock como fallback
            else:
                print(f"⚠️ Erro inesperado, usando fallback mock: {instagram_error}")
                instagram_service.use_mock = True
                dados_perfil = await instagram_service.get_profile_data(username)
                metricas = instagram_service.calcular_metricas(dados_perfil)
                dados_perfil["_mock_data"] = True
                dados_perfil["_mock_reason"] = "erro_instagram"
                relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

                return {
                    "perfil": f"@{username}",
                    "dados": dados_perfil,
                    "metricas": metricas,
                    "relatorio_ia": relatorio_ia,
                    "status": "fallback",
                    "data_source": "mock",
                    "warning": f"Erro ao coletar dados reais: {str(instagram_error)[:100]}",
                }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro inesperado na análise: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}"
        )


@app.get("/perfil/{username}")
async def obter_dados_perfil(username: str):
    """Obtém apenas os dados básicos do perfil"""
    try:
        # Verificar cache primeiro
        cached_data = rate_limiter.get_cached_data(username)
        if cached_data and "dados" in cached_data:
            return {**cached_data["dados"], "cached": True}

        # Verificar rate limit
        can_proceed, wait_time = rate_limiter.check_rate_limit(username)
        if not can_proceed:
            raise HTTPException(
                status_code=429,
                detail=f"Aguarde {wait_time} segundos antes de tentar novamente",
            )

        await asyncio.sleep(2)
        dados_perfil = await instagram_service.get_profile_data(username)
        rate_limiter.register_request(username)

        return dados_perfil
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao obter dados: {str(e)}")


@app.get("/analisar-mock/{username}")
async def analisar_perfil_mock(username: str):
    """Analisa um perfil usando dados mock (para teste/demonstração)"""
    try:
        print(f"🎭 Usando dados mock para @{username}")
        instagram_service.use_mock = True
        dados_perfil = await instagram_service.get_profile_data(username)
        metricas = instagram_service.calcular_metricas(dados_perfil)
        dados_perfil["_mock_data"] = True

        relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)

        return {
            "perfil": f"@{username}",
            "dados": dados_perfil,
            "metricas": metricas,
            "relatorio_ia": relatorio_ia,
            "status": "success",
            "data_source": "mock",
            "note": "Dados de demonstração - não são reais",
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erro ao analisar perfil: {str(e)}"
        )


@app.get("/gerar-pdf/{username}")
async def gerar_pdf(username: str, use_cache: bool = True):
    """Gera um relatório PDF para o perfil"""
    try:
        # Verificar cache se permitido
        if use_cache:
            cached_data = rate_limiter.get_cached_data(username)
            if cached_data:
                print(f"📦 Usando dados do cache para PDF de @{username}")
                dados_perfil = cached_data.get("dados", {})
                metricas = cached_data.get("metricas", {})
                relatorio_ia = cached_data.get("relatorio_ia", {})

                pdf_path = report_service.gerar_pdf(
                    username, dados_perfil, metricas, relatorio_ia
                )
                return {
                    "pdf_path": pdf_path,
                    "message": "PDF gerado com sucesso (dados em cache)",
                    "cached": True,
                }

        # Tentar coletar dados reais
        try:
            can_proceed, wait_time = rate_limiter.check_rate_limit(username)
            if not can_proceed:
                raise Exception(f"Rate limiting: aguarde {wait_time}s")

            await asyncio.sleep(2)
            dados_perfil = await instagram_service.get_profile_data(username)
            metricas = instagram_service.calcular_metricas(dados_perfil)
            rate_limiter.register_request(username)

        except Exception as instagram_error:
            print(f"⚠️ Usando dados mock para PDF: {instagram_error}")
            instagram_service.use_mock = True
            dados_perfil = await instagram_service.get_profile_data(username)
            metricas = instagram_service.calcular_metricas(dados_perfil)
            dados_perfil["_mock_data"] = True

        relatorio_ia = await ai_service.gerar_relatorio(dados_perfil, metricas)
        pdf_path = report_service.gerar_pdf(
            username, dados_perfil, metricas, relatorio_ia
        )

        return {
            "pdf_path": pdf_path,
            "message": "PDF gerado com sucesso",
            "data_source": "mock" if dados_perfil.get("_mock_data") else "instagram",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar PDF: {str(e)}")


if __name__ == "__main__":
    print("🚀 Iniciando Instagram Analyzer API...")
    print("📝 Endpoints disponíveis:")
    print("   - GET /analisar/{username}")
    print("   - GET /analisar-mock/{username}")
    print("   - GET /perfil/{username}")
    print("   - GET /gerar-pdf/{username}")
    print("   - GET /status")
    print("\n⚙️  Configurações:")
    print(f"   - Rate limit por perfil: {rate_limiter.min_interval}s")
    print(f"   - Duração do cache: {rate_limiter.cache_duration}")
    uvicorn.run(app, host="0.0.0.0", port=8000)