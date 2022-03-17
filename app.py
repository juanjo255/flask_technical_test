from utils.fun import *
from flask import Flask, request
from models.models import *

app = Flask(__name__)

# debug para no tener que correr en cada cambio
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "secret"

#RUTAS
@app.route("/")
def index():
  return "<h1>HOLA, PARECE QUE YA FUNCIONO</h1>"

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
    token = request.headers.get("Authorization")
    userHospitalData = getTokenData(token)
    userDoctorData = request.get_json()
    
    if userHospitalData ["userType"].upper() == "HOSPITAL" and not ("" in userDoctorData.values()):
      if not(searchUser(userDoctorData)):
        addDoctorUser(userDoctorData)
        return "Doctor user created"
      
      return "doctor already registered"
    return "No authorized"

@app.route("/record/<identification>", methods=["POST"])
def createObservation (identification):
  if request.method == "POST":
    token = request.headers.get("Authorization")
    userDoctorData = getTokenData(token)
    if userDoctorData ["userType"].upper() == "DOCTOR":
      data = request.get_json()
      createRecord(identification, data)
      return "record created"
    return "No authorized"

if __name__ == "__main__":
  app.run(debug=True)