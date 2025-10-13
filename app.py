from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resgatar-pontos")
def resgatar_pontos():
    return jsonify({"message": "Você acessou a rota de Resgatar Pontos!"})

@app.route("/consultar-rotas")
def consultar_rotas():
    return jsonify({"message": "Consultando rotas..."})

@app.route("/planejar-rota")
def planejar_rota():
    return jsonify({"message": "Planejando rota..."})

@app.route("/salvar-trajeto")
def salvar_trajeto():
    return jsonify({"message": "Trajeto salvo com sucesso!"})

@app.route("/feedback")
def feedback():
    return jsonify({"message": "Envie seu feedback!"})

if __name__ == "__main__":
    app.run(debug=True)
