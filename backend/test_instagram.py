import asyncio
from services.mock_service import MockInstagramService


async def test_mock_instagram():
    # Criar instância do serviço mock
    mock_service = MockInstagramService()

    # Testar coleta de dados do perfil
    username = "perfil_teste"
    dados_perfil = await mock_service.get_profile_data(username)

    # Verificar dados básicos do perfil
    assert dados_perfil["username"] == username
    assert "seguidores" in dados_perfil
    assert "seguindo" in dados_perfil
    assert "posts" in dados_perfil
    assert len(dados_perfil["posts"]) == 5

    # Testar cálculo de métricas
    metricas = mock_service.calcular_metricas(dados_perfil)

    # Verificar métricas calculadas
    assert "engajamento_medio" in metricas
    assert "posts_semanais" in metricas
    assert "principais_hashtags" in metricas
    assert "media_curtidas" in metricas
    assert "media_comentarios" in metricas
    assert "taxa_engajamento" in metricas

    # Verificar dados específicos de um post
    primeiro_post = dados_perfil["posts"][0]
    assert "id" in primeiro_post
    assert "caption" in primeiro_post
    assert "likes" in primeiro_post
    assert "comments" in primeiro_post
    assert "date" in primeiro_post
    assert "is_video" in primeiro_post
    assert "url" in primeiro_post
    assert "hashtags" in primeiro_post

    print("✅ Todos os testes passaram com sucesso!")

    return dados_perfil, metricas


if __name__ == "__main__":
    dados_perfil, metricas = asyncio.run(test_mock_instagram())

    print("\nExemplo de dados do perfil gerados:")
    print(f"Username: {dados_perfil['username']}")
    print(f"Seguidores: {dados_perfil['seguidores']}")
    print(f"Total de posts: {dados_perfil['total_posts']}")

    print("\nMétricas calculadas:")
    print(f"Engajamento médio: {metricas['engajamento_medio']}")
    print(f"Posts por semana: {metricas['posts_semanais']}")
    print(f"Top hashtags: {', '.join(metricas['principais_hashtags'])}")
    print(f"Média de curtidas: {metricas['media_curtidas']}")
    print(f"Média de comentários: {metricas['media_comentarios']}")
