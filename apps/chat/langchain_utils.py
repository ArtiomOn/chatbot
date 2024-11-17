from typing import Dict, Any

from django.conf import settings
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI

from apps.chat.promt_templates import PromptTemplates


def build_messages_from_chat_history(chat_history: list) -> list:
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


def get_search_results(query: str) -> str:
    """
    Perform Google search and return formatted results
    """
    search = GoogleSearchAPIWrapper(
        google_api_key=settings.GOOGLE_API_KEY,
        google_cse_id=settings.GOOGLE_CSE_ID,
    )

    results = search.results(query, 3)

    formatted_results = "\n\n".join(
        [
            (
                f"Title: {result['title']}\nSnippet: {result['snippet']}\nLink: {result['link']}"
                if not result.get("Result")
                else "No results found."
            )
            for result in results
        ]
    )

    return formatted_results


def get_streaming_chat_chain(history, use_search: bool = False):
    """
    Build and return a streaming-enabled LangChain chat chain with optional Google Search.
    """
    llm = ChatOpenAI(
        model_name=settings.OPENAI_MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=settings.OPENAI_TEMPERATURE,
        streaming=True,
    )

    prompt_templates = PromptTemplates(use_search)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                prompt_templates.get_system_template
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(
                prompt_templates.get_human_template
            ),
        ]
    )

    def get_chat_history(_: Dict[str, Any]) -> list:
        return history.messages

    def add_search_results(input_dict: Dict[str, Any]) -> Dict[str, Any]:
        input_value = input_dict["input"]
        if use_search and settings.GOOGLE_API_KEY and settings.GOOGLE_CSE_ID:
            search_results = get_search_results(input_value)
            return {
                "input": input_value,
                "chat_history": input_dict["chat_history"],
                "search_results": f"Search Results:\n{search_results}",
                "search_capability": prompt_templates.get_search_capability_template,
            }
        return {
            "input": input_value,
            "chat_history": input_dict["chat_history"],
            "search_results": "",
            "search_capability": prompt_templates.get_search_capability_template,
        }

    chain = (
        RunnablePassthrough()
        | RunnablePassthrough.assign(chat_history=get_chat_history)
        | add_search_results
        | prompt
        | llm
    )

    return chain
