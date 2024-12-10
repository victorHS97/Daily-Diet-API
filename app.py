from flask import Flask, request, jsonify
from database import db
from models.user import User
from models.diets import Diets
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
login_manager.init_app(app)

# VIEW DE LOGIN
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


# ROTAS DE DIETAS


@app.route('/diet', methods=['POST'])
@login_required
def create_diet():
    data = request.json
    id = data.get("id")
    name = data.get("name")
    description = data.get("description")
    date_hour = data.get("Date/Hour")
    diet = data.get("diet")
    id_user = current_user.id
    diet = Diets(id=id, name=name, description=description,
                 date_hour=date_hour, diet=diet, id_user=id_user)
    db.session.add(diet)
    db.session.commit()
    return jsonify({"message": "Dieta cadastrada com sucesso"})


@app.route('/diet/<int:id_diet>', methods=['PUT'])
@login_required
def update_diet_user(id_diet):
    id_user = current_user.id
    diets = db.session.query(Diets).filter(Diets.id_user == id_user).all()
    data = request.json
    for d in diets:
        if d.id == id_diet:
            d.name = data.get("name")
            d.description = data.get("description")
            d.date_hour = data.get("Date/Hour")
            d.diet = data.get("diet")
            db.session.commit()
            return jsonify({"message": "Dieta atualizada com sucesso"})

    return jsonify({"message": "Dieta não encontrada"}), 404


@app.route('/diet', methods=['GET'])
@login_required
def read_diets_user():
    id_user = current_user.id
    diet_list = []
    diets = db.session.query(Diets).filter(Diets.id_user == id_user).all()
    if diets:
        for d in diets:
            output = {
                "id": d.id,
                "name": d.name,
                "description": d.description,
                "date_hour": d.date_hour,
                "diet": d.diet
            }
            diet_list.append(output)
        return jsonify(diet_list)
    return jsonify({"message": "Nenhuma dieta encontrada"}), 404


@app.route('/diet/<int:id_diet>', methods=['GET'])
@login_required
def read_diet_user(id_diet):  # ROTA PARA EXIBIR UMA UNICA DIETA
    id_user = current_user.id
    diets = db.session.query(Diets).filter(Diets.id_user == id_user).all()
    for d in diets:
        if d.id == id_diet:
            output = {
                "id": d.id,
                "name": d.name,
                "description": d.description,
                "date_hour": d.date_hour,
                "diet": d.diet
            }
            return jsonify(output)
    return jsonify({"message": "Dieta não encontrada"}), 404


@app.route('/diet/<int:id_diet>', methods=['DELETE'])
@login_required
def delete_diet_user(id_diet):
    id_user = current_user.id
    diets = db.session.query(Diets).filter(Diets.id_user == id_user).all()
    for d in diets:
        if d.id == id_diet:
            db.session.delete(d)
            db.session.commit()
            return jsonify({"message": "Dieta deletada com sucesso"})
    return jsonify({"message": "Dieta não encontrada"}), 404

# ROTAS DE USUARIO


@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    if data:
        id = data.get("id")
        name = data.get("name")
        password = data.get("password")
        user = User(id=id, name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})
    return jsonify({"message": "Dados invalidos para cadastro"}), 400


@app.route('/user', methods=['PUT'])
@login_required
def update_user():
    id_user = current_user.id
    user = db.session.query(User).filter(User.id == id_user).first()
    data = request.json
    if user and data:
        user.password = data.get("password")
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso"})
    return jsonify({"message": "Dados invalidos"}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:
        user = db.session.query(User).filter(User.name == username).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Usuário logado com sucesso"})
    return jsonify({"message": "Dados invalidos"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Usuário deslogado com sucesso"})


if __name__ == '__main__':
    app.run(debug=True)
