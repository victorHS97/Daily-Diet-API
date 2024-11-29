from database import db


class Diets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date_hour = db.Column(db.String(80), nullable=False)
    diet = db.Column(db.String(80), nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
