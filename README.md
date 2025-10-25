# 📊 Instagram Analyzer

Uma aplicação completa para análise de perfis do Instagram com geração de relatórios estratégicos usando IA.

## 🚀 Funcionalidades

### Análise de Perfis
- ✅ **Dados do Perfil**: Nome, bio, seguidores, posts
- ✅ **Métricas**: Engajamento, frequência, hashtags
- ✅ **Gráficos**: Performance dos posts, hashtags populares
- ✅ **Relatório IA**: Análise estratégica completa
- ✅ **Exportação**: PDF profissional
- ✅ **Dashboard**: Interface moderna e responsiva

### Sistema Anti Rate-Limiting
- ✅ **Retry Inteligente**: Backoff exponencial (5s → 40s)
- ✅ **Delays Adaptativos**: 3-8s entre requisições
- ✅ **Fallback Automático**: Dados mock quando necessário
- ✅ **Cache**: Rate limiting por IP (5-30 min)

### Proteção e Segurança
- ✅ **Rate Limiting**: Sistema robusto de proteção
- ✅ **Fallback**: Dados mock automáticos
- ✅ **Cache**: Gestão inteligente de requisições
- ✅ **Retry Logic**: 3 tentativas com backoff

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **FastAPI** - Framework web moderno
- **Instaloader** - Coleta de dados do Instagram
- **OpenAI API** - Geração de relatórios com IA
- **ReportLab** - Geração de PDFs
- **BeautifulSoup** - Web scraping

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **TailwindCSS** - Estilização
- **Recharts** - Gráficos e visualizações
- **Lucide React** - Ícones

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd instagram-analyzer
```

### 2. Configure o Backend

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example .env
# Edite o arquivo .env com suas chaves
```

### 3. Configure o Frontend

```bash
# Instalar dependências Node.js
npm install
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# OpenAI API Key (obrigatório para relatórios de IA)
[OPENAI_KEY_REMOVED]_chave_openai_aqui

# Instagram credentials (opcional, para perfis privados)
INSTAGRAM_USERNAME=seu_usuario_instagram
INSTAGRAM_PASSWORD=sua_senha_instagram

# API Configuration
API_HOST=localhost
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

## � Solução de Problemas

### Rate Limiting do Instagram
- **Sintoma**: Erro 429 "Too Many Requests"
- **Solução**: Aguarde 5-10 minutos entre análises
- **Alternativa**: Sistema usa dados mock automaticamente

### Perfis Privados
- **Requisito**: Credenciais do Instagram no `.env`
- **Alternativa**: Sistema fornece dados mock
- **Dica**: Teste primeiro com perfis públicos

### Relatórios de IA
- **Requisito**: Chave OpenAI válida no `.env`
- **Erro comum**: "API key not configured"
- **Solução**: Configure OPENAI_API_KEY no `.env`

### Configurações de Retry
- **Tentativas**: 3 máximo
- **Delay base**: 5 segundos
- **Delay máximo**: 60 segundos
- **Jitter**: 0.5x a 1.5x do delay base

## 📊 Como Usar

### Acessar a Aplicação
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000

### Exemplos para Teste
- `natgeo` (perfil público grande)
- `nike` (perfil verificado)
- `starbucks` (perfil comercial)
- `teste` (receberá dados mock)

## �🚀 Como Executar

### 1. Iniciar o Backend
```bash
cd backend
python main.py
```
A API estará disponível em: http://localhost:8000

### 2. Iniciar o Frontend
```bash
npm run dev
```
O frontend estará disponível em: http://localhost:3000

## 📋 Como Usar

1. **Acesse a aplicação** em http://localhost:3000
2. **Digite o username** do Instagram (com ou sem @)
3. **Clique em "Analisar"** para processar o perfil
4. **Visualize os resultados**:
   - Dados básicos do perfil
   - Métricas de engajamento
   - Gráficos de performance
   - Relatório estratégico gerado por IA
5. **Exporte para PDF** se necessário

## 📊 Métricas Calculadas

- **Engajamento médio**: (curtidas + comentários) / seguidores * 100
- **Posts por semana**: Frequência de postagem
- **Média de curtidas**: Média dos últimos posts
- **Média de comentários**: Média dos últimos posts
- **Principais hashtags**: Hashtags mais utilizadas

## 🤖 Relatórios de IA

O sistema gera automaticamente relatórios estratégicos incluindo:

- **Resumo do negócio**
- **Pontos fortes** identificados
- **Pontos fracos** para melhoria
- **Oportunidades** de crescimento
- **Sugestões de abordagem** para prospecção

## 📁 Estrutura do Projeto

```
instagram-analyzer/
├── backend/
│   ├── main.py                 # API principal
│   ├── services/
│   │   ├── instagram_service.py    # Coleta de dados
│   │   ├── ai_service.py           # Integração com IA
│   │   └── report_service.py       # Geração de PDFs
│   └── data/                   # Dados coletados (JSON)
├── app/
│   ├── page.tsx               # Página principal
│   ├── layout.tsx             # Layout da aplicação
│   └── globals.css            # Estilos globais
├── reports/                   # PDFs gerados
├── requirements.txt           # Dependências Python
├── package.json              # Dependências Node.js
└── README.md                 # Este arquivo
```

## ⚠️ Limitações e Considerações

1. **Rate Limiting**: O Instagram pode limitar requisições excessivas
2. **Perfis Privados**: Requer credenciais válidas do Instagram
3. **API Keys**: Necessário configurar chave da OpenAI para relatórios
4. **Dados Públicos**: Apenas perfis públicos são analisados por padrão

## 🔧 Configuração Avançada

### Para Perfis Privados
Configure suas credenciais do Instagram no arquivo `.env`:
```env
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha
```

### Para Relatórios de IA
Obtenha uma chave da OpenAI em: https://platform.openai.com/api-keys

## 📈 Próximos Passos

- [ ] Implementar cache de dados
- [ ] Adicionar mais métricas de análise
- [ ] Suporte a múltiplos perfis
- [ ] Dashboard de comparação
- [ ] Notificações de mudanças
- [ ] Integração com outras redes sociais

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido com ❤️ para análise estratégica de perfis do Instagram**
