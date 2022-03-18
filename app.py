from sqlalchemy import update
from utils.fun import *
from flask import Flask, redirect, request, url_for
from flask_mail import Mail
from models.models import *

app = Flask(__name__)




# debug para no tener que correr en cada cambio
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "secret"
app.config['MAIL_SERVER']= "smtp.gmail.com"
app.config ['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME'] = 'juanjosepikon05@gmail.com'
app.config['MAIL_PASSWORD'] = "clave255"
app.config['MAIL_PORT'] = "587"

#inicializamos Mail para poder enviar correos
mail = Mail(app)

#RUTAS
@app.route("/")
def index():
  #token = generateTokenEmail({"email":"p@gmail.com"})
  # ENVIAR EMAIL de CONFIRMACION
  #sendEmail(mail, token)
  return "<h1> mi API </h1>"
  

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
        
        token = generateTokenEmail({"email":data["email"]})
        # ENVIAR EMAIL de CONFIRMACION
        sendEmail(mail, token, data["email"])
        res= "user created, check your email for account activation"
      return res
    return "Bad data"
  
@app.route("/login", methods=["POST"])
def login():
  data = request.get_json()
  result = searchUser(data)
  
  if result and request.method == "POST":
    
    res=""
    if result.password == data ["password"]:
      
      # Chekear si es el primer login del usuario doctor
      # si lo es debe cambiar contraseña
      if not(result.confirmed):
        return "You haven't confirmed your email"
      elif result.userType.upper() == "DOCTOR":
        if result.firstLogin:
          return redirect(url_for('changePassword', identification=result.identification))
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
    try:
      userHospitalData = decodeTokenData(token)
    except:
      return "TOKEN MISSING"
    
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
    try:
      userDoctorData = decodeTokenData(token)
    except: 
      return "TOKEN MISSING"
    
    if userDoctorData ["userType"].upper() == "DOCTOR":
      data = request.get_json()
      createRecord(identification, data)
      return "record created"
    return "No authorized"

@app.route("/changePassword", methods=["POST","GET"])
def changePassword():
  if request.method == "POST":
    psw= request.get_json()
    identification = request.args.get("identification")
    session= Session(engine)
    command= update(userModel).where(identification==userModel.identification).values({doctorUser.password:psw["password"], doctorUser.firstLogin:False})
    session.execute(command)
    session.commit()
    session.close()
    return "password changed"
  return "<h1> change password endpoint </h1>"

@app.route("/confirmation/<token>")
def confirmation(token):
  data = decodeTokenData(token)
  session= Session(engine)
  command= update(userModel).where(data["email"]==userModel.email).values(confirmed=True)
  session.execute(command)
  session.commit()
  session.close()
  return "<h1> YOUR ACCOUNT IS NOW ACTIVE </h1>"

if __name__ == "__main__":
  app.run(debug=True)