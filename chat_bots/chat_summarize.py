from langchain_groq import ChatGroq
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def chat_summarize_messages(message):
    """
    Summarize the last two messages in the chat history.

    Args:
        store: The chat history store.
        name: The name of the chat history to summarize.

    Returns:
        The updated chat history store with the last two messages summarized and any messages older than 6000 characters removed.

    """
    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.2-11b-vision-preview",
        temperature=0.5,
    )

    prompt_summary = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
                                                                Summarize the received information and the provided response.
                                                                Try to condense it into 300 characters. Write only the summary without adding extra messages or irrelevant information.
                                                                Use only words, avoiding punctuation or special formatting.
                                                                """
            ),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    llm_chain_summary = prompt_summary | model | StrOutputParser()

    return llm_chain_summary.invoke([{"role": "user", "content": message}])
