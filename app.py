from flask import Flask, request
from flask_cors import CORS
import google.generativeai as genai
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Set up API key
genai.configure(api_key="AIzaSyACn0ut4jxm-Kp9N5zcuOYQrTRJe6Z6aPQ")

# Set up the model
config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=config,
    safety_settings=safety_settings,
)


@app.route("/", methods=["POST"])
def post():
    if request.method == "POST":
        # Access POST data from the request
        prompt = request.get_json()["prompt"]
        print("Prompt:", prompt)

        # Trying to parse message
        try:

            response = model.generate_content(prompt)

            return response.text

        except Exception as e:
            print("Deu ruim!", e)
            return e.with_traceback


if __name__ == "__main__":
    app.run(debug=False)
