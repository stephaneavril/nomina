from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import openai

# Cargar variables del .env (local) y del entorno en Render
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    if request.method == "POST":
        respuesta_usuario = request.form["respuesta"]
        prompt = f"Un empleado del área de nómina respondió lo siguiente a un caso donde hubo un pago duplicado a 15 empleados:\n\n{respuesta_usuario}\n\nComo coach experto en liderazgo y compliance, genera retroalimentación constructiva y profesional sobre esa respuesta."

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        feedback = response.choices[0].message.content

    return render_template("index.html", feedback=feedback)

# Para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
