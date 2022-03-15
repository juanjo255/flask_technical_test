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
migrate = Migrate()
migrate.init_app(app, db)

@app.route("/")
def index():
  return {"nombre":"juan"}

@app.route("/update", methods= ["POST"])
def update():
  print ("datos recibidos", request.get_data())
  return "enviado"

if __name__ == "__main__":
  app.run(debug=True)