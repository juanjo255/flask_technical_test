from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# conexion a postgress
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:5433/mydb"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class weatherModel(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    temp_hi = db.Column(db.Integer())
    temp_lo = db.Column(db.Integer())
    prcp = db.Column(db.Float())
    date = db.Column (db.Date())
    
    def __init__(self, city, temp_hi, temp_lo, prcp, date):
        self.city = city
        self.temp_hi = temp_hi
        self.temp_lo = temp_lo
        self.prcp = prcp
        self.date = date
        
    def __repr__(self):
        return f"<Car {self.name}>"

@app.route("/")
def index():
  return {"nombre":"juan"}

@app.route("/update", methods= ["POST"])
def update():
  print ("datos recibidos", request.get_data())
  return "enviado"


if __name__ == "__main__":
  app.run(debug=True)