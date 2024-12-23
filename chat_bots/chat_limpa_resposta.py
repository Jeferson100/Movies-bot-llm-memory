from langchain_groq import ChatGroq
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from .verificao_key import get_secret_key

load_dotenv()

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError:
    raise ValueError("API key inválida ou não definida")

load_dotenv()


def chat_limpa_resposta(texto: str, api_secret: str = api_secret_groq) -> str:
    model = ChatGroq(
        api_key=api_secret,
        model="llama-3.2-11b-vision-preview",
        temperature=0.5,
        stop_sequences=None,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
                                                        Receive a Markdown text containing information about movies. Extract only the text, 
                                                        removing any unnecessary elements such as formatting, links, images, or other irrelevant data. The length of the result should be less than 6500 characters. 
                                                        Present the result in markdow.
                                                        """
            ),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    llm_chain = prompt | model | StrOutputParser()

    resposta = llm_chain.invoke({"input": texto})

    return resposta
