from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from huggingface_hub import InferenceClient
from llama_cpp import Llama
import traceback

llm = Llama(
    model_path="api/models/tinyllama-1.1b-chat-v1.0.Q6_K.gguf",
    n_ctx=2048
)

@api_view(["POST"])
def beybots_chat(request):
    mensaje_usuario = request.data.get("mensaje")

    if not mensaje_usuario:
        return Response(
            {"error": "No se recibió mensaje"},
            status=status.HTTP_400_BAD_REQUEST
        )

       
    prompt=f"""Eres BeyBot 🤖⚡ experto en Beyblade Metal Fight.
Responde máximo en 3 líneas.
No hagas preguntas innecesarias.
Mensaje del usuario: {mensaje_usuario}
Respuesta:"""
    
    output = llm(prompt, max_tokens=120, temperature=0.7, stop=["<|user|>", "Usuario:", "BeyBot:"])

    respuesta = output["choices"][0]["text"].strip()
    
         

    return Response({"respuesta": respuesta})
