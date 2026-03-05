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
# PASSO 3 — Configuração do Agente Agno
# ============================================================
agente = Agent(
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
    ],

    # --- Configurações de exibição ---
    markdown=True,
    debug_mode=True, # Deixa isso True para você ver ele lendo os arquivos!
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
    print("-> Analise o perfil do GitHub de 'leoserpa' e verifique ATIVAMENTE se eu tenho menção a 'Power BI' ou 'Dashboards'.")
    print("Depois que ele responder, faça qualquer outra pergunta sobre a análise!\n")

    # O cli_app transforma o agente num chat interativo (looping contínuo) automático.
    agente.cli_app(markdown=True)
