from flask import Flask, request
from models.models import *
from flask_migrate import Migrate

app = Flask(__name__)
# conexion a postgress
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:2020@localhost:5433/mydb"
# debug para no tener que correr en cada cambio
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/login", methods=["POST"])
def login():
  if request.method == "POST":
    data = request.get_json()
    print (data)
    if data and not ("" in data.values()):
      print (userModel.query.filter_by(identification=data[identification]) )
    return data


if __name__ == "__main__":
  app.run(debug=True)