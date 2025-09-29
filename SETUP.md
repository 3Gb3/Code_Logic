# Guia de Configuração do CodeLogic

## 🔧 Configuração Passo a Passo

### 1. Pré-requisitos
- Python 3.8+
- Git
- Conta Google (para Firebase)

### 2. Configuração do Firebase

#### 2.1. Criar Projeto Firebase
1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Clique em "Adicionar projeto"
3. Nome do projeto: `codelogic-[seu-nome]`
4. Desabilite Google Analytics (opcional)
5. Clique em "Criar projeto"

#### 2.2. Configurar Autenticação
1. No painel do Firebase, vá em "Authentication"
2. Clique na aba "Sign-in method"
3. Ative "Email/Password"
4. Salve as configurações

#### 2.3. Configurar Firestore
1. Vá em "Firestore Database"
2. Clique em "Criar banco de dados"
3. Escolha "Iniciar no modo de teste"
4. Selecione uma localização próxima

#### 2.4. Gerar Chave de Conta de Serviço
1. Vá em "Configurações do projeto" (ícone da engrenagem)
2. Aba "Contas de serviço"
3. Clique em "Gerar nova chave privada"
4. Baixe o arquivo JSON
5. Renomeie para `chave_firebase.json`
6. Coloque na raiz do projeto CodeLogic

### 3. Configuração do Projeto

#### 3.1. Clone e Configuração Inicial
```bash
git clone https://github.com/seu-usuario/CodeLogic.git
cd CodeLogic
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### 3.2. Configuração de Arquivos
```bash
# Copie os arquivos de exemplo
cp .env.example .env
cp chave_firebase.json.example chave_firebase.json

# Edite o arquivo chave_firebase.json com suas credenciais Firebase
# Edite o arquivo .env se necessário
```

#### 3.3. Teste da Aplicação
```bash
python app.py
```

### 4. Configuração Opcional - OpenAI

Se quiser usar correção automática com IA:

1. Crie conta na [OpenAI](https://platform.openai.com/)
2. Gere uma API key
3. Adicione no arquivo `.env`:
```env
OPENAI_API_KEY=sua_chave_aqui
```

### 5. Deploy (Opcional)

#### 5.1. Heroku
```bash
# Instale Heroku CLI
pip install gunicorn
echo "web: gunicorn app:app" > Procfile
git add .
git commit -m "Deploy configuration"
heroku create codelogic-[seu-nome]
heroku config:set FLASK_ENV=production
git push heroku main
```

### 6. Solução de Problemas

#### Erro de Firebase
- Verifique se `chave_firebase.json` está configurado corretamente
- Confirme que Firestore e Authentication estão ativados

#### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Erro de Permissões Firestore
1. Vá no Firebase Console
2. Firestore Database > Regras
3. Temporariamente use:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 7. Estrutura de Dados Firestore

#### Coleção: `users`
```json
{
  "uid": "user_id",
  "email": "user@email.com",
  "name": "Nome do Usuário",
  "created_at": "timestamp"
}
```

#### Coleção: `progress`
```json
{
  "user_id": "user_id",
  "module": "sequencial",
  "lesson": 1,
  "completed": true,
  "score": 100,
  "completed_at": "timestamp"
}
```

### 8. Comandos Úteis

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar nova dependência
pip install package_name
pip freeze > requirements.txt

# Executar em modo debug
python app.py

# Limpar cache Python
find . -type d -name __pycache__ -delete
find . -name "*.pyc" -delete
```

### 9. Contato para Suporte

- **Professor Orientador**: Arthur Marques de Oliveira
- **Instituição**: Faculdade Cesuca
- **GitHub Issues**: Use para reportar problemas técnicos

---

*Este guia cobre a configuração básica. Para configurações avançadas, consulte a documentação do Flask e Firebase.*