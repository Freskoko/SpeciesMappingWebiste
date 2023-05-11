from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects.postgresql import JSON
import secrets
import string

from mapping import plot_norway

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])  # Allow requests from the React app running on port 3000
#----------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.db'  # Use SQLite database file named words.db
db = SQLAlchemy(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    # location = db.Column(db.String, unique=True, nullable = False)
    longitude = db.Column(db.Float, nullable = True)
    latitude = db.Column(db.Float, nullable = True)

    
with app.app_context():
    db.create_all()

@app.route("/addanimal", methods=["POST"])
def addanimal():
    data = request.get_json()
    name = data.get("name")
    longitude = data.get("longitude")
    latitude = data.get("latitude")
    print(f"received animal {name}")

    new_word = Animal(name=name,longitude=longitude,latitude=latitude)
    db.session.add(new_word)
    db.session.commit() 

    return jsonify({"message": f"Animal {name} added successfully"}), 201


@app.route("/getanimal", methods=["GET"])
def getanimal():
    animal_name_user = request.args.get("name",None)

    if animal_name_user:
        animal_list = Animal.query.filter_by(name=animal_name_user).all()
    else:
        return jsonify({"animal_names":"None found"}), 201
    
    animal_names = [animal.name for animal in animal_list]

    print(animal_names)

    return jsonify({"animal_names":animal_names})

def random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.route("/update_animal_and_img",methods=["POST"])
def update_animal_and_img():
    data = request.get_json()
    animal_name_user = data.get("name")
    longitude = data.get("longitude")
    latitude = data.get("latitude")

    if not animal_name_user:
        return jsonify({"animal_names":"Not found"}), 404

    animal_from_db = Animal.query.filter_by(name=animal_name_user).all()

    

    



@app.route("/getmap_with_animal",methods=["GET"])
def getmap_with_animal():
    animal_name_user = request.args.get("name",None)

    if not animal_name_user:
        return jsonify({"animal_names":"Not found"}), 404
    
    animal_list = Animal.query.filter_by(name=animal_name_user).all()
    longs = [animal.longitude for animal in animal_list]
    lats = [animal.latitude for animal in animal_list]

    special_code = f"{random_string()}.png"

    plot_norway(lats,longs,special_code)

    return jsonify({"message": f"Animal {animal_name_user} mapped successfully with code {special_code}", "img_code":special_code}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the Flask app on port 5000


