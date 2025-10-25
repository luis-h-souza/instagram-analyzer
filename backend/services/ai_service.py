import openai
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class AIService:
    def __init__(self):
        # Configurar OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("Aviso: OPENAI_API_KEY não configurada. Usando relatórios mock.")
        else:
            print("OpenAI API configurada. Relatórios de IA funcionarão.")
    
    async def gerar_relatorio(self, dados_perfil: Dict[str, Any], metricas: Dict[str, Any]) -> Dict[str, str]:
        """
        Gera um relatório estratégico usando IA
        """
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            # Gerar relatório mock baseado nos dados
            return self._gerar_relatorio_mock(dados_perfil, metricas)
        
        try:
            # Preparar dados para análise
            contexto = self._preparar_contexto(dados_perfil, metricas)
            
            # Gerar relatório com GPT
            prompt = f"""
            Analise este perfil do Instagram e gere um relatório estratégico para prospecção comercial:
            
            {contexto}
            
            Gere um relatório estruturado com:
            1. Resumo do negócio (2-3 frases)
            2. Pontos fortes (3-4 itens)
            3. Pontos fracos (2-3 itens)
            4. Oportunidades de melhoria (3-4 itens)
            5. Sugestão de abordagem de prospecção (2-3 frases)
            
            Seja objetivo e focado em oportunidades comerciais.
            """
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um especialista em marketing digital e análise de perfis do Instagram para prospecção comercial."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            relatorio_completo = response.choices[0].message.content
            
            # Extrair seções do relatório
            return self._extrair_secoes_relatorio(relatorio_completo)
            
        except Exception as e:
            # Se houver erro (incluindo quota), usar relatório mock
            print(f"Erro na API da OpenAI: {e}. Usando relatório mock.")
            return self._gerar_relatorio_mock(dados_perfil, metricas)
    
    def _preparar_contexto(self, dados_perfil: Dict[str, Any], metricas: Dict[str, Any]) -> str:
        """Prepara contexto para análise da IA"""
        contexto = f"""
        PERFIL: @{dados_perfil.get('username', 'N/A')}
        Nome: {dados_perfil.get('nome_completo', 'N/A')}
        Biografia: {dados_perfil.get('biografia', 'N/A')}
        Seguidores: {dados_perfil.get('seguidores', 0):,}
        Seguindo: {dados_perfil.get('seguindo', 0):,}
        Total de posts: {dados_perfil.get('total_posts', 0):,}
        Verificado: {'Sim' if dados_perfil.get('verificado', False) else 'Não'}
        Conta privada: {'Sim' if dados_perfil.get('conta_privada', False) else 'Não'}
        
        MÉTRICAS:
        - Engajamento médio: {metricas.get('engajamento_medio', 'N/A')}
        - Posts por semana: {metricas.get('posts_semanais', 0)}
        - Média de curtidas: {metricas.get('media_curtidas', 0):,}
        - Média de comentários: {metricas.get('media_comentarios', 0):,}
        - Principais hashtags: {', '.join(metricas.get('principais_hashtags', [])[:5])}
        
        ÚLTIMOS POSTS:
        """
        
        for i, post in enumerate(dados_perfil.get('posts', [])[:3], 1):
            contexto += f"""
            Post {i}:
            - Legenda: {post.get('legenda', 'N/A')[:100]}...
            - Curtidas: {post.get('curtidas', 0):,}
            - Comentários: {post.get('comentarios', 0):,}
            - Tipo: {post.get('tipo', 'N/A')}
            """
        
        return contexto
    
    def _extrair_secoes_relatorio(self, relatorio: str) -> Dict[str, str]:
        """Extrai seções específicas do relatório gerado"""
        secoes = {
            "resumo_negocio": "Análise não disponível",
            "pontos_fortes": "Análise não disponível", 
            "pontos_fracos": "Análise não disponível",
            "oportunidades": "Análise não disponível",
            "sugestao_prospeccao": "Análise não disponível"
        }
        
        # Dividir por seções (método simples)
        linhas = relatorio.split('\n')
        secao_atual = None
        conteudo_atual = []
        
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
                
            # Detectar início de seção
            if any(palavra in linha.lower() for palavra in ['resumo', 'negócio', 'business']):
                secao_atual = 'resumo_negocio'
                conteudo_atual = [linha]
            elif any(palavra in linha.lower() for palavra in ['fortes', 'strengths', 'pontos fortes']):
                secao_atual = 'pontos_fortes'
                conteudo_atual = [linha]
            elif any(palavra in linha.lower() for palavra in ['fracos', 'weaknesses', 'pontos fracos']):
                secao_atual = 'pontos_fracos'
                conteudo_atual = [linha]
            elif any(palavra in linha.lower() for palavra in ['oportunidades', 'opportunities']):
                secao_atual = 'oportunidades'
                conteudo_atual = [linha]
            elif any(palavra in linha.lower() for palavra in ['prospecção', 'prospecting', 'abordagem']):
                secao_atual = 'sugestao_prospeccao'
                conteudo_atual = [linha]
            elif secao_atual and linha:
                conteudo_atual.append(linha)
            
            # Salvar seção quando encontrar próxima ou fim
            if secao_atual and conteudo_atual:
                secoes[secao_atual] = '\n'.join(conteudo_atual)
        
        return secoes
    
    def _gerar_relatorio_mock(self, dados_perfil: Dict[str, Any], metricas: Dict[str, Any]) -> Dict[str, str]:
        """
        Gera um relatório mock baseado nos dados do perfil
        """
        username = dados_perfil.get('username', 'perfil')
        seguidores = dados_perfil.get('seguidores', 0)
        engajamento = metricas.get('taxa_engajamento', 0)
        posts_semanais = metricas.get('posts_semanais', 0)
        
        # Resumo do negócio
        if seguidores > 10000:
            resumo = f"@{username} é um perfil estabelecido com {seguidores:,} seguidores, demonstrando forte presença digital e potencial comercial significativo."
        elif seguidores > 1000:
            resumo = f"@{username} é um perfil em crescimento com {seguidores:,} seguidores, mostrando engajamento consistente e oportunidades de expansão."
        else:
            resumo = f"@{username} é um perfil emergente com {seguidores:,} seguidores, apresentando potencial de crescimento e desenvolvimento de audiência."
        
        # Pontos fortes
        pontos_fortes = []
        if engajamento > 5:
            pontos_fortes.append(f"Alta taxa de engajamento ({engajamento:.1f}%)")
        if posts_semanais > 3:
            pontos_fortes.append(f"Frequência consistente de posts ({posts_semanais:.1f} posts/semana)")
        if dados_perfil.get('verificado', False):
            pontos_fortes.append("Perfil verificado (maior credibilidade)")
        if not dados_perfil.get('conta_privada', False):
            pontos_fortes.append("Perfil público (conteúdo acessível)")
        
        if not pontos_fortes:
            pontos_fortes = ["Perfil ativo no Instagram", "Presença digital estabelecida"]
        
        # Pontos fracos
        pontos_fracos = []
        if engajamento < 2:
            pontos_fracos.append(f"Baixa taxa de engajamento ({engajamento:.1f}%)")
        if posts_semanais < 1:
            pontos_fracos.append("Frequência baixa de posts")
        if dados_perfil.get('conta_privada', False):
            pontos_fracos.append("Perfil privado (conteúdo restrito)")
        
        if not pontos_fracos:
            pontos_fracos = ["Oportunidade de crescimento", "Potencial de melhoria na estratégia"]
        
        # Oportunidades
        oportunidades = []
        if engajamento < 5:
            oportunidades.append("Melhorar estratégia de conteúdo para aumentar engajamento")
        if posts_semanais < 3:
            oportunidades.append("Aumentar frequência de posts para maior visibilidade")
        oportunidades.append("Desenvolver parcerias estratégicas")
        oportunidades.append("Otimizar uso de hashtags relevantes")
        oportunidades.append("Criar conteúdo interativo (stories, reels)")
        
        # Sugestão de abordagem
        if seguidores > 5000:
            sugestao = f"Abordagem direta e profissional. @{username} tem audiência estabelecida e pode ser um parceiro valioso. Foque em propostas de valor claras e benefícios mútuos."
        elif seguidores > 1000:
            sugestao = f"Abordagem colaborativa. @{username} está em crescimento e pode estar aberto a parcerias. Ofereça suporte e crescimento mútuo."
        else:
            sugestao = f"Abordagem de mentoria. @{username} é um perfil emergente que pode se beneficiar de orientação e parcerias estratégicas."
        
        return {
            "resumo_negocio": resumo,
            "pontos_fortes": " • ".join(pontos_fortes),
            "pontos_fracos": " • ".join(pontos_fracos),
            "oportunidades": " • ".join(oportunidades),
            "sugestao_prospeccao": sugestao
        }
