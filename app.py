import streamlit as st

from personal_tech_advocate import agente_time

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
        agente_time.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# --- Componentes Principais da Interface ---
st.title("Apresente um Candidato")

# Estado de Histórico no UI da Tela
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Mensagem Oficial de Saudação
    st.session_state.messages.append(
        {"role": "assistant", "content": "Olá! Digite o nome de usuário do GitHub ou faça uma pergunta sobre as análises anteriores que eu posso te ajudar!"}
    )

# Renderiza todo o histórico salvo na tela a cada re-load
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Campo de Prompt (Chat Box)
if prompt := st.chat_input("Digite o @username do GitHub ou faça perguntas..."):
    # 1. Impressão na tela da mensagem do Usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Chama a Inteligência (O Agente)
    with st.chat_message("assistant"):
        # Mostramos um loader de carregamento na UI para ele pensar
        with st.spinner("Analisando o GitHub e cruzando com padrões de Negócios/Dados..."):

            # Aqui conectamos o Time do Agno na nossa Interface visual.
            resposta_texto = ""
            container = st.empty()

            # Streaming Progressivo: a msg carrega escrevendo em tempo real
            for chunk in agente_time.run(prompt, stream=True):
                # Extraimos as sentenças que o bot devolve string a string
                if isinstance(chunk.content, str):
                    resposta_texto += chunk.content
                    container.markdown(resposta_texto + "▌")

            # Finaliza removendo o Cursor Quadrado
            container.markdown(resposta_texto)

    # Salva essa resposta na interface para não sumir ao recarregar a tela
    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
