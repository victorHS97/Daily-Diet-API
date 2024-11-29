from flask import Flask, request, jsonify
from database import db
from models.user import User
from models.diets import Diets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

user = []
diets = []

# ROTAS DE DIETAS


@app.route('/diet', methods=['POST'])
def create_diet():
    data = request.json
    id = data.get("id")
    name = data.get("name")
    description = data.get("description")
    date_hour = data.get("Date/Hour")
    diet = data.get("diet")
    id_user = data.get("id_user")
    diet = Diets(id=id, name=name, description=description,
                 date_hour=date_hour, diet=diet, id_user=id_user)
    db.session.add(diet)
    db.session.commit()
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
    diets_user = []
    for d in diets:
        if d['id_user'] == id_user:
            diets_user.append(d)
    if diets_user:
        output = {"diets": diets_user}
        return jsonify(output)
    else:
        return jsonify({"message": "Dieta nao encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
