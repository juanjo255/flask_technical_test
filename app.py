from email import header
from utils.fun import *
from flask import Flask, request
from models.models import *
import jwt

app = Flask(__name__)
# conexion a postgress
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:2020@localhost:5433/hospital"
# debug para no tener que correr en cada cambio
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ruta de registro de usuarios
# def searchUser(data):
#   data = request.get_json()
#   sqlcommand= select(userModel).where(userModel.identification == data["identification"] )
#   session = Session(engine)
#   result = session.scalars(sqlcommand).first()

@app.route("/register", methods=["POST"])
def register():
  if request.method == "POST":
    data = request.get_json()
    print (data["identification"])
    
    #revisar que no este vacio, que no hayan campos vacios y, en el caso del tipo de usuario, sean valores correctos
    if data and not ("" in data.values()) and data ["userType"].upper() in ["HOSPITAL", "PATIENT"]:
      result = searchUser(data)
      res = ""
      if result:
        res= "user already registered"
      # dado que no este registrado el usuario, lo agregamos dependiendo de que tipo de usuario es
      # PATIENT / HOSPITAL
      else:
        if data["userType"].upper() == "HOSPITAL":  
          createHospitalUser(data)
        else:
          createPatienteUser(data)
        res= "user created"
      return res
    return "Bad data"
  
@app.route("/login")
def login():
  data = request.get_json()
  result = searchUser(data)
  if result:
    res=""
    if result.password == data ["password"]:
      res = "user approved"
    else:
      res = "wrong password"
    return res
  else:
    return "user no registered - redirect"

@app.route("/create-doctor", methods=["POST"])
def createDoctorUser():
  if request.method == "POST":
    header = request.headers.get("Authorization")
    data = jwt.decode(header, "secret" ,algorithms=["HS256"])
    if data ["userType"].upper() == "HOSPITAL" and data and not ("" in data.values()):
      if not(searchUser(data)):
        createDoctorUser(data)
        return "Doctor user created"
      
      return "doctor already registered"
    return "No authorized"

if __name__ == "__main__":
  app.run(debug=True)