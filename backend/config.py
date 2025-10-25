import os
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]

load_dotenv()

class Config:
    """Configurações centralizadas da aplicação"""
    
    # Instagram
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    
    # OpenAI
    [OPENAI_KEY_REMOVED].getenv("OPENAI_API_KEY")
    
    # Rate Limiting
    MIN_REQUEST_INTERVAL = int(os.getenv("MIN_REQUEST_INTERVAL", "10"))  # segundos
    CACHE_DURATION_HOURS = int(os.getenv("CACHE_DURATION_HOURS", "1"))
    MAX_POSTS_PER_REQUEST = int(os.getenv("MAX_POSTS_PER_REQUEST", "12"))
    GLOBAL_RATE_LIMIT_DURATION = 300  # 5 minutos quando detectar rate limit
    
    # Delays para parecer humano
    MIN_DELAY_BETWEEN_REQUESTS = 2.0  # segundos
    MAX_DELAY_BETWEEN_REQUESTS = 4.0
    MIN_DELAY_BETWEEN_POSTS = 0.5
    MAX_DELAY_BETWEEN_POSTS = 1.5
    
    # Retry settings
    MAX_RETRY_ATTEMPTS = 3
    RETRY_DELAY_MULTIPLIER = 3  # segundos * tentativa
    
    # Session management
    SESSION_REFRESH_HOURS = 12
    
    # Application
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Valida se as configurações essenciais estão presentes"""
        errors = []
        
        if not cls.INSTAGRAM_USERNAME:
            errors.append("INSTAGRAM_USERNAME não configurado no .env")
        
        if not cls.INSTAGRAM_PASSWORD:
            errors.append("INSTAGRAM_PASSWORD não configurado no .env")
        
        if errors:
            print("⚠️ AVISOS DE CONFIGURAÇÃO:")
            for error in errors:
                print(f"  - {error}")
            print("\nA aplicação funcionará apenas com dados mock até que as credenciais sejam configuradas.")
        
        return len(errors) == 0

# Validar ao importar
Config.validate()