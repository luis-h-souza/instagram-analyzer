# 📊 Instagram Analyzer

Uma aplicação completa para análise de perfis do Instagram com geração de relatórios estratégicos usando IA.

## 🚀 Funcionalidades

### Análise de Perfis
- ✅ **Dados do Perfil**: Nome, bio, seguidores, posts
- ✅ **Métricas**: Engajamento, frequência, hashtags
- ✅ **Gráficos**: Performance dos posts, hashtags populares
# 📊 Instagram Analyzer

Uma aplicação para análise de perfis do Instagram com geração de relatórios estratégicos usando IA.

## Principais melhorias no README
- Atualizei instruções de setup e execução (incluindo comandos para Windows)
- Adicionei instruções de formatação de código (Black) e uso do `npm run format`
- Documentei solução para erro de dependência comum (reportlab)

## 🚀 Funcionalidades

- Análise de perfis (dados básicos, métricas, gráficos)
- Relatórios gerados por IA (OpenAI)
- Exportação para PDF (ReportLab)
- Fallback para dados mock quando rate limits ocorrerem

## Tecnologias

- Backend: Python 3.8+, FastAPI, Instaloader, ReportLab, OpenAI
- Frontend: Next.js 14, React, TailwindCSS, Recharts

## Rápido: instalação e execução (Windows / PowerShell)

1) Clone o repositório

```powershell
git clone <url-do-repositorio>
cd instagram-analyzer
```

2) Backend — criar e ativar venv, instalar dependências

```powershell
cd backend
python -m venv .venv
# PowerShell
. .\.venv\Scripts\Activate.ps1
# ou CMD
.\.venv\Scripts\activate.bat
pip install -r ..\requirements.txt
```

3) Frontend

```powershell
cd ..
npm install
```

4) Copie variáveis de ambiente e edite `.env` (na raiz do projeto)

```powershell
cp env.example .env
# Edite .env e defina as chaves necessárias (OPENAI, credenciais Instagram se for usar perfis privados)
```

Exemplo mínimo importante em `.env`:

```env
# OpenAI (necessário para relatórios IA)
OPENAI_API_KEY=chave_openai_aqui

# (Opcional) Credenciais Instagram para perfis privados
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha

# Configuração da API
API_HOST=localhost
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

## Executando a aplicação

Backend (modo rápido):

```powershell
cd backend
python main.py
# ou, com reload (recomendado para desenvolvimento):
# .venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```powershell
cd ..
npm run dev
```

Acesse:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Formatação de código (Black)

O repositório já inclui scripts para rodar o Black e um `npm` script:

- Usar via npm (raiz do projeto):

```powershell
npm run format
```

Esse script prefere o Python dentro de `.venv` quando presente. Você também pode rodar diretamente:

```powershell
. .\.venv\Scripts\Activate.ps1
python -m black .
```

## Solução de problemas comum

- Erro: "ModuleNotFoundError: No module named 'reportlab'"
   - Causa: dependência Python não instalada.
   - Solução: ative a venv e rode `pip install -r requirements.txt`.

- Erro: rate limiting (429)
   - O sistema aplica backoff automático e fallback para dados mock.
   - Solução manual: aguarde 5–30 minutos ou troque de rede/VPN.

## Notas úteis para desenvolvimento

- Se `npm run format` não alterou nada, significa que os arquivos já estavam compatíveis com o estilo do Black.
- Se quiser forçar a checagem sem modificar arquivos:

```powershell
npm run format:check
```

## Troubleshooting de ambiente (Windows)

- Ative a `.venv` antes de instalar pacotes ou rodar o backend para garantir que os pacotes vão para o ambiente correto.
- Se usar PowerShell e der erro ao ativar a venv por política de execução, rode como administrador:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Estrutura do projeto (resumida)

```
instagram-analyzer/
├── backend/                # Código Python (FastAPI)
├── app/                    # Frontend Next.js
├── scripts/                # Helpers (runner do Black)
├── requirements.txt        # Dependências Python
├── package.json            # Scripts e dependências Node
└── README.md
```

## Contribuindo

Abra uma branch, faça commits pequenos e crie um PR. Veja também as issues abertas.

---

Se quiser, posso adaptar o README com instruções adicionais (Docker, CI, husky pre-commit) — diga o que prefere.
