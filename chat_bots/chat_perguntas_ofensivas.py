from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import Dict, List, Tuple
from .verificao_key import get_secret_key

api_secret = get_secret_key("GROQ_API_KEY")
if api_secret is None:
    raise ValueError("API key inválida ou não definida")


def chat_avaliacao_perguntas_ofensivas(
    mensagem: str,
) -> Dict[str, List[Tuple[str, str]]]:

    class resposta(BaseModel):
        boleano: str = Field(
            description="If the question is offensive, respond 'Yes', and if the question is not offensive, respond 'No'."
        )
        comentario: str = Field(
            description="Comment about the question, explaining why it was offensive."
        )

    model = ChatGroq(
        api_key=api_secret,
        model="llama-3.2-11b-vision-preview",
        temperature=0.5,
        stop_sequences=None,
    )
    parser = JsonOutputParser(pydantic_object=resposta)

    prompt = PromptTemplate(
        template="""You are an evaluator of offensive questions about movies and series.
        Your role is to analyze each question submitted by the user and determine whether it contains offensive, discriminatory, or inappropriate content.
    
    Answer the user query:\n{format_instructions}\n{query}\n
    
    Se a pergunta for ofensiva, responda "Sim" em Resposta e explique por que ela é inadequada em Comentário.
    Se a pergunta não for ofensiva, responda "Não" em Resposta e indique que ela está dentro dos padrões aceitáveis.
    
    
    Examples:

    Input:
    "Why are movies directed by women bad?"
    Response:
    "This question contains discriminatory content and is not allowed. We kindly ask you to avoid generalizations and rephrase your question respectfully."

    Input:
    "What are the best science fiction movies of the last 10 years?"
    Response:
    "The question meets acceptable standards."

    Input:
    "Why are actors from a certain country terrible?"
    Response:
    "This question is offensive and not allowed. We kindly ask you to avoid generalizations and rephrase your question respectfully."

    Input:
    "What is the most popular Netflix series currently?"
    Response:
    "The question meets acceptable standards."

    Input:
    "Why is a certain ethnicity never good in hero roles?"
    Response:
    "This question contains discriminatory content and is not allowed. We kindly ask you to address the topic with respect and avoid offensive remarks."

    Input:
    "What are the best documentaries about classic cinema?"
    Response:
    "The question meets acceptable standards."

    Input:
    "I only like movies with white people; recommend a movie like that."
    Response:
    "This question is offensive and not allowed."                                                   
    
    """,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    response = chain.invoke({"query": mensagem})

    return {"messages": [("assistant", response)]}
