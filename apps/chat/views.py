from django.conf import settings
from django.shortcuts import render, redirect
from langchain_community.chat_message_histories import ChatMessageHistory

from .forms import ChatForm
from .langchain_utils import get_chat_chain, build_messages_from_chat_history


def chat_view(request):
    chat_history = request.session.get("chat_history", [])

    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["message"]

            chat_history.append({"role": "user", "content": user_input})

            messages = build_messages_from_chat_history(chat_history)
            history = ChatMessageHistory(messages=messages)

            chain = get_chat_chain(settings.OPENAI_API_KEY, history)

            response = chain.invoke({"input": user_input})

            chat_history.append({"role": "assistant", "content": response})

            request.session["chat_history"] = chat_history

            return redirect("chat")
    else:
        form = ChatForm()

    return render(
        request, "chat/chat.html", {"form": form, "chat_history": chat_history}
    )


def reset_chat(request):
    if "chat_history" in request.session:
        del request.session["chat_history"]
    return redirect("chat")
