from flask import Flask, render_template, request
import openai

app = Flask(__name__)

import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    if request.method == "POST":
        respuesta_usuario = request.form["respuesta"]
        prompt = f"Un empleado del área de nómina respondió lo siguiente a un caso donde hubo un pago duplicado a 15 empleados:\n\n{respuesta_usuario}\n\nComo coach experto en liderazgo y compliance, genera retroalimentación constructiva y profesional sobre esa respuesta."
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        feedback = completion.choices[0].message["content"]

    return render_template("index.html", feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
