from django.http import StreamingHttpResponse
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from langchain_community.chat_message_histories import ChatMessageHistory
from apps.chat.langchain_utils import (
    get_streaming_chat_chain,
    build_messages_from_chat_history,
)
import json


@ensure_csrf_cookie
def chat_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session.save()

    if "chat_history" not in request.session:
        request.session["chat_history"] = []
        request.session.modified = True

    chat_history = request.session.get("chat_history", [])
    return render(request, "chat/chat.html", {"chat_history": chat_history})


def stream_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        if not request.session.session_key:
            request.session.create()
            request.session.save()

        data = json.loads(request.body)
        user_input = data.get("message")

        if not user_input:
            return JsonResponse({"error": "No message provided"}, status=400)

        chat_history = list(request.session.get("chat_history", []))

        chat_history.append({"role": "user", "content": user_input})
        request.session["chat_history"] = chat_history
        request.session.modified = True
        request.session.save()

        messages = build_messages_from_chat_history(chat_history)
        history = ChatMessageHistory(messages=messages)

        chain = get_streaming_chat_chain(settings.OPENAI_API_KEY, history)

        def event_stream():
            full_response = ""
            try:
                for chunk in chain.stream({"input": user_input}):
                    chunk_content = chunk.content
                    full_response += chunk_content
                    yield f"data: {json.dumps({'chunk': chunk_content})}\n\n"

                current_chat_history = list(request.session.get("chat_history", []))
                current_chat_history.append(
                    {"role": "assistant", "content": full_response}
                )

                request.session["chat_history"] = current_chat_history
                request.session.modified = True
                request.session.save()

                yield f"data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache, no-transform"
        response["X-Accel-Buffering"] = "no"
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def reset_chat(request):
    request.session["chat_history"] = []
    request.session.modified = True
    request.session.save()
    return JsonResponse({"status": "success"})
