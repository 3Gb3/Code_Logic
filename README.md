# CodeLogic

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![Roadmap](https://img.shields.io/badge/roadmap-ativo-0ea5e9)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB)
![Flask](https://img.shields.io/badge/Flask-2.3.x-000000)
![Firebase](https://img.shields.io/badge/Firebase-Auth%20%26%20Firestore-FFCA28)
![Licença](https://img.shields.io/badge/licença-MIT-22c55e)

Plataforma educacional para ensino de lógica e programação em Python, com aulas progressivas, exercícios práticos, execução de código e acompanhamento de progresso.

## Acesso ao projeto

Site publicado: **https://code-logic-iota.vercel.app**

## Status atual

> 🚧 **Projeto em andamento**
>
> O CodeLogic já está funcional e disponível online, mas ainda está em evolução contínua.
> Existem **diversas melhorias planejadas no roadmap** (UX, desempenho, qualidade de código,
> monitoramento e novas funcionalidades pedagógicas).

## Visão geral

O projeto foi construído para apoiar o aprendizado de programação de forma prática, com foco em progressão de conteúdo e feedback rápido.

### Módulos disponíveis

| Módulo | Conteúdo principal | Aulas |
|---|---|---:|
| Sequencial | Fundamentos, entrada/saída, cálculos básicos | 10 |
| Comparativa | Condicionais e tomada de decisão | 10 |
| Repetitiva | Estruturas de repetição e validações | 10 |
| Vetores | Listas, busca, média, filtros e análise | 10 |
| Matrizes | Estruturas bidimensionais e operações com matrizes | 10 |

**Total atual:** 50 aulas.

## Funcionalidades implementadas

- Autenticação com Firebase.
- Controle de progresso por usuário.
- Desbloqueio progressivo de aulas.
- Execução de código Python nos exercícios.
- Correção automatizada com IA (OpenAI, quando configurado).
- Interface web com páginas de login, dashboard, módulos e aulas.

## Stack do projeto

### Backend
- Python
- Flask
- Firebase Admin SDK

### Frontend
- HTML
- CSS
- JavaScript
- Jinja2

### Infraestrutura
- Firebase Auth
- Firestore
- Deploy web em Vercel

## Estrutura principal

```text
Code_Logic/
├── app.py
├── requirements.txt
├── routes/
├── utils/
├── templates/
├── static/
├── api/
├── vercel.json
└── render.yaml
```

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Code_Logic
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar credenciais

- Firebase local: use o arquivo `chave_firebase.json` na raiz do projeto.
- Produção: configure `FIREBASE_CREDENTIALS` como JSON da service account.
- IA (opcional): configure `OPENAI_API_KEY` no arquivo `.env`.

### 5. Executar a aplicação

```bash
python app.py
```

A aplicação inicia em `http://localhost:5000`.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE`.

## Nota final

O CodeLogic é um projeto acadêmico e prático em constante evolução.

Se você usar a plataforma hoje, já encontrará um produto funcional.
Se voltar daqui a algum tempo, encontrará uma versão melhor.
