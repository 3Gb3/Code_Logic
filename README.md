# CodeLogic - Plataforma Educacional de Programação

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Firebase](https://img.shields.io/badge/Firebase-Admin-orange.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)

## 📝 Sobre o Projeto

**CodeLogic** é uma plataforma educacional interativa desenvolvida para ensinar programação Python de forma progressiva e prática. O projeto abrange desde conceitos básicos de programação até aplicações avançadas de inteligência artificial usando álgebra linear.

### 🎓 Informações Acadêmicas
- **Instituição**: Faculdade Cesuca
- **Orientador**: Professor Arthur Marques de Oliveira
- **Status**: Projeto em andamento, muitas funcionalidades ainda em desenvolvimento

## 🚀 Funcionalidades

### 📚 Módulos de Ensino
- **Sequencial**: Conceitos básicos, variáveis, entrada/saída
- **Comparativa**: Estruturas condicionais e lógica booleana
- **Repetitiva**: Loops, iterações e algoritmos
- **Vetores**: Listas, arrays e estruturas de dados
- **Matrizes**: Álgebra linear e aplicações em IA

### 🛠️ Recursos Técnicos
- Interface web responsiva
- Sistema de autenticação via Firebase
- Acompanhamento de progresso do usuário
- Editor de código interativo
- Exercícios práticos com feedback
- Exemplos de código executáveis

## 🏗️ Arquitetura do Sistema

```
CodeLogic/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── routes/               # Blueprints das rotas
│   ├── auth.py          # Autenticação
│   ├── aulas.py         # Sistema de aulas
│   ├── exercicios.py    # Exercícios práticos
│   ├── api.py           # API endpoints
│   └── progress.py      # Progresso do usuário
├── static/              # Arquivos estáticos (CSS, JS, imagens)
├── templates/           # Templates HTML (Jinja2)
│   ├── login/          # Páginas de autenticação
│   ├── dashboard/      # Painel principal
│   ├── aulas/          # Templates das aulas
│   └── exercicios/     # Exercícios por módulo
└── utils/              # Utilitários e helpers
    ├── executor.py     # Execução de código Python
    ├── comparator.py   # Comparação de respostas
    └── firebase_utils.py # Integração Firebase
```

## 🔧 Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Linguagem principal
- **Flask 2.3.3**: Framework web
- **Firebase Admin**: Autenticação e banco de dados
- **python-dotenv**: Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5/CSS3**: Estrutura e estilização
- **JavaScript**: Interatividade
- **Jinja2**: Templates dinâmicos

### Infraestrutura
- **Firebase Firestore**: Banco de dados NoSQL
- **Firebase Auth**: Sistema de autenticação
- **Flask Blueprints**: Organização modular

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta Firebase (para autenticação e banco de dados)
- Navegador web moderno

## ⚙️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/CodeLogic.git
cd CodeLogic
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração do Firebase

1. Acesse o [Console do Firebase](https://console.firebase.google.com/)
2. Crie um novo projeto
3. Ative a Autenticação e o Firestore
4. Gere uma chave de conta de serviço
5. Baixe o arquivo JSON e renomeie para `chave_firebase.json`
6. Coloque o arquivo na raiz do projeto

### 5. Configuração de variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:
```env
# Configurações da aplicação CodeLogic
# Para usar correção automática com IA, adicione sua chave da OpenAI:
# OPENAI_API_KEY=sua_chave_aqui
```

### 6. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📱 Como Usar

1. **Registro/Login**: Crie uma conta ou faça login
2. **Dashboard**: Visualize seu progresso nos módulos
3. **Aulas**: Acesse conteúdo teórico e exemplos práticos
4. **Exercícios**: Pratique com exercícios interativos
5. **Progresso**: Acompanhe sua evolução no aprendizado

## 🎯 Módulos de Aprendizado

### 📊 Progressão Pedagógica

1. **Módulo Sequencial** (10 aulas)
   - Variáveis e tipos de dados
   - Entrada e saída de dados
   - Operações básicas

2. **Módulo Comparativa** (10 aulas)
   - Estruturas condicionais (if/else)
   - Operadores de comparação
   - Lógica booleana

3. **Módulo Repetitiva** (10 aulas)
   - Laços de repetição (for/while)
   - Controle de fluxo
   - Algoritmos iterativos

4. **Módulo Vetores** (10 aulas)
   - Listas e arrays
   - Métodos de manipulação
   - Algoritmos de busca e ordenação

5. **Módulo Matrizes** (10 aulas)
   - Álgebra linear
   - Operações matriciais
   - Aplicações em IA e machine learning

## 🤝 Contribuição

Este é um projeto acadêmico em desenvolvimento. Contribuições são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe

- **Desenvolvedor**: [Seu Nome]
- **Orientador**: Professor Arthur Marques de Oliveira
- **Instituição**: Faculdade Cesuca

## 📞 Contato

- **Email**: [seu-email@exemplo.com]
- **LinkedIn**: [Seu LinkedIn]
- **GitHub**: [Seu GitHub]

## 🔄 Status do Desenvolvimento

### ✅ Funcionalidades Implementadas
- Sistema de autenticação completo
- 50 aulas distribuídas em 5 módulos
- Interface responsiva
- Sistema de progresso
- Exercícios interativos

### 🚧 Em Desenvolvimento
- Sistema de avaliação automática
- Integração com IA para correção
- Modo multiplayer/colaborativo
- Certificados de conclusão
- Dashboard para professores

### 🎯 Próximas Funcionalidades
- Mobile app
- Gamificação
- Fórum de dúvidas
- Exportação de progresso
- API pública

## 📊 Estatísticas do Projeto

- **Total de Aulas**: 50
- **Linhas de Código**: 10,000+
- **Exercícios Práticos**: 50+
- **Módulos**: 5
- **Tecnologias**: 8+

## 🏆 Objetivos Educacionais

O CodeLogic visa proporcionar uma experiência de aprendizado completa em programação Python, desde conceitos básicos até aplicações avançadas em inteligência artificial, preparando estudantes para o mercado de trabalho em tecnologia.

---

*Projeto desenvolvido como parte do curso de [Seu Curso] na Faculdade Cesuca, sob orientação do Professor Arthur Marques de Oliveira.*