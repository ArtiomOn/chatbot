from django.shortcuts import render

from .forms import QuestionForm
from .langchain_utils import conversation


def chat_view(request):
    response = None
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"]
            # Получаем ответ от цепочки
            response = conversation.run(input=question)
    else:
        form = QuestionForm()
    return render(request, "chat/chat.html", {"form": form, "response": response})
