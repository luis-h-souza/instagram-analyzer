# 🚀 Guia Rápido - Instagram Analyzer

## ⚡ Início Rápido (5 minutos)

### 1. Instalar Dependências
```bash
# Windows
install_dependencies.bat

# Linux/Mac
pip install -r requirements.txt
npm install
```

### 2. Configurar Chaves de API
Edite o arquivo `.env`:
```env
[OPENAI_KEY_REMOVED]_chave_openai_aqui
```

### 3. Executar Aplicação

**Terminal 1 - Backend:**
```bash
# Windows
start_backend.bat

# Linux/Mac
cd backend && python main.py
```

**Terminal 2 - Frontend:**
```bash
# Windows
start_frontend.bat

# Linux/Mac
npm run dev
```

### 4. Usar a Aplicação
1. Acesse: http://localhost:3000
2. Digite um username do Instagram (ex: `cafeteriaxyz`)
3. Clique em "Analisar"
4. Visualize os resultados!

## 📊 O que você receberá:

- **Dados do Perfil**: Nome, bio, seguidores, posts
- **Métricas**: Engajamento, frequência, hashtags
- **Gráficos**: Performance dos posts, hashtags populares
- **Relatório IA**: Análise estratégica completa
- **PDF**: Exportação profissional

## 🔧 Solução de Problemas

### Erro: "Erro ao analisar perfil"
- Verifique se o username existe
- Perfis privados precisam de credenciais do Instagram
- Verifique sua conexão com a internet

### Erro: "Relatório de IA não disponível"
- Configure a chave da OpenAI no arquivo `.env`
- Obtenha uma chave em: https://platform.openai.com/api-keys

### Erro: "Module not found"
- Execute `pip install -r requirements.txt` novamente
- Execute `npm install` novamente

## 🎯 Exemplos de Usernames para Testar

- `natgeo` (National Geographic)
- `nike` (Nike)
- `starbucks` (Starbucks)
- `cafeteriaxyz` (exemplo fictício)

## 📱 Funcionalidades Principais

✅ **Análise Completa**: Dados + métricas + IA
✅ **Interface Moderna**: Dashboard responsivo
✅ **Gráficos Interativos**: Visualizações em tempo real
✅ **Exportação PDF**: Relatórios profissionais
✅ **API REST**: Integração com outros sistemas

---

**Pronto para analisar perfis do Instagram! 🚀**
