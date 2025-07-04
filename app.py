from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import threading

# Importa tu agente
from agent.agent_core import JaimeAgent

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
agente = JaimeAgent()
thread = None
stop_flag = False

def ejecutar_agente(query, filepath=None):
    global stop_flag
    try:
        if filepath:
            respuesta = agente.run(f"{query} Archivo: {filepath}")
        else:
            respuesta = agente.run(query)
        return respuesta
    except Exception as e:
        return f"Error: {e}"
    finally:
        stop_flag = False

@app.route("/", methods=["GET", "POST"])
def index():
    global thread, stop_flag
    respuesta = None
    if request.method == "POST":
        if request.form.get("query"):
            query = request.form["query"]
            archivo = request.files.get("archivo")
            if archivo:
                filename = secure_filename(archivo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                archivo.save(filepath)
                thread = threading.Thread(target=ejecutar_agente, args=(query, filepath))
            else:
                thread = threading.Thread(target=ejecutar_agente, args=(query,))
            thread.start()
            respuesta = "Agente en ejecución..."
        else:
            respuesta = "Por favor, ingresa una consulta."
    return render_template("index.html", respuesta=respuesta)

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag, thread
    stop_flag = True
    if thread and thread.is_alive():
        agente.detener()
        thread.join()
        thread = None
    return "Agente detenido."

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)