from typing import Dict, Any
import random
from datetime import datetime, timedelta

class MockInstagramService:
    """
    Serviço mock para testar a aplicação sem fazer requisições reais ao Instagram
    """
    
    def __init__(self):
        pass
    
    async def coletar_dados_perfil(self, username: str) -> Dict[str, Any]:
        """
        Retorna dados mock de um perfil do Instagram
        """
        # Simular delay de rede
        import asyncio
        await asyncio.sleep(1)
        
        # Dados mock realistas
        seguidores = random.randint(1000, 50000)
        seguindo = random.randint(100, 2000)
        total_posts = random.randint(50, 500)
        
        # Gerar posts mock
        posts = []
        for i in range(5):
            data_post = datetime.now() - timedelta(days=random.randint(1, 30))
            curtidas = random.randint(50, seguidores // 10)
            comentarios = random.randint(5, curtidas // 10)
            
            post = {
                "id": f"mock_post_{i+1}",
                "legenda": f"Post de exemplo #{i+1} #instagram #foto #vida #feliz #amor",
                "curtidas": curtidas,
                "comentarios": comentarios,
                "data_postagem": data_post.isoformat(),
                "tipo": "foto" if random.choice([True, False]) else "video",
                "url": f"https://instagram.com/p/mock_{i+1}",
                "hashtags": ["instagram", "foto", "vida", "feliz", "amor"]
            }
            posts.append(post)
        
        dados_perfil = {
            "username": username,
            "nome_completo": f"Perfil {username.title()}",
            "biografia": f"✨ Conta de exemplo do @{username}\n📸 Fotos e vídeos incríveis\n🎯 Foco em qualidade",
            "seguidores": seguidores,
            "seguindo": seguindo,
            "total_posts": total_posts,
            "verificado": random.choice([True, False]),
            "conta_privada": random.choice([True, False]),
            "url_perfil": f"https://instagram.com/{username}",
            "foto_perfil": "https://via.placeholder.com/150x150/FF6B6B/FFFFFF?text=IG",
            "posts": posts
        }
        
        return dados_perfil
    
    def calcular_metricas(self, dados_perfil: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula métricas baseadas nos dados mock
        """
        posts = dados_perfil.get("posts", [])
        seguidores = dados_perfil.get("seguidores", 0)
        
        if not posts or seguidores == 0:
            return {
                "engajamento_medio": "0%",
                "posts_semanais": 0,
                "principais_hashtags": [],
                "media_curtidas": 0,
                "media_comentarios": 0,
                "taxa_engajamento": 0
            }
        
        # Calcular métricas
        total_curtidas = sum(post.get("curtidas", 0) for post in posts)
        total_comentarios = sum(post.get("comentarios", 0) for post in posts)
        total_engajamento = total_curtidas + total_comentarios
        
        media_curtidas = total_curtidas / len(posts)
        media_comentarios = total_comentarios / len(posts)
        engajamento_medio = (total_engajamento / len(posts)) / seguidores * 100
        
        # Simular frequência de posts
        posts_semanais = random.uniform(2, 7)
        
        # Hashtags mais usadas
        todas_hashtags = []
        for post in posts:
            todas_hashtags.extend(post.get("hashtags", []))
        
        contador_hashtags = {}
        for hashtag in todas_hashtags:
            contador_hashtags[hashtag] = contador_hashtags.get(hashtag, 0) + 1
        
        principais_hashtags = sorted(
            contador_hashtags.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return {
            "engajamento_medio": f"{engajamento_medio:.1f}%",
            "posts_semanais": round(posts_semanais, 1),
            "principais_hashtags": [tag[0] for tag in principais_hashtags],
            "media_curtidas": round(media_curtidas, 0),
            "media_comentarios": round(media_comentarios, 0),
            "taxa_engajamento": round(engajamento_medio, 2)
        }
