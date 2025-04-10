from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    if request.method == "POST":
        respuesta_usuario = request.form["respuesta"]
        prompt = f"""Un empleado del área de nómina respondió lo siguiente a un caso donde hubo un pago duplicado a 15 empleados:\n\n{respuesta_usuario}\n\nComo coach experto en liderazgo y compliance, genera retroalimentación constructiva y profesional sobre esa respuesta."""

        chat_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        feedback = chat_response.choices[0].message.content

    return render_template("index.html", feedback=feedback)

# Para Render: puerto dinámico y host 0.0.0.0
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
