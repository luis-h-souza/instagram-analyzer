🔧 Guia de Solução de Problemas - Instagram Analyzer
🔴 Erro: Rate Limiting (429 Too Many Requests)
Sintomas:
JSON Query to graphql/query: 401 Unauthorized - "fail" status, 
message "Please wait a few minutes before you try again."
Soluções:
✅ Solução 1: Aguardar o Tempo de Bloqueio
bash
# Verificar status do sistema
curl http://localhost:8000/status
O sistema automaticamente usa dados mock durante o bloqueio.

✅ Solução 2: Usar Endpoint Mock
bash
# Em vez de /analisar/{username}, use:
curl http://localhost:8000/analisar-mock/picko_lhs
✅ Solução 3: Ajustar Configurações
Edite o arquivo .env:

env
MIN_REQUEST_INTERVAL=15  # Aumentar para 15 segundos
CACHE_DURATION_HOURS=2   # Aumentar cache para 2 horas
MAX_POSTS_PER_REQUEST=6  # Reduzir posts coletados
✅ Solução 4: Limpar Sessão e Relogar
bash
# Deletar arquivo de sessão
rm session-seu_usuario

# Reiniciar aplicação
cd backend && python main.py
🚫 Erro: 401 Unauthorized / Login Failed
Sintomas:
Login no Instagram falhou
Sessão inválida ou expirada
Soluções:
✅ Verificar Credenciais
bash
# Conferir .env
cat .env | grep INSTAGRAM
✅ Verificar Login Manual
Tente fazer login manualmente no Instagram pelo navegador com as mesmas credenciais.

✅ Verificar Autenticação de 2 Fatores
Se você tem 2FA ativado:

Desative temporariamente o 2FA
Ou gere uma senha de aplicativo específica
✅ Desbloquear Conta
Se o Instagram bloqueou sua conta:

Acesse instagram.com pelo navegador
Complete o desafio de segurança
Aguarde 24-48h antes de usar a API
⏱️ Erro: Timeout / Connection Error
Sintomas:
ConnectionException
Request timeout
Unable to fetch profile
Soluções:
✅ Aumentar Timeout
No instagram_service.py, ajuste:

python
self.L = instaloader.Instaloader(
    request_timeout=60,  # Aumentar para 60s
    max_connection_attempts=5
)
✅ Verificar Conexão com Internet
bash
# Testar conexão
ping instagram.com
curl -I https://www.instagram.com
✅ Verificar Firewall/Proxy
Desative temporariamente o firewall
Se usa proxy corporativo, configure:
python
L.context._session.proxies = {
    'http': 'http://proxy:porta',
    'https': 'https://proxy:porta'
}
📦 Cache não está Funcionando
Verificar Cache:
bash
curl http://localhost:8000/status
Resposta esperada:

json
{
  "status": "online",
  "cache_entries": 5
}
Limpar Cache:
Reinicie a aplicação para limpar o cache em memória.

🔍 Perfil Não Encontrado
Sintomas:
Perfil @username não encontrado
Profile does not exist
Verificações:
✅ Username correto (sem @)
✅ Perfil não foi deletado
✅ Perfil não está banido
✅ Você não está bloqueado pelo perfil
Teste Manual:
bash
# Abrir no navegador
https://www.instagram.com/username/
🔐 Perfil Privado
Sintomas:
Perfil é privado e você não o segue
Private profile not followed
Soluções:
Siga o perfil com sua conta
Aguarde aprovação
Ou use o endpoint mock para demonstração
💡 Boas Práticas para Evitar Rate Limiting
✅ DO's (Faça):
Aguarde 10-15s entre requisições diferentes
Use cache sempre que possível
Limite análises a 5-10 perfis por hora
Colete no máximo 12 posts por perfil
Use dados mock para testes
Faça login apenas uma vez por sessão
❌ DON'Ts (Não Faça):
Fazer múltiplas requisições simultâneas
Analisar mais de 20 perfis por hora
Coletar todos os posts de uma vez
Fazer login repetidamente
Ignorar mensagens de rate limiting
🔄 Reiniciar Sistema Limpo
bash
# 1. Parar aplicação
Ctrl+C

# 2. Limpar sessões e cache
rm session-*
rm -rf __pycache__

# 3. Reinstalar dependências (se necessário)
pip install --upgrade instaloader

# 4. Reiniciar
python main.py
📊 Monitoramento de Taxa de Sucesso
Verificar Logs:
bash
# Durante execução, observe os emojis:
🔍 = Tentando coletar dados reais
✅ = Sucesso
⚠️ = Fallback para mock
🔴 = Rate limiting detectado
❌ = Erro crítico
📦 = Usando cache
🎭 = Modo mock
Estatísticas de Uso:
bash
# Endpoint de status
curl http://localhost:8000/status

# Resposta:
{
  "status": "online",
  "rate_limited": false,
  "cache_entries": 3
}
🆘 Últimos Recursos
Ainda não funciona?
Use Modo Mock Exclusivamente:
python
# Forçar mock em main.py
FORCE_MOCK_MODE = True
Considere Alternativas:
Instagram Graph API (oficial)
RapidAPI Instagram APIs
Apify Scraper
Phantom Buster
Contate Suporte:
GitHub Issues
Documentação Instaloader
Stack Overflow
📚 Recursos Úteis
Documentação Instaloader
Instagram Graph API
FastAPI Docs
🔍 Debug Avançado
Ativar Modo Debug:
env
# .env
DEBUG=True
LOG_LEVEL=DEBUG
Logs Detalhados:
python
# Adicionar em instagram_service.py
import logging
logging.basicConfig(level=logging.DEBUG)
Testar Conexão Direta:
python
import instaloader
L = instaloader.Instaloader()
L.login("usuario", "senha")
profile = instaloader.Profile.from_username(L.context, "instagram")
print(f"Seguidores: {profile.followers}")
