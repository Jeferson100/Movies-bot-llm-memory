import streamlit as st
from funcoes_auxiliares import condicional_edges
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory
from funcoes_auxiliares import InMemoryHistory
from chat_bots import chat_bot, chat_summarize_messages
import os
from groq import GroqError


st.set_page_config(
    page_title="Movies-bot-llm",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Movies-bot-llm",
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
    },
)

st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #black;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "config" not in st.session_state:
    st.session_state.config = {"configurable": {"session_id": "foo"}}

if "store" not in st.session_state:
    st.session_state.store = {}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

store = st.session_state.store
config = st.session_state.config
messages = st.session_state.messages


def clear_messages():
    st.session_state.messages = []
    st.session_state.store = {}


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()

    if store[session_id].messages:
        for mes in store[session_id].messages[-2:]:
            if isinstance(mes, HumanMessage):
                if "\n%%%\n" in mes.content:
                    store[session_id].messages[
                        store[session_id].messages.index(mes)
                    ] = HumanMessage(
                        content=mes.content.split("\n%%%\n")[0]  # type: ignore
                    )  # type: ignore
            if isinstance(message, AIMessage):
                store[session_id].messages[store[session_id].messages.index(mes)] = (
                    AIMessage(content=chat_summarize_messages(mes.content, groq_api))  # type: ignore
                )

    # Removendo as duas primeiras mensagens
    tamanho_memoria = sum([len(mes.content) for mes in store[session_id].messages])
    if tamanho_memoria > 6500:
        del store[session_id].messages[:2]
    return store[session_id]


def chat_reposta_condicional(
    enter, memory, config_memory, api_groq, api_searchapi
) -> str:

    input_message = {"messages": [{"content": enter}]}

    resposta_incorporada = condicional_edges(input_message, api_groq, api_searchapi)
    try:
        if isinstance(resposta_incorporada, dict):
            resposta_incorporada = resposta_incorporada["messages"][0]["content"]
    except KeyError:
        resposta_incorporada = resposta_incorporada["messages"][0]["content"]

    resposta_concluida = chat_bot(resposta_incorporada, memory, config_memory, api_groq)

    return resposta_concluida["messages"][0][1]


# Configuração do Streamlit
st.title("Assistente de filmes e séries")

st.image(
    "https://raw.githubusercontent.com/Jeferson100/Movies-bot-llm-memory/refs/heads/main/image/imagem_modificada.webp",
    use_column_width=True,
)

with st.sidebar:
    st.markdown("# Sobre")
    st.markdown(
        """
            **Este chatbot foi criado para sugerir e fornecer informações sobre filmes e séries com base no que o usuário digitar. Ele combina as tecnologias:**
            """
    )

    st.markdown(
        """![python](https://img.shields.io/badge/python-black?style=flat&logo=python)
                    ![Langchain](https://img.shields.io/badge/langchain-black?style=flat&logo=langchain)
                    ![streamlit](https://img.shields.io/badge/streamlit-black?style=flat&logo=streamlit)
                    """
    )
    st.markdown("---")
    st.markdown("# Login APIS:")
    st.write(
        """Para utilizar o Bot, primeiro faça um cadastro gratuito nos sites abaixo e depois gere as chaves APIs necessárias:"""
    )

    st.markdown(
        """
    [![Groq API](https://img.shields.io/badge/Create%20Groq%20API%20Key-black?style=flat&logo=groq)](https://console.groq.com/keys)
    [![Create TAVILY API Key](https://img.shields.io/badge/Create%20TAVILY%20API%20Key-blue?style=flat&logo=key)](https://app.tavily.com/home?code=PySHU7SgEgmNYjzs9NsvBjVy1HyFziRHp1NWQ_-j_MH42&state=eyJyZXR1cm5UbyI6Ii9ob21lIn0)
    [![Create FIRECRAWL API Key](https://img.shields.io/badge/Create%20FIRECRAWL%20API%20Key-red?style=flat&logo=key)](https://www.firecrawl.dev/app/api-keys)
    [![Create SEARCHAPI API Key](https://img.shields.io/badge/Create%20SEARCHAPI%20API%20Key-green?style=flat&logo=key)](https://www.searchapi.io/)
    """,
        unsafe_allow_html=True,
    )
    try:
        if os.getenv("GROQ_API_KEY") is not None:
            groq_api = os.getenv("GROQ_API_KEY")
            st.success("API key GROQ ja existe!", icon="✅")
        else:
            groq_api = st.text_input("Enter GROQ API token:", type="password")

        if os.getenv("TAVILY_API_KEY") is not None:
            tavily_api = os.getenv("TAVILY_API_KEY")
            st.success("API key TAVILY ja existe!", icon="✅")
        else:
            tavily_api = st.text_input("Enter TAVILY API token:", type="password")

        if os.getenv("FIRECRAWL_API_KEY") is not None:
            firecrawl_api = os.getenv("FIRECRAWL_API_KEY")
            st.success("API key FIRECRAWL ja existe!", icon="✅")
        else:
            firecrawl_api = st.text_input("Enter FIRECRAWL API token:", type="password")

        if os.getenv("SEARCHAPI_API_KEY") is not None:
            searchapi_api = os.getenv("SEARCHAPI_API_KEY")
            st.success("API key SEARCHAPI ja existe!", icon="✅")
        else:
            searchapi_api = st.text_input("Enter SEARCHAPI API token:", type="password")
    except ValueError as e:
        st.error(f"Erro ao utilizar a API: {e}")
        st.stop()

    st.markdown("---")

    message_unidas = "\n".join([m["content"] for m in messages])

    st.download_button(
        label="Download Text",  # Rótulo do botão
        data=message_unidas,  # Conteúdo do arquivo
        file_name="documento.txt",  # Nome do arquivo ao ser baixado
        mime="text/plain",  # Tipo MIME do arquivo
        help="Clique para baixar a conversa em texto.",  # Dica ao passar o mouse
    )

    st.download_button(
        label="Download Markdown",  # Rótulo do botão
        data=message_unidas,  # Conteúdo do arquivo
        file_name="documento.md",  # Nome do arquivo ao ser baixado
        mime="text/markdown",  # Tipo MIME do arquivo
        help="Clique para baixar a conversa em Markdown.",
        # Dica ao passar o mouse
    )

    if st.button("Limpar Memoria"):
        clear_messages()

    st.markdown("---")

    st.markdown("# Contatos")
    st.sidebar.markdown(
        """
        <div style="display: inline-block; margin-right: 10px;">
            <a href="https://github.com/jeferson100">
                <img src="https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github">
            </a>
        </div>
        <div style="display: inline-block;">
            <a href="https://www.linkedin.com/in/jefersonsehnem/">
                <img src="https://img.shields.io/badge/linkedin-0077b5?style=for-the-badge&logo=linkedin&logocolor=white">
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )

# Display chat messages from history on app rerun
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input

prompt = st.chat_input(
    "Me pergunte sobre filmes?",
)


if prompt:
    # Add user message to chat history
    messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = chat_reposta_condicional(
            prompt, get_by_session_id, config, groq_api, searchapi_api
        )
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to chat history
        messages.append({"role": "assistant", "content": response})
    except GroqError as e:
        st.error(
            "Por favor, insira um token de API válido. Clique no botão para abrir uma conta na [GROQ](https://console.groq.com/keys) e obter um token."
        )
