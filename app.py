import json
import os
import requests
from flask import Flask, request, Response, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set up API key
genai.configure(api_key="AIzaSyACn0ut4jxm-Kp9N5zcuOYQrTRJe6Z6aPQ")

# Set up the model
generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


@app.route("/", methods=["POST"])
def post_example():
    if request.method == "POST":
        # Access POST data from the request
        # msg = request.get_json() VOLTAR AO FINAL
        msg = {
            "prompt": f"você agora é um agente de viagens e possui vasta experiência sobre todos os países do mundo. Crie um roteiro de viagens para mim considerando as seguintes informações:\nCidade: [Cidade informada no input field 1]\nPeríodo: [Período informado no input field 2]\nTipos de atividade que mais gosto: [Tipos de atividade informadas no input field 3]\nBudget da viagem: [Informação selecionada no input field 4]\nNão precisa categorizar os dias por tipos de atividade.\nLeve em consideração a proximidade de cada atividade para montar os dias.\nSeja específico e detalhado sobre cada atividade sugerida e dê dicas importantes, como por exemplo, se há necessidade de reserva antecipada para a atividade sugerida.\nSugira restaurantes.\nDê dicas sobre o melhor meio de se locomover na cidade.\nPor fim, informe a média do custo total da viagem com base no roteiro sugerido.\nTenha em mente que eu moro no Brasil."
        }
        print("Prompt: ", msg)

        # Trying to parse message
        try:

            print("There is a text")
            text = msg["prompt"]  # This gets the prompt from the msg

            response = model.generate_content(text)

            print(response.text)

            return response.text

        except Exception as e:
            print("Deu ruim!")
            return e.with_traceback


if __name__ == "__main__":
    app.run(debug=False)
