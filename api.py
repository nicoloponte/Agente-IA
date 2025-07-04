from flask import Flask, request, jsonify
from agent.agent_core import JaimeAgent

app = Flask(__name__)
jaime = JaimeAgent()

@app.route("/api/agent", methods=["POST"])
def agent_api():
    data = request.get_json()
    command = data["command"]
    response = jaime.run(command)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)