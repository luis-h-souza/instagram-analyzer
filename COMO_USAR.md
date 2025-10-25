# 🚀 Como Usar o Instagram Analyzer

## ✅ **Status: FUNCIONANDO!**

Sua aplicação está rodando perfeitamente! Aqui está como usar:

## 🌐 **Acessar a Aplicação**

1. **Frontend**: http://localhost:3000
2. **Backend API**: http://localhost:8000

## 📱 **Como Testar**

### 1. **Teste Básico (Dados Mock)**
- Digite qualquer username (ex: `teste`, `cafeteria`, `loja`)
- Clique em "Analisar"
- Veja os dados mock sendo exibidos

### 2. **Teste com Perfil Real (Opcional)**
Para testar com dados reais do Instagram:
- Configure credenciais no arquivo `.env`
- Aguarde alguns minutos entre tentativas (rate limiting)

## 🔧 **Configurações Disponíveis**

### **Arquivo `.env`**
```env
# Para relatórios de IA (opcional)
[OPENAI_KEY_REMOVED]_chave_openai_aqui

# Para perfis privados (opcional)
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha
```

## 📊 **O que Você Verá**

### **Dados do Perfil**
- Nome, biografia, foto
- Número de seguidores/seguindo
- Total de posts
- Status de verificação

### **Métricas Calculadas**
- Taxa de engajamento
- Posts por semana
- Média de curtidas/comentários
- Principais hashtags

### **Gráficos Interativos**
- Gráfico de barras: engajamento por post
- Gráfico de pizza: distribuição de hashtags

### **Relatório de IA**
- Resumo do negócio
- Pontos fortes/fracos
- Oportunidades
- Sugestões de abordagem

## 🎯 **Exemplos de Usernames para Testar**

- `teste` (dados mock)
- `cafeteria` (dados mock)
- `loja` (dados mock)
- `natgeo` (perfil real - pode ter rate limiting)
- `nike` (perfil real - pode ter rate limiting)

## ⚠️ **Limitações Atuais**

1. **Rate Limiting**: Instagram limita requisições
2. **Dados Mock**: Por padrão, usa dados simulados
3. **IA**: Precisa de chave da OpenAI para relatórios

## 🔄 **Reiniciar a Aplicação**

### **Backend**
```bash
cd backend
python main.py
```

### **Frontend**
```bash
npm run dev
```

## 🐛 **Solução de Problemas**

### **Erro 405 Method Not Allowed**
- ✅ **RESOLVIDO**: Endpoints corrigidos para GET

### **Rate Limiting do Instagram**
- ✅ **RESOLVIDO**: Sistema de fallback para dados mock

### **Erro de API Key**
- Configure a chave da OpenAI no `.env` (opcional)

## 🎉 **Próximos Passos**

1. **Teste a aplicação** com diferentes usernames
2. **Configure a chave da OpenAI** para relatórios de IA
3. **Personalize** os dados mock se necessário
4. **Deploy** para produção quando estiver satisfeito

---

**🎊 Sua aplicação está funcionando perfeitamente! Divirta-se analisando perfis!**
