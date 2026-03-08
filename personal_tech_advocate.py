"""Personal Tech Advocate — Agente de IA com Agno + Gemini.

Este agente analisa os repositórios públicos de um usuário do GitHub
e gera um relatório profissional sobre as competências técnicas do
desenvolvedor, focado em vagas de Análise e Ciência de Dados.
"""

# ============================================================
# PASSO 1 — Importação de bibliotecas
# ============================================================
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.github import GithubTools
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (ex: GOOGLE_API_KEY e GITHUB_ACCESS_TOKEN)
load_dotenv()

from code_reviewer import agente_reviewer  # noqa: E402
from product_manager import agente_pm  # noqa: E402

# ============================================================
# PASSO 2 — Configuração da Ferramenta Nativa (GithubTools)
# ============================================================
# O Agno já fornece uma tool pronta que faz dezenas de operações no GitHub.
ferramenta_github = GithubTools(
    # Quais poderes daremos ao agente?
    # Para economizar, listamos apenas as ferramentas que ele vai precisar usar:
    include_tools=[
        "search_repositories", # 🔍 Permite ao agente buscar repositórios
        "get_repository", # 📦 Permite acessar os detalhes de um repo específico
        "get_file_content", # 🔥 O agente poderá LER seus arquivos (ex: README)
        "list_repositories", # 👤 Permite listar TODOS os seus repositórios
    ]
)


# ============================================================
# PASSO 3 — Configuração dos Agentes Agno
# ============================================================
agente_advocate = Agent(
    name="Personal Tech Advocate",
    role="Headhunter Especializado (Líder Comercial)",

    # --- Modelo de IA ---
    model=Gemini(id="gemini-3.1-flash-lite-preview"),

    # --- Memória (Para ter um Chat Contínuo) ---
    db=SqliteDb(db_file="memoria_groq.db"),
    session_id="analise_rh_leoserpa",
    add_history_to_context=True,

    # --- Ferramentas disponíveis para o agente ---
    tools=[ferramenta_github],

    # --- Instruções de comportamento do agente ---
    instructions=[
        "Você é o 'Personal Tech Advocate', um Líder Recrutador focado na área de Dados.",
        "Você não precisa ler código fonte, e também não precisa ler manualmente os READMEs."
        "Você DEVE chamar o seu 'Product Manager' para ler a documentação do repositório (Business Value) "
        "e também o seu 'Senior Code Reviewer' para auditar a qualidade real do código do candidato (Technical Hard Skills).",
        "Após os dois especialistas retornarem os relatórios detalhados para você, SUA MISSÃO é "
        "unificar tudo num relatório impecável e extremamente bem-escrito, vendendo o candidato "
        "para uma vaga na área de Análise de Dados.",
        "Organize o Resumo Executivo contemplando: "
        "- Forças de Produto (O que o PM avaliou no README e na comunicação). "
        "- Forças de Engenharia (A pureza e arquitetura do código que o Code Reviewer auditou).",
        "Use um tom confiante, elogioso e executivo de alta escalão.",
    ],

    # --- Configurações de exibição ---
    markdown=True,
    debug_mode=True, # Deixa isso True para você ver ele lendo os arquivos!
)

agente_time = Team(
    name="Time de Tech Recruitment",
    # Passamos os 3 Agentes que vão se comunicar sob a gestão do Agno:
    members=[agente_reviewer, agente_pm, agente_advocate],
    # Memória atrelada ao time (banco base unificado):
    db=SqliteDb(db_file="memoria_groq.db"),
    session_id="time_analise_rh_leoserpa",
    add_history_to_context=True,
    model=Gemini(id="gemini-3.1-flash-lite-preview"),
    stream_member_events=False,
    instructions=[
        "Você é o Gerente de uma equipe especializada de Avaliação Tecnológica.",
        "CRÍTICO: O 'Senior Code Reviewer' e a 'Product Manager' NÃO DEVEM buscar repositórios. Eles apenas lêem os arquivos internos.",
        "Portanto, o seu Fluxo de Trabalho OBRIGATÓRIO é:",
        "1. DELEGUE ao 'Personal Tech Advocate' a tarefa de listar e descobrir os nomes completos (no formato owner/repo) dos repositórios do candidato.",
        "2. COM OS NOMES exatos dos repositórios em mãos, DELEGUE ao 'Senior Code Reviewer' a análise de qualidade do código Python.",
        "3. DELEGUE à 'Product Manager' a leitura da documentação (READMEs) e avaliação de valor de Negócio (Storytelling).",
        "4. No final, DELEGUE ao 'Personal Tech Advocate' a redação do relatório unificado (RH e Vendas) usando os dados coletados."
    ],
    markdown=True,
)


# ============================================================
# PASSO 4 — Execução do agente
# ============================================================
if __name__ == "__main__":
    print("====================================")
    print("🤖 Personal Tech Advocate (Com Memória)")
    print("====================================")
    print("Dica Inicial:")
    print("Para começar, copie e cole a mensagem abaixo:")
    print("-> Analise o perfil do GitHub de 'leoserpa'. Depois mande o Code Reviewer olhar o repositório 'Rango-Serpa'.")
    print("Depois que ele responder, faça qualquer outra pergunta sobre a análise!\n")

    # O cli_app transforma o TIME num chat interativo (looping contínuo) automático.
    agente_time.cli_app(markdown=True)
