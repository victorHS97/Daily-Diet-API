from flask import Flask, request, jsonify

app = Flask(__name__)

user = []
diets = []
diets_user = []

# ROTAS DE DIETAS


@app.route('/diet', methods=['POST'])
def create_diet():
    data = request.json
    diets.append(data)
    return jsonify({"message": "Dieta cadastrada com sucesso"})


@app.route('/diet/<int:id_diet>', methods=['PUT'])
def update_diet(id_diet):
    data = request.json
    for d in diets:
        if d['id'] == id_diet:
            d['Name'] = data.get("name")
            d['description'] = data.get("description")
            d['Date/Hour'] = data.get("Date/Hour")
            d['Diet'] = data.get("diet")
            return jsonify({"message": "Dieta atualizada com sucesso"})
    return jsonify({"message": "Dieta nao encontrada"}), 404


@app.route('/diet/<int:id_user>', methods=['GET'])
def get_diet_user(id_user):
    for d in diets:
        if d['id_user'] == id_user:
            diets_user.append(d)
        else:
            diets_user.clear()
            continue
    if diets_user:
        output = {"diets": diets_user}
        return jsonify(output)
    else:
        return jsonify({"message": "Dieta nao encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
