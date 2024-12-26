from langchain_groq import ChatGroq
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from typing import Dict, List, Tuple
from .verificao_key import get_secret_key

load_dotenv()

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


def chat_bot(
    mensagem: str,
    memory: str,
    config: Dict[str, Dict[str, str]],
    api_secret: str = api_secret_groq,
) -> Dict[str, List[Tuple[str, str]]]:

    model = ChatGroq(
        api_key=api_secret,
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        stop_sequences=None,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
                                                      Role: You are a chatbot focused on movies and series. You receive messages from a user and a list of movies and series with research data gathered from the internet. 
                                                      Use this list of information to provide detailed insights, recommendations, and answers about movies and TV series.
                                                      Never comment in your response that you recebed a list of movies or series from a font external.
                                                      Use this information to provide detailed insights, recommendations, and answers about movies and series.

                                                    Capabilities:

                                                    Provide streaming platforms, synopses, genres, and casts of movies.
                                                    Suggest up to 5 movies with brief summaries if requested.
                                                    Rules:

                                                    Respond only if asked directly about movies or series.
                                                    For streaming availability, share only the platform.
                                                    Respond in Portuguese with a friendly, professional tone.
                                                    Avoid repetition of movies within the same conversation.
                                                    
                                                    Objective:
                                                    Offer accurate, engaging, and concise movie recommendations to enhance the user's experience.

                                                    Limitations:

                                                    Only respond to topics about movies or series.
                                                    Ensure all answers are concise, relevant, and accurate.
                                                      """
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    llm_chain = prompt | model | StrOutputParser()

    chain_with_history = RunnableWithMessageHistory(
        llm_chain,  # type: ignore
        memory,  # type: ignore
        input_messages_key="input",
        history_messages_key="history",
    )

    resposta = chain_with_history.invoke({"input": mensagem}, config=config)  # type: ignore

    return {"messages": [("assistant", resposta)]}
