from langchain_core.messages import BaseMessage

openai_api_key = "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"

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict, Any


def create_chat_chain(openai_api_key: str):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0.7
    )

    chat_history = ChatMessageHistory()

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a helpful assistant that remembers previous conversation context."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    def get_chat_history(_: Dict[str, Any]) -> list[BaseMessage]:
        return chat_history.messages

    chain = (
        RunnablePassthrough.assign(chat_history=get_chat_history)
        | prompt
        | llm
        | StrOutputParser()
    )

    def invoke_chain(user_input: str) -> str:
        response = chain.invoke({"input": user_input})
        chat_history.add_user_message(user_input)
        chat_history.add_ai_message(response)
        return response

    return invoke_chain


def main():
    chat_chain = create_chat_chain(openai_api_key)

    print("Start chatting (type 'exit' to end):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "выход"]:
            print("Ending conversation.")
            break

        try:
            response = chat_chain(user_input)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
