<div align="center">
  <h1>🤖 Personal Tech Advocate</h1>
  <p><strong>Autonomous AI Headhunter Team & Technical Assessor</strong></p>
  <p>
    <a href="#-english-version">English</a> • <a href="#-versão-em-português">Português</a>
  </p>
</div>

<br>

---

<br>

# 🇺🇸 English Version

## 📖 About the Project
**Personal Tech Advocate** is an autonomous multi-agent recruitment platform powered by **Agno** and **Streamlit**. It acts as an elite technical headhunter, automatically scanning a candidate's public GitHub repositories to assess their coding skills, business acumen, and cultural fit for Data Science and Engineering roles. 

Instead of relying on basic LLM summaries, the system delegates the workload to a strict hierarchy of AI specialized agents (A Team Leader, a Senior Code Reviewer, and a Product Manager) to provide an un-biased, deep-dive recruitment dossier.

## ✨ Features
- **Multi-Agent Architecture:** Powered by three distinct AI personas analyzing code quality vs. business value.
- **Job Description Matcher:** Paste a job requirement and the AI will calculate a precise `Match Score (%)` identifying strengths and skill gaps.
- **Dynamic Radar Chart:** A Plotly-generated spider chart visualizing the candidate's core competencies automatically derived from their GitHub projects.
- **Technical Interview Generator:** Generates 3 hard, unseen technical interview questions (along with the expected answers) based specifically on the applicant's weaknesses or tech stack to test them during interviews.
- **Cold E-mail Automation:** Drafts a highly personalized outreach pitch (InMail) citing specific code achievements to attract the candidate.
- **PDF Export:** Downloads the entire executive recruitment report as a formatted PDF for C-Level stakeholder reading.

## 🛠️ Technology Stack
- **Framework:** [Agno](https://www.agno.com) (Multi-Agent orchestration)
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **LLM Provider:** Google Gemini API (Flash-Lite / Pro) or Groq (Llama 3)
- **Data Visualization:** Plotly (Spider/Radar Charts)
- **PDF Engine:** fpdf2
- **Package Manager:** `uv` (Fast Python dependency management)

## 🚀 Getting Started

### 1. Prerequisites
You will need Python 3.10+ and the `uv` package manager installed.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/leoserpa/agno_novo.git
cd agno_novo
uv sync
```

### 3. Environment Variables
Create a `.env` file in the root of the project and add your API keys:
```env
# Required for the default LLM (Gemini)
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: To skip rate limits when calling GitHub APIs
GITHUB_ACCESS_TOKEN=your_github_token_here
```

### 4. Running the App
Spin up the Streamlit interface:
```bash
uv run streamlit run app.py
```
Type any GitHub username (e.g., `leoserpa`) in the chat to start the autonomous technical due diligence!

---
<br><br>

# 🇧🇷 Versão em Português

## 📖 Sobre o Projeto
O **Personal Tech Advocate** é uma plataforma de recrutamento multi-agente autônoma alimentada por **Agno** e **Streamlit**. Ele atua como um headhunter técnico de elite, rastreando automaticamente os repositórios públicos de um candidato no GitHub para avaliar suas habilidades de código, visão de negócios e aderência ('fit') para vagas de Ciência de Dados e Engenharia.

Em vez de depender de resumos básicos de IA, o sistema delega o trabalho a uma hierarquia estrita de agentes especializados em IA (Um Gerente de Equipe, um Senior Code Reviewer e uma Product Manager) para fornecer um dossiê de recrutamento imparcial e profundo.

## ✨ Funcionalidades
- **Arquitetura Multi-Agente:** Alimentado por três personas distintas de IA avaliando qualidade de código vs. valor de negócio.
- **Match de Vagas (Job Description):** Cole os requisitos de uma vaga e a IA calculará um `Match Score (%)` preciso, identificando pontos fortes e lacunas.
- **Gráfico Radial Dinâmico (Radar Chart):** Um gráfico de teia gerado via Plotly visualizando as competências centrais do candidato, extraídas matematicamente dos seus projetos.
- **Gerador de Entrevista Técnica:** Gera 3 perguntas técnicas inéditas e difíceis (com gabarito) baseadas estritamente nas fraquezas ou na stack do candidato para testá-lo presencialmente.
- **Automação de Cold E-mail:** Rascunha um 'pitch' de abordagem InMail altamente personalizado, citando conquistas específicas de código para seduzir o candidato.
- **Exportação em PDF:** Baixa o relatório executivo inteiro formatado em PDF para leitura de Stakeholders ou Diretoria.

## 🛠️ Tecnologias Utilizadas
- **Framework:** [Agno](https://www.agno.com) (Orquestração Multi-Agente)
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Provedor de LLM:** Google Gemini API (Flash-Lite / Pro) ou Groq (Llama 3)
- **Visualização de Dados:** Plotly (Spider/Radar Charts)
- **Motor de PDF:** fpdf2
- **Gerenciador de Pacotes:** `uv` (Gestão de dependências Python ultra-rápida)

## 🚀 Como Executar (Getting Started)

### 1. Pré-requisitos
Você precisará do Python 3.10+ e do gerenciador de pacotes `uv` instalado.

### 2. Instalação
Clone o repositório e instale as dependências:
```bash
git clone https://github.com/leoserpa/agno_novo.git
cd agno_novo
uv sync
```

### 3. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API:
```env
# Necessário para o LLM padrão (Gemini)
GOOGLE_API_KEY=sua_chave_de_api_gemini_aqui

# Opcional: Para evitar limites de taxa ao buscar dados nativamente no GitHub
GITHUB_ACCESS_TOKEN=seu_token_do_github_aqui
```

### 4. Rodando o Aplicativo
Inicie a interface no Streamlit:
```bash
uv run streamlit run app.py
```
Digite qualquer nome de usuário do GitHub (ex: `leoserpa`) no chat para iniciar a due diligence técnica autônoma!

---

<div align="center">
  <p>Built with ❤️ by Leonardo Serpa & AI Advocate</p>
</div>
