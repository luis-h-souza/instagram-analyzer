import instaloader
import os
import asyncio
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from dotenv import load_dotenv
load_dotenv()


class InstagramService:
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.L = None
        self.session_file = None
        self.last_login = None
        self.rate_limit_until = None
        self._login()

    # ==========================================================
    # LOGIN
    # ==========================================================
    def _login(self):
        """Faz login no Instagram com gerenciamento de sessão e suporte a 2FA"""
        try:
            self.L = instaloader.Instaloader(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                download_pictures=False,
                download_videos=False,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
                max_connection_attempts=3,
                request_timeout=30,
                sleep=True,
                quiet=False,
            )

            self.session_file = Path(f"session-{self.username}")

            # 1️⃣ Tenta carregar sessão anterior
            if self.session_file.exists():
                try:
                    print(f"📦 Carregando sessão salva para {self.username}...")
                    self.L.load_session_from_file(self.username, str(self.session_file))
                    print("✅ Sessão carregada com sucesso.")
                    self.last_login = datetime.now()
                    print(f"🔐 Sessão autenticada como: {self.L.test_login()}")
                    return
                except Exception as session_error:
                    print(f"⚠️ Erro ao carregar sessão: {session_error}")
                    self.session_file.unlink(missing_ok=True)

            # 2️⃣ Se não existir sessão, faz login
            if not self.username or not self.password:
                raise Exception("Credenciais do Instagram não configuradas no .env")

            print(f"🔑 Fazendo login no Instagram com usuário: {self.username}")
            self.L.login(self.username, self.password)

            # 3️⃣ Verifica se o login foi aceito
            logged_user = self.L.test_login()
            if not logged_user:
                raise Exception("Falha no login — verifique usuário/senha ou autenticação 2FA")

            # 4️⃣ Caso o Instagram peça código 2FA
            if "two_factor" in str(logged_user).lower():
                code = input("Digite o código 2FA enviado pelo Instagram: ")
                self.L.two_factor_login(code)

            # 5️⃣ Salva sessão
            self.L.save_session_to_file(str(self.session_file))
            print(f"✅ Login bem-sucedido! Sessão salva em {self.session_file}")
            self.last_login = datetime.now()

        except Exception as e:
            print(f"❌ Erro no login do Instagram: {e}")
            raise Exception(f"Falha ao fazer login: {str(e)}")

    # ==========================================================
    # CONTROLES INTERNOS
    # ==========================================================
    def _check_and_refresh_session(self):
        """Renova sessão se estiver antiga"""
        if self.last_login and datetime.now() - self.last_login > timedelta(hours=12):
            print("🔄 Sessão antiga detectada — renovando...")
            try:
                self._login()
            except Exception as e:
                print(f"⚠️ Erro ao renovar sessão: {e}")

    def _check_rate_limit(self):
        """Verifica se há bloqueio ativo"""
        if self.rate_limit_until and datetime.now() < self.rate_limit_until:
            wait_seconds = int((self.rate_limit_until - datetime.now()).total_seconds())
            raise Exception(f"⏱️ Rate limiting ativo — aguarde {wait_seconds} segundos")

    def _set_rate_limit(self, seconds: int):
        """Ativa temporariamente bloqueio de requisições"""
        self.rate_limit_until = datetime.now() + timedelta(seconds=seconds)
        print(f"🚫 Rate limiting detectado — aguardando {seconds} segundos")

    async def _random_delay(self, min_sec: float = 1.5, max_sec: float = 4.0):
        """Delay aleatório entre ações"""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)

    # ==========================================================
    # COLETA DE DADOS
    # ==========================================================
    async def coletar_dados_perfil(self, username: str, tentativas: int = 3) -> Dict:
        """Coleta dados de um perfil do Instagram com retry e fallback para mock"""
        self._check_rate_limit()
        self._check_and_refresh_session()

        for tentativa in range(1, tentativas + 1):
            try:
                print(f"📸 Coletando dados do perfil @{username} (tentativa {tentativa})")

                await self._random_delay(2, 4)
                profile = instaloader.Profile.from_username(self.L.context, username)

                # Coleta posts com limite
                posts_list, max_posts = [], 12
                for i, post in enumerate(profile.get_posts()):
                    if i >= max_posts:
                        break
                    posts_list.append({
                        "likes": post.likes,
                        "comments": post.comments,
                        "caption": post.caption[:200] if post.caption else "",
                        "date": post.date_local.isoformat(),
                        "is_video": post.is_video,
                        "url": f"https://www.instagram.com/p/{post.shortcode}/"
                    })
                    await self._random_delay(0.5, 1.5)

                dados = {
                    "username": profile.username,
                    "nome_completo": profile.full_name or profile.username,
                    "biografia": profile.biography or "Sem biografia",
                    "seguidores": profile.followers,
                    "seguindo": profile.followees,
                    "total_posts": profile.mediacount,
                    "foto_perfil": profile.profile_pic_url,
                    "is_private": profile.is_private,
                    "is_verified": profile.is_verified,
                    "is_business": profile.is_business_account,
                    "categoria": profile.business_category_name if profile.is_business_account else None,
                    "url_externo": profile.external_url,
                    "posts": posts_list,
                    "coletado_em": datetime.now().isoformat(),
                }

                print(f"✅ Dados coletados com sucesso para @{username}")
                return dados

            except instaloader.exceptions.ProfileNotExistsException:
                raise Exception(f"Perfil @{username} não encontrado.")

            except instaloader.exceptions.PrivateProfileNotFollowedException:
                raise Exception(f"Perfil @{username} é privado e não pode ser acessado.")

            except instaloader.exceptions.LoginRequiredException:
                print("🔐 Sessão expirada — renovando...")
                self._login()
                continue

            except instaloader.exceptions.ConnectionException as e:
                msg = str(e).lower()
                if "wait" in msg or "401" in msg or "rate" in msg:
                    self._set_rate_limit(300)
                    print("⚠️ Bloqueio temporário detectado — retornando dados mock.")
                    return self._mock_profile(username)
                if tentativa < tentativas:
                    wait_time = tentativa * 5
                    print(f"⚠️ Erro de conexão, tentando novamente em {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                raise

            except Exception as e:
                msg = str(e).lower()
                if "rate" in msg or "wait" in msg or "401" in msg:
                    self._set_rate_limit(300)
                    print("⚠️ Rate limiting detectado — retornando dados mock.")
                    return self._mock_profile(username)
                if tentativa < tentativas:
                    print(f"⚠️ Erro na tentativa {tentativa}: {e}")
                    await asyncio.sleep(tentativa * 3)
                    continue
                raise Exception(f"Erro ao coletar dados do perfil: {e}")

        raise Exception(f"Não foi possível coletar dados após {tentativas} tentativas.")

    # ==========================================================
    # MOCK DE DADOS
    # ==========================================================
    def _mock_profile(self, username: str) -> Dict:
        """Retorna dados simulados quando o Instagram bloqueia"""
        return {
            "username": username,
            "nome_completo": "Usuário Mock",
            "biografia": "Dados simulados (modo seguro ativado)",
            "seguidores": random.randint(500, 5000),
            "seguindo": random.randint(100, 1000),
            "total_posts": 12,
            "foto_perfil": "https://via.placeholder.com/150",
            "is_private": False,
            "is_verified": False,
            "is_business": False,
            "posts": [
                {
                    "likes": random.randint(50, 500),
                    "comments": random.randint(0, 30),
                    "caption": f"Post de exemplo {i+1}",
                    "date": (datetime.now() - timedelta(days=i)).isoformat(),
                    "is_video": random.choice([True, False]),
                    "url": "#"
                }
                for i in range(5)
            ],
            "coletado_em": datetime.now().isoformat(),
        }

    # ==========================================================
    # MÉTRICAS
    # ==========================================================
    def calcular_metricas(self, dados: Dict) -> Dict:
        """Calcula métricas de engajamento"""
        try:
            posts = dados.get("posts", [])
            seguidores = dados.get("seguidores", 0)
            if not posts or seguidores == 0:
                return {
                    "taxa_engajamento": 0,
                    "media_likes": 0,
                    "media_comentarios": 0,
                    "total_interacoes": 0,
                    "melhor_post": None,
                    "posts_analisados": 0
                }

            total_likes = sum(p["likes"] for p in posts)
            total_comments = sum(p["comments"] for p in posts)
            total_interacoes = total_likes + total_comments
            media_likes = total_likes / len(posts)
            media_comentarios = total_comments / len(posts)
            media_interacoes = total_interacoes / len(posts)
            taxa_engajamento = (media_interacoes / seguidores) * 100

            melhor_post = max(posts, key=lambda p: p["likes"] + p["comments"])
            return {
                "taxa_engajamento": round(taxa_engajamento, 2),
                "media_likes": round(media_likes, 2),
                "media_comentarios": round(media_comentarios, 2),
                "total_interacoes": total_interacoes,
                "melhor_post": {
                    "likes": melhor_post["likes"],
                    "comments": melhor_post["comments"],
                    "url": melhor_post["url"],
                    "caption": melhor_post["caption"][:100],
                },
                "posts_analisados": len(posts),
                "razao_video_foto": sum(1 for p in posts if p["is_video"]) / len(posts),
            }
        except Exception as e:
            print(f"Erro ao calcular métricas: {e}")
            return {"erro": str(e)}
