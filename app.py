import json
import os
import requests
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

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
        rawPrompt = request.get_json()["prompt"]
        formattedPrompt = f"{rawPrompt}"
        print("Prompt:", formattedPrompt)

        # Trying to parse message
        try:

            response = model.generate_content(formattedPrompt)

            print(response.text)

            return response.text

        except Exception as e:
            print("Deu ruim!")
            return e.with_traceback


if __name__ == "__main__":
    app.run(debug=False)
