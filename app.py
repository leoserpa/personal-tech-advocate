import json
import re

import markdown
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF


def criar_pdf(texto_markdown):
    html = markdown.markdown(texto_markdown, extensions=['extra'])
    # Codificação segura contra erro de glifos unicode no motor FPDF2 Default
    html_safe = html.encode('latin-1', 'ignore').decode('latin-1')
    pdf = FPDF()
    pdf.add_page()
    pdf.write_html(html_safe)
    return bytes(pdf.output()) # Formato exigido para Download no Streamlit


# Força o recarregamento em tempo real do .env no Hot Reload do Streamlit
load_dotenv(override=True)

from personal_tech_advocate import agente_time  # noqa: E402

# Configurações da página
st.set_page_config(
    page_title="Personal Tech Advocate",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("🤖 Tech Advocate")
    st.markdown("Bem-vindo ao agente recrutador e avaliador especializado em Análise de Dados e Ciência de Dados.")
    st.markdown("---")
    st.markdown("### 💡 Como Usar")
    st.markdown("1. Digite o `@username` público do dev.")
    st.markdown("2. O agente vai ler o perfil, achar projetos de Dados e olhar os `README`s.")
    st.markdown("3. Você receberá um relatório sobre as hard/soft skills.")
    st.markdown("---")

    if st.button("Limpar Histórico", use_container_width=True):
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎯 Avaliação Específica (Opcional)")
    st.markdown("Para fazer um *fit* técnico, cole a Job Description (Requisitos) abaixo:")
    descricao_vaga = st.text_area("Descrição da Vaga", height=150, placeholder="Ex: Sênior Data Engineer. Requisitos: Python, AWS, Snowflake, dbt...")

# --- Componentes Principais da Interface ---
st.title("Apresente um Candidato")

# Estado de Histórico no UI da Tela
if "messages" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []

    # Mensagem Oficial de Saudação
    st.session_state.messages.append(
        {"role": "assistant", "content": "Olá! Digite o nome de usuário do GitHub ou faça uma pergunta sobre as análises anteriores que eu posso te ajudar!"}
    )

# Garante que o agente na memória ativa do Streamlit rode na sessão correta definida pelo navegador
agente_time.session_id = st.session_state.session_id

# Helper para renderizar radar chart:
def renderizar_grafico_se_existir(texto_completo):
    # Procura a tag mágica e extrai o dicionário python que o LLM cuspiu. Ex: {'Python': 8, 'SQL': 4}
    match = re.search(r'\[GRAFICO\]\s*(\{.*?\})', texto_completo, re.DOTALL)
    if match:
        try:
            dados_dict = json.loads(match.group(1).replace("'", '"')) # Parseia de JSON String para Objeto Python Puro

            # Montagem estrutural para o Plotly
            categorias = list(dados_dict.keys())
            valores = list(dados_dict.values())

            # Precisamos duplicar o primeiro no fim pra "fechar o circulo" da teia
            categorias.append(categorias[0])
            valores.append(valores[0])

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=categorias,
                fill='toself',
                name='Senioridade',
                line_color='#00CC96'
            ))
            fig.update_layout(
                polar={"radialaxis": {"visible": True, "range": [0, 10]}},
                showlegend=False,
                margin={"l": 40, "r": 40, "t": 20, "b": 20}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Corta a parte matemática feia pra não poluir o visual do texto no Chat
            texto_limpo = re.sub(r'\[GRAFICO\]\s*\{.*?\}', '', texto_completo, flags=re.DOTALL)
            return texto_limpo
        except Exception:
            return texto_completo # Retorna limpo se der problema de Parsing
    return texto_completo

# Renderiza todo o histórico salvo na tela a cada re-load
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            # Extrai e exibe o plot se houver, e retorna o texto bonitinho
            texto_formatado = renderizar_grafico_se_existir(msg["content"])
            st.markdown(texto_formatado)
        else:
            st.markdown(msg["content"])

# Render botão de download para a última análise feita pelo Agente (se houver)
erros_de_bem_vindo = ["Olá! Digite o nome de usuário do GitHub", "Olá!"]
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    ultimo_texto = st.session_state.messages[-1]["content"]
    if not any(ultimo_texto.startswith(b) for b in erros_de_bem_vindo):
        st.download_button(
            label="📥 Baixar Última Análise em PDF",
            data=criar_pdf(ultimo_texto),
            file_name="Analise_Tech_Advocate.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Campo de Prompt (Chat Box)
if prompt := st.chat_input("Digite o @username do GitHub ou faça perguntas..."):
    # 1. Impressão na tela da mensagem do Usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lógica de Empacotamento de Vaga (Invisível na UI para ficar limpo)
    prompt_enviado_ao_agente = prompt
    if descricao_vaga.strip():
        prompt_enviado_ao_agente = (
            f"O usuário pediu: '{prompt}'.\n\n"
            f"IMPORTANTE: Você deve avaliar o candidato cruzando seu repósitorio com a seguinte DESCRIÇÃO DE VAGA:\n"
            f"\"\"\"{descricao_vaga}\"\"\"\n"
            f"Forneça obrigatoriamente um Match Score (0 a 100%) e liste os Requisitos Atendidos e Gaps."
        )

    # 2. Chama a Inteligência (O Agente)
    with st.chat_message("assistant"):
        # Mostramos um loader de carregamento na UI para ele pensar
        with st.spinner("Analisando o GitHub e cruzando com padrões de Negócios/Dados..."):

            # Aqui conectamos o Time do Agno na nossa Interface visual.
            resposta_texto = ""
            container = st.empty()

            # Streaming Progressivo usando o prompt turbinado com a Job Description
            for chunk in agente_time.run(prompt_enviado_ao_agente, stream=True):
                # Extraimos as sentenças que o bot devolve string a string
                if isinstance(chunk.content, str):
                    resposta_texto += chunk.content
                    container.markdown(resposta_texto + "▌")

            # Finaliza removendo o Cursor Quadrado e tentando renderizar o Radar Chart Visual
            texto_final_limpo = renderizar_grafico_se_existir(resposta_texto)
            container.markdown(texto_final_limpo)

    # Salva essa resposta na interface para não sumir ao recarregar a tela
    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
