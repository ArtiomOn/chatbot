from typing import Dict, Any

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


def build_messages_from_chat_history(chat_history):
    """
    Convert chat history into a list of LangChain messages.
    """
    messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages


def get_chat_chain(openai_api_key, history):
    """
    Build and return the LangChain chat chain.
    """
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
        temperature=0.7,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a helpful assistant that remembers previous conversation context."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    def get_chat_history(_: Dict[str, Any]) -> list:
        return history.messages

    chain = (
        RunnablePassthrough.assign(chat_history=get_chat_history)
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
