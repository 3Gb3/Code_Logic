# CodeLogic - Plataforma Educacional de Programação

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Firebase](https://img.shields.io/badge/Firebase-Admin-orange.svg)
![Aulas](https://img.shields.io/badge/Aulas-50%20Completas-success.svg)
![Módulos](https://img.shields.io/badge/M%C3%B3dulos-5%20Ativos-blue.svg)
![Status](https://img.shields.io/badge/Status-Funcional-brightgreen.svg)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow.svg)

## 📝 Sobre o Projeto

**CodeLogic** é uma plataforma educacional interativa desenvolvida para ensinar programação Python de forma progressiva e prática. O projeto foi construído convertendo 50 exercícios do formato VISUALG (Portugol) para Python, oferecendo uma abordagem estruturada desde conceitos básicos até aplicações avançadas de álgebra linear.

### 🎓 Informações Acadêmicas
- **Instituição**: Faculdade Cesuca
- **Orientador**: Professor Arthur Marques de Oliveira
- **Status**: Plataforma funcional com 50 aulas completas

## 🚀 Funcionalidades

### 📚 Módulos de Ensino Completos

#### 1. **Sequencial** (10 aulas)
Exercícios práticos de programação sequencial:
- Introdução à Programação e Python
- Cálculo de Área e Preço de Terreno
- Cálculos com Retângulo
- Média de Idades
- Soma de Dois Números
- Cálculo de Troco
- Área do Círculo
- Cálculo de Pagamento
- Consumo Médio
- Cálculo de Áreas Geométricas

#### 2. **Comparativa** (10 aulas)
Estruturas condicionais e tomada de decisões:
- Fórmula de Baskara
- Menor de Três Números
- Conta de Telefone
- Conversão de Temperatura
- Análise de Lucro
- Sistema de Lanchonete
- Verificação de Múltiplos
- Plano Cartesiano
- Cálculo de Aumento Salarial
- Verificação de Troco

#### 3. **Repetitiva** (10 aulas)
Estruturas de repetição e loops:
- Validação com Loop
- Múltiplas Leituras
- Senha com Tentativas
- Média com Validação
- Soma de Pares Consecutivos
- Classificação Par/Ímpar e Positivo/Negativo
- Estatísticas de Experimentos
- Sequência de Ímpares
- Tabuada
- Divisão com Validação

#### 4. **Vetores** (10 aulas)
Listas e estruturas de dados lineares:
- Introdução a Listas e Números Negativos
- Soma e Média de Vetores
- Dados Compostos (Nome + Idade + Altura)
- Filtrar Pares com Posições
- Encontrar Maior Valor e Posição
- Soma de Dois Vetores
- Valores Abaixo da Média
- Média de Números Pares
- Pessoa Mais Velha
- Alunos Aprovados

#### 5. **Matrizes** (10 aulas)
Listas bidimensionais e álgebra linear:
- Introdução a Matrizes e Diagonal Principal
- Maior Elemento de Cada Linha
- Soma de Cada Linha
- Soma Acima da Diagonal
- Análise Geral de Matriz
- Contagem de Negativos em Matriz
- Soma de Matrizes
- Matriz Transposta
- Maior Elemento e Posição por Linha
- Análise Completa de Matriz

### 🛠️ Recursos Técnicos
- ✅ **50 aulas completas** convertidas de VISUALG para Python
- ✅ Interface web responsiva e moderna
- ✅ Sistema de autenticação via Firebase
- ✅ Acompanhamento de progresso por módulo
- ✅ Sistema de desbloqueio progressivo de aulas
- ✅ Editor de código interativo com execução em tempo real
- ✅ Correção automática de exercícios com IA
- ✅ Validação de sintaxe Python
- ✅ Exemplos práticos com entrada/saída formatada
- ✅ Sistema de "pular módulo" para usuários avançados

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
│   ├── css/            # Estilos globais
│   ├── js/             # JavaScript (Firebase, validação)
│   ├── aulas/          # CSS dos módulos
│   ├── dashboard/      # CSS do painel
│   ├── login/          # CSS e JS de autenticação
│   ├── img/            # Imagens e ícones
│   └── sequencial/     # CSS específico por módulo
├── templates/           # Templates HTML (Jinja2)
│   ├── base_aula.html  # Template base das aulas
│   ├── login/          # Páginas de autenticação
│   ├── dashboard/      # Painel principal do usuário
│   ├── aulas/          # Páginas dos módulos
│   │   ├── sequencial.html
│   │   ├── comparativa.html
│   │   ├── repetitiva.html
│   │   ├── vetores.html
│   │   └── matrizes.html
│   └── exercicios/     # 50 exercícios organizados
│       ├── sequencial/  # 10 aulas
│       ├── comparativa/ # 10 aulas
│       ├── repetitiva/  # 10 aulas
│       ├── vetores/     # 10 aulas
│       └── matrizes/    # 10 aulas
└── utils/              # Utilitários e helpers
    ├── executor.py     # Execução segura de código Python
    └── ai_corrector.py # Correção automática com IA
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
3. Ative a **Autenticação** (Email/Senha)
4. Ative o **Firestore Database**
5. Gere uma chave de conta de serviço:
   - Configurações do projeto → Contas de serviço
   - Gerar nova chave privada
6. Baixe o arquivo JSON e renomeie para `chave_firebase.json`
7. Coloque o arquivo na raiz do projeto

#### 📊 Estrutura do Firestore

```
firestore/
├── users/                          # Coleção de usuários
│   └── {userId}/                   # Documento do usuário
│       ├── name: string
│       ├── email: string
│       ├── created_at: timestamp
│       └── last_login: timestamp
│
└── user_progress/                  # Coleção de progressos
    └── {userId}/                   # Documento de progresso
        ├── sequencial/
        │   ├── aulas_concluidas: [1,2,3...]
        │   ├── aulas_liberadas: [1,2,3,4...]
        │   └── completed: boolean
        ├── comparativa/
        ├── repetitiva/
        ├── vetores/
        └── matrizes/
```

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

## 🖼️ Interface da Plataforma

### 📱 Telas Principais

- **Login/Registro**: Autenticação via Firebase com interface moderna
- **Dashboard**: Visão geral dos 5 módulos com progresso visual
- **Página de Módulo**: Lista de 10 aulas com sistema de desbloqueio
  - 🔒 Bloqueada (cinza)
  - 🔓 Disponível (azul)
  - ✅ Concluída (verde)
- **Página de Aula**: Editor de código integrado com:
  - Descrição do problema
  - Exemplos de entrada/saída
  - Editor de código Python
  - Botão de execução e submissão
  - Feedback de correção automática

### 🎨 Design
- Interface responsiva (mobile-friendly)
- Tema moderno com gradientes
- Ícones intuitivos
- Animações suaves
- Feedback visual em tempo real

## 📱 Como Usar

1. **Registro/Login**: Crie uma conta ou faça login com Firebase Auth
2. **Dashboard**: Visualize seu progresso nos 5 módulos disponíveis
3. **Selecione um Módulo**: Escolha entre Sequencial, Comparativa, Repetitiva, Vetores ou Matrizes
4. **Aulas Progressivas**: Complete as aulas na ordem para desbloquear as próximas
5. **Exercícios Práticos**: Resolva problemas práticos com correção automática
6. **Acompanhe seu Progresso**: Veja quantas aulas completou em cada módulo
7. **Pular Módulo**: Se já conhece o conteúdo, pode pular o módulo inteiro

### 🎮 Sistema de Desbloqueio
- A primeira aula de cada módulo está sempre disponível
- Complete uma aula para desbloquear a próxima
- Módulos são desbloqueados sequencialmente (complete Sequencial para acessar Comparativa)
- Usuários avançados podem pular módulos conhecidos

## 🎯 Módulos de Aprendizado

### 📊 Progressão Pedagógica Completa

Cada módulo contém **10 aulas** com exercícios práticos baseados em problemas reais, convertidos de VISUALG (Portugol) para Python.

#### **Características de Cada Aula:**
- 🎯 Objetivo claro e definido
- 📚 Conceitos teóricos explicados
- 💡 Problema prático para resolver
- 📝 Exemplos de entrada/saída
- 💻 Editor de código integrado
- ✅ Correção automática com IA
- 🔓 Sistema de desbloqueio progressivo

### **Total: 50 Aulas Completas**

Todas as aulas foram cuidadosamente desenvolvidas seguindo os exercícios dos PDFs fornecidos, garantindo uma progressão pedagógica consistente e efetiva.

## 🤝 Contribuição

Este é um projeto acadêmico ativo e contribuições são bem-vindas! Veja como você pode ajudar:

### 📝 Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### 💡 Áreas para Contribuição
- 🐛 Correção de bugs
- ✨ Novos exercícios ou módulos
- 🎨 Melhorias na interface
- 📚 Documentação
- 🌐 Traduções
- 🧪 Testes automatizados
- ⚡ Otimizações de performance

### 📋 Guidelines
- Mantenha o código limpo e comentado
- Siga a estrutura de pastas existente
- Teste suas alterações antes de submeter
- Documente novas funcionalidades

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe

- **Desenvolvedor**: Gabriel Schwingel Conci
- **Orientador**: Professor Arthur Marques de Oliveira
- **Instituição**: Faculdade Cesuca

## 🔄 Histórico de Desenvolvimento

### 📅 Versão Atual (Outubro 2025)
- ✅ **50 aulas completas** criadas e validadas
- ✅ Conversão integral de exercícios VISUALG → Python
- ✅ Sincronização de títulos entre módulos e aulas
- ✅ Sistema de progresso funcional
- ✅ Correção automática com IA implementada
- ✅ Interface responsiva e moderna

### 🛠️ Processo de Conversão
Todo o conteúdo foi cuidadosamente adaptado:
1. **Análise dos PDFs**: 5 PDFs fonte com exercícios em VISUALG
2. **Extração de Conteúdo**: Mapeamento de todos os 50 exercícios
3. **Conversão para Python**: Adaptação da sintaxe e lógica
4. **Criação de Templates**: Estrutura consistente com Jinja2
5. **Validação**: Verificação de sintaxe e estrutura
6. **Sincronização**: Títulos e descrições consistentes

### 📝 Estrutura das Aulas
Cada uma das 50 aulas segue o padrão:
```
- Objetivo (🎯)
- Conceitos Teóricos (📚)
- Problema Prático (💡)
- Exemplos com Entrada/Saída (📝)
- Código Inicial (💻)
- Descrição para IA (🤖)
```

## 🔄 Status do Desenvolvimento

### ✅ Funcionalidades Implementadas
- ✅ Sistema de autenticação completo via Firebase
- ✅ **50 aulas distribuídas em 5 módulos** (100% completo)
- ✅ Interface responsiva e moderna
- ✅ Sistema de progresso por usuário
- ✅ Sistema de desbloqueio progressivo de aulas
- ✅ Editor de código Python integrado
- ✅ Execução de código em tempo real
- ✅ Correção automática com IA
- ✅ Validação de sintaxe Python
- ✅ Sistema de "pular módulo"
- ✅ Títulos das aulas sincronizados entre módulos e páginas
- ✅ Todos os exercícios convertidos de VISUALG para Python

### 🚧 Em Desenvolvimento
- ⏳ Sistema de ranking/leaderboard
- ⏳ Modo colaborativo
- ⏳ Certificados de conclusão
- ⏳ Dashboard para professores/instrutores

### 🎯 Próximas Funcionalidades Planejadas
- 📱 Aplicativo mobile (React Native)
- 🎮 Gamificação com conquistas e badges
- 💬 Fórum de dúvidas entre alunos
- 📊 Relatórios detalhados de desempenho
- 🔗 API pública para integrações
- 🌐 Suporte multilíngue

## 📊 Estatísticas do Projeto

- 📚 **Total de Aulas**: 50 (100% completas)
- 💻 **Linhas de Código**: ~15,000+
- 🎯 **Exercícios Práticos**: 50 (todos com correção automática)
- 📦 **Módulos**: 5 (Sequencial, Comparativa, Repetitiva, Vetores, Matrizes)
- 🔧 **Tecnologias**: 10+ (Python, Flask, Firebase, HTML/CSS/JS, etc.)
- 📖 **Templates HTML**: 60+ arquivos
- 🎨 **Arquivos CSS**: 15+ estilos customizados
- ⚡ **Arquivos JavaScript**: 10+ scripts interativos
- 🔥 **Firebase Collections**: 2 (users, user_progress)
- 📝 **Conversão**: VISUALG → Python (50 exercícios)

## 🏆 Objetivos Educacionais

O CodeLogic visa proporcionar uma experiência de aprendizado completa e estruturada em programação Python, seguindo uma metodologia pedagógica consistente:

### 🎓 Metodologia
1. **Progressão Linear**: Aulas organizadas do básico ao avançado
2. **Aprender Fazendo**: Cada aula tem um exercício prático
3. **Feedback Imediato**: Correção automática com IA
4. **Gamificação**: Sistema de desbloqueio e acompanhamento de progresso
5. **Conversão Pedagógica**: Exercícios adaptados de VISUALG para Python mantendo a essência didática

### 🎯 Objetivos
- ✅ Ensinar fundamentos sólidos de programação
- ✅ Desenvolver pensamento lógico e algorítmico
- ✅ Preparar para estruturas de dados avançadas
- ✅ Introduzir conceitos de álgebra linear aplicada
- ✅ Criar base para machine learning e IA
- ✅ Preparar estudantes para o mercado de trabalho

### 📈 Resultados Esperados
Ao concluir os 5 módulos, o aluno será capaz de:
- Desenvolver programas Python completos
- Resolver problemas usando estruturas de dados
- Implementar algoritmos eficientes
- Trabalhar com matrizes e álgebra linear
- Ter base sólida para estudos avançados em IA/ML

---

*Projeto desenvolvido como parte do curso de Análise e Desenvolvimento de Sistemas na Faculdade Cesuca, sob orientação do Professor Arthur Marques de Oliveira.*
