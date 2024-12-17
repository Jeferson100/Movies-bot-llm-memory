from langchain_groq import ChatGroq
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from typing import Dict, List, Tuple

load_dotenv()


def chat_limpa_resposta(texto: str):
    model = ChatGroq(# type: ignore
        api_key=os.getenv("GROQ_API_KEY"),# type: ignore,
        model="llama-3.2-11b-vision-preview",# type: ignore
        temperature=0.5,# type: ignore
    )  # type: ignore

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

    resposta = llm_chain.invoke([{"role": "user", "content": texto}])

    return resposta
