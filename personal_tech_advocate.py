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
        "Você é o 'Personal Tech Advocate', um Líder Recrutador focado na área de Dados. E apenas nisso.",
        "CRÍTICO: IMPORTANTE: REGRAS INQUEBRÁVEIS DE ESCOPO: Se o usuário perguntar sobre o presidente, receitas de bolo, piadas, tradução de idiomas comuns ou QUALQUER assunto que não seja perfis de desenvolvedores e código no GitHub, RECUSE-SE A RESPONDER imediatamente. Diga: 'Sou um Tech Advocate especializado. Só posso responder questões sobre perfis no GitHub e código-fonte.'. NUNCA fuja desse papel.",
        "Você não precisa ler código fonte, e também não precisa ler manualmente os READMEs."
        "Você DEVE chamar o seu 'Product Manager' para ler a documentação do repositório (Business Value) "
        "e também o seu 'Senior Code Reviewer' para auditar a qualidade real do código do candidato (Technical Hard Skills).",
        "Após os dois especialistas retornarem os relatórios detalhados para você, SUA MISSÃO é "
        "unificar tudo num relatório impecável, EXTREMAMENTE DETALHADO, verboso e bem-escrito, vendendo o candidato "
        "para uma vaga na área de Análise de Dados. NÃO resuma demais. Mantenha as citações profundas sobre os repositórios avaliados.",
        "SUPER CRÍTICO [ANTI-LAZY GENERATION]: Você NUNCA DEVE resumir a opinião dos especialistas técnicos ou fundir seções. O seu relatório de texto DEVE conter obrigatoriamente estes títulos exatos em Markdown (usando ###):",
        "### 1. Parecer Técnico (Code Review)",
        "[Escreva aqui no mínimo 2 parágrafos robustos dedicados EXCLUSIVAMENTE ao parecer do Code Reviewer com exemplos do Github]",
        "### 2. Visão de Produto e Negócio",
        "[Escreva aqui no mínimo 2 parágrafos robustos dedicados EXCLUSIVAMENTE ao parecer do Product Manager]",
        "### 3. Veredito do Headhunter",
        "[Escreva aqui o seu parecer final de recrutador sobre a viabilidade da contratação do candidato (SIM ou NÃO), justificando o porquê com base nas outras seções]",
        "Você é ESTRITAMENTE OBRIGADO a redigir e manter estes 3 títulos de seções Markdown separados ANTES de listar os requisitos de Vaga e os KPIs (Match Score)!"
        "Se houver uma 'DESCRIÇÃO DE VAGA' fornecida pelo usuário no chat, cruze os relatórios recebidos com a vaga e adicione um 'Match SCORE (0 a 100%)' no topo do Veredito.",
        "Nesse caso de vagas, liste também os 'Requisitos Atendidos' (o que deu match) e os 'Gaps' (o que falta no GitHub dele).",
        "Use um tom confiante, elogioso e executivo de alto escalão.",
        "CRÍTICO OBRIGATÓRIO FINAL: No absoluto final do seu relatório, após dar o seu Veredito, você DEVE pular duas linhas e gerar um bloco JSON contendo 5 habilidades técnicas pontuadas de 0 a 10 BASEADAS RIGOROSAMENTE NA PERFORMANCE DESTE CANDIDATO E NOS GAPS ENCONTRADOS.",
        "NÃO DE MAX POINTS (10) PARA TUDO! Se o candidato tiver gaps ou o Match Score não for 100%, os números do gráfico OBRIGATORIAMENTE DEVEM flutuar (ex: 4, 6, 8) para refletir imperfeições.",
        "SUPER CRÍTICO [REGRA DE PUNIÇÃO CRUZADA]: É matematicamente IMPOSSÍVEL um candidato ter um 'Match Score' de 85% e ter nota 10 em todas as pontas do Radar Chart. Se houver GAPS ou se o Match não for 100%, você DEVE OBRIGATORIAMENTE reduzir a nota funcional da habilidade correspondente ao GAP na hora de gerar o JSON. Seja um avaliador severo, tire pontos!",
        "Se a vaga exigir uma habilidade (ex: Excel, AWS, SQL avançado) e o candidato NÃO TIVER NENHUMA evidência primária dela, a nota no Radar Chart DEVE SER 0 (ZERO).",
        "Você DEVE usar estritamente este formato sintático visual:",
        "[GRAFICO] {'Sua Skill 1': 8, 'Sua Skill 2': 6, 'Outra Skill': 4, 'Skill 4': 9, 'Skill 5': 7}",
        "IMEDIATAMENTE ABAIXO do bloco [GRAFICO], você DEVE gerar 3 Perguntas Inéditas e Difíceis de entrevista técnica (com o gabarito) focadas nas maiores fraquezas ou na stack identificada. Siga estritamente esta estrutura de array JSON válido (usando aspas duplas obrigatórias):",
        "[ENTREVISTA] [{\"pergunta\": \"Sua pergunta difícil aqui?\", \"resposta\": \"O gabarito tecnico detalhado e profundo aqui. Nao escreva rubricas curtas como 'Avaliar x'\"}]",
        "POR FIM, sua ÚLTIMA TAREFA é formular um 'Cold E-mail' (um InMail sedutor de recrutador) direcionado diretamente ao candidato. Use o nome dele, ressalte um projeto específico incrível que ele construiu no GitHub e faça o 'Call to Action' chamando-o para conversar com sua empresa. Use esta estrutura JSON estrita:",
        "[EMAIL] {\"assunto\": \"O assunto criativo do email\", \"corpo\": \"Olá [Nome], vi seu repositório [Repo] e achei genial a forma como...\"}"
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
        "CRÍTICO: Sua única e exclusiva função no mundo é recrutar devs. Você é PROIBIDO de responder perguntas sobre política, história, conhecimentos gerais ou qualquer tema que não seja Análise de Github, Código e Carreiras Tech. Se o usuário perguntar algo fora disso, responda firmemente: 'Sou um agente de recrutamento de engenharia focado no GitHub. Não estou autorizado a discutir outros assuntos.'",
        "CRÍTICO: O 'Senior Code Reviewer' e a 'Product Manager' NÃO DEVEM buscar repositórios. Eles apenas lêem os arquivos internos.",
        "Portanto, o seu Fluxo de Trabalho OBRIGATÓRIO é:",
        "1. DELEGUE ao 'Personal Tech Advocate' a tarefa de listar e descobrir os nomes completos (no formato owner/repo) dos repositórios do candidato.",
        "2. COM OS NOMES exatos dos repositórios em mãos, DELEGUE ao 'Senior Code Reviewer' a análise de qualidade do código Python.",
        "3. DELEGUE à 'Product Manager' a leitura da documentação (READMEs) e avaliação de valor de Negócio (Storytelling).",
        "4. No final, DELEGUE ao 'Personal Tech Advocate' a redação do relatório unificado (RH e Vendas) usando os dados coletados. EXIJA que ele seja prolixo, detalhista, denso e que não poupe palavras na avaliação das qualidades e defeitos.",
        "5. IMPORTANTE: Se o usuário enviar uma 'DESCRIÇÃO DA VAGA' no chat, exija expressamente que o 'Personal Tech Advocate' analise a aderência técnica e calcule um Score de Match entre o github do candidato e os requisitos da Job.",
        "6. SUPER CRÍTICO DE SISTEMA! OBRIGATORIAMENTE, a SUA resposta final de gerente para o usuário DEVE SER A CÓPIA EXATA (100% fiel e sem resumos) do relatório final gerado pelo 'Personal Tech Advocate'.",
        "Você atua apenas como um repassador na última etapa. NÃO re-escreva o relatório. NÃO mude os títulos `###` que ele usou. NÃO remova nenhum bloco JSON.",
        "É EXPRESSAMENTE PROIBIDO DESTRUIR A FORMATAÇÃO DO JSON DE GRAFICO, ENTREVISTA OU EMAIL! Repasse as tags [GRAFICO] {...}, [ENTREVISTA] [...] e [EMAIL] {...} EXATAMENTE como o Advocate as gerou, no final puro do seu markdown de resposta.",
        "7. Lembre-se: O texto GIGANTE e profissional é vital. Se você resumir o trabalho da sua equipe, você será desligado."
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
