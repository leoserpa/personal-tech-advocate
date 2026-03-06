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
from agno.tools.github import GithubTools
from dotenv import load_dotenv

from code_reviewer import agente_reviewer

# Carrega as variáveis do arquivo .env (ex: GOOGLE_API_KEY e GITHUB_ACCESS_TOKEN)
load_dotenv()


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
    model=Gemini(id="gemini-2.5-flash"),

    # --- Memória (Para ter um Chat Contínuo) ---
    db=SqliteDb(db_file="agente_memoria.db"),
    session_id="analise_rh_leoserpa",
    add_history_to_context=True,

    # --- Ferramentas disponíveis para o agente ---
    tools=[ferramenta_github],

    # --- Instruções de comportamento do agente ---
    instructions=[
        "Você é o 'Personal Tech Advocate', um especialista em recrutar e apresentar "
        "desenvolvedores para recrutadores de tecnologia.",
        "Sua função principal é ser o tradutor oficial entre o mundo técnico da Ciência de Dados/IA "
        "e os visitantes que buscam entender o valor dos projetos (recrutadores, gestores ou entusiastas).",
        "Você deve ser profissional, didático, entusiasmado e focado em resultados.",
        "IMPORTANTE: Você deve analisar EXCLUSIVAMENTE o portfólio do usuário solicitado.",
        "Não analise, não busque e não mencione repositórios de outras pessoas.",
        "Seu fluxo de trabalho DEVE ser:",
        "  1. Buscar a lista de repositórios do usuário solicitado.",
        "  2. Escolher os 3 repositórios mais focados em Dados/Python/SQL.",
        "  3. Ler o conteúdo do arquivo 'README.md' desses 3 repositórios "
        "     para entender profundamente a qualidade do código e da documentação.",
        "Com base em toda essa investigação, gere um relatório profissional "
        "e persuasivo 'vendendo' o perfil candidato para uma vaga de Dados.",
        "Organize o relatório com seções claras: Resumo do Perfil, "
        "Competências Técnicas, Análise da Documentação (baseada nos READMEs que você leu) "
        "e Projetos de Destaque.",
        "Use um tom confiante e positivo.",
        "NOTA: Peça AJUDA ao seu Sênior Code Reviewer sempre que precisar de "
        "uma auditoria avançada na qualidade do código interno das pastas dos repositórios."
    ],

    # --- Configurações de exibição ---
    markdown=True,
    debug_mode=True, # Deixa isso True para você ver ele lendo os arquivos!
)

agente_time = Agent(
    name="Time de Tech Recruitment",
    # Passamos a lista de Sub-Agentes que o Agno vai gerenciar:
    team=[agente_reviewer, agente_advocate],
    # Memória atrelada ao time e não a um membro único:
    db=SqliteDb(db_file="agente_memoria.db"),
    session_id="time_analise_rh_leoserpa",
    add_history_to_context=True,
    model=Gemini(id="gemini-2.5-flash"),
    instructions=[
        "Você é um gerente de uma equipe especializada.",
        "Se o usuário pedir análises técnicas pesadas de código limpo, pastas ou funções python, delegue ao 'Senior Code Reviewer'.",
        "Se o usuário pedir relatórios focados em vendas, recrutamento ou resumos de READMEs e portfólios, delegue ao 'Personal Tech Advocate'."
    ],
    show_tool_calls=True,
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
