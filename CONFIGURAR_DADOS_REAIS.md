# 🔧 Configurar Dados Reais do Instagram

## 📋 **Passo a Passo para Usar Dados Reais**

### 1. **Configurar Credenciais do Instagram**

Edite o arquivo `.env` e adicione suas credenciais:

```env
# Instagram credentials (OBRIGATÓRIO para dados reais)
INSTAGRAM_USERNAME=seu_usuario_instagram
INSTAGRAM_PASSWORD=sua_senha_instagram

# OpenAI API Key (já configurada)
[OPENAI_KEY_REMOVED]_pUPeuT3BlbkFJK1hpd9tSWhSmVeqyV7DRPXcNakFCfJXYXSOW6q-yq52ock7Nd_bALzwdO1BCanoO7dT4dPyCYA
```

### 2. **Reiniciar a Aplicação**

```bash
# Parar o backend atual
taskkill /F /IM python.exe

# Iniciar novamente
cd backend && python main.py
```

### 3. **Testar com Perfis Reais**

Agora você pode testar com perfis reais do Instagram:
- `natgeo` (National Geographic)
- `nike` (Nike)
- `starbucks` (Starbucks)
- Qualquer perfil público

## ⚠️ **Importante**

### **Rate Limiting**
- Instagram limita requisições por IP
- Aguarde 2-5 segundos entre análises
- Se receber erro 429, aguarde alguns minutos

### **Perfis Privados**
- Só funcionam com credenciais válidas
- Perfis públicos funcionam sem credenciais

### **Dados Mock**
- Usados apenas quando perfil não existe
- Usados quando Instagram está indisponível

## 🎯 **O que Mudou**

✅ **Prioridade para dados reais** - Tenta Instagram primeiro
✅ **Melhor tratamento de erros** - Mensagens mais claras
✅ **Rate limiting inteligente** - Aguarda entre requisições
✅ **Fallback para mock** - Só quando necessário
✅ **API OpenAI corrigida** - Relatórios de IA funcionando

## 🚀 **Teste Agora**

1. Configure suas credenciais no `.env`
2. Reinicie o backend
3. Teste com `natgeo` ou `nike`
4. Veja dados reais do Instagram!

---

**🎊 Agora sua aplicação usa dados reais do Instagram!**
