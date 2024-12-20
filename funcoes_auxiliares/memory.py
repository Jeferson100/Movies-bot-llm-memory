from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from typing import List, Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from chat_bots import chat_summarize_messages
from langchain_core.messages import HumanMessage, AIMessage


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    # def add_messages(self, messages: List[BaseMessage]) -> None:
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


def get_by_session_id(session_id: str, store: dict) -> BaseChatMessageHistory:
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
            if isinstance(mes, AIMessage):
                store[session_id].messages[store[session_id].messages.index(mes)] = (
                    AIMessage(content=chat_summarize_messages(mes.content))  # type: ignore
                )

    # Removendo as duas primeiras mensagens
    tamanho_memoria = sum([len(mes.content) for mes in store[session_id].messages])
    if tamanho_memoria > 6500:
        del store[session_id].messages[:2]
    return store[session_id]


# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
