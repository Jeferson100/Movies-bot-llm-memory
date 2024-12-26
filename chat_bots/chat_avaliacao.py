from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List

from .verificao_key import get_secret_key

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


def chat_avaliacao(
    mensagem: str, api_secret: str = api_secret_groq
) -> Dict[str, List[Dict[str, str]]]:

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
                                                        You are an evaluator of questions. Your task is to determine if a given input is related to movies, series, 
                                                        or questions about these topics. Answer so "Yes" if the input is related, and "No" if it is not. Below are examples to help you understand the task.

                                                        Examples:
                                                        Input 1:
                                                        "What are the new movie releases on Netflix this month?"
                                                        Evaluation: Yes.

                                                        Input 2:
                                                        "How does the chemical formula for sodium chloride work?"
                                                        Evaluation: No.

                                                        Input 3:
                                                        "Who won the Oscar for Best Actor in 2023?"
                                                        Evaluation: Yes.

                                                        Input 4:
                                                        "What is the difference between a CPU and a GPU?"
                                                        Evaluation: No.

                                                        Input 5:
                                                        "What is the best order to watch the Marvel Cinematic Universe movies?"
                                                        Evaluation: Yes.

                                                        Input 6:
                                                        "What is the duration of Messi's contract with Inter Miami?"
                                                        Evaluation: No.

                                                        Input 7:
                                                        "When does the second season of The Witcher premiere on Netflix?"
                                                        Evaluation: Yes.  
                                                        
                                                        Input 8:
                                                        "My name is jeferson"
                                                        Evaluation: No.    
                                                        
                                                        Input 9:
                                                        "Who was _______"
                                                        Evaluation: No. 
                                                        ""
                                                        
                                                        """
            ),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    llm_chain = prompt | model | StrOutputParser()

    resposta = llm_chain.invoke({"input": mensagem})

    return {"messages": [{"content": resposta}]}
