import asyncio
from services.instagram_service import InstagramService

async def main():
    print("📸 Testando coleta de perfil...")
    service = InstagramService()

    try:
        dados = await service.coletar_dados_perfil("picko_lhs")  # você pode trocar o nome do perfil
        print("\n✅ DADOS COLETADOS:")
        print(dados)

        metricas = service.calcular_metricas(dados)
        print("\n📊 MÉTRICAS CALCULADAS:")
        print(metricas)

    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    asyncio.run(main())
