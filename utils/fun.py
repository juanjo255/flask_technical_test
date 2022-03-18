from models.models import *
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask_mail import Message
#from smtplib import SMTP
import jwt
import os

def searchUser(data):
  sqlcommand= select(userModel).where(userModel.identification == data["identification"] )
  session = Session(engine)
  result = session.scalars(sqlcommand).first()
  return result

def createHospitalUser(data):
  session = Session(engine)
  user = hospitalUser(data["identification"], data["email"], data["cellphone"], data["password"], data["userType"],data["address"], data["service"])
  session.add(user)
  session.commit()
  session.close()
  return "done"
  
def createPatienteUser(data):
  session = Session(engine)
  user = patientUser(data["identification"], data["email"], data["cellphone"], data["password"], data["userType"],data["address"], data["birth"])
  session.add(user)
  session.commit()
  session.close()
  return "done"

def addDoctorUser(data):
  
  session= Session(engine)
  user= doctorUser(data["identification"], data["email"], data["cellphone"], data["password"], data["userType"],data["address"], data["specialty"])
  session.add(user)
  session.commit()
  session.close()
  return "done"

def createRecord(identification, data):
  session= Session(engine)
  user= healthRecords(identification, data["healthStatus"], data["observations"], data["specialty"])
  session.add(user)
  session.commit()
  session.close()

def decodeTokenData(token):
  userData = jwt.decode(token, "secret" ,algorithms=["HS256"])
  return userData

def generateTokenEmail(email):
  token = jwt.encode(email, "secret" ,algorithm="HS256")
  return token

def sendEmail(mail, token, recipients):
  msg = Message("Account activation",
                sender="juanjosepikon05@gmail.com",
                recipients=[recipients])
  msg.html = f"<button><a href= 'http://localhost:5000/confirmation/{token}'> ACTIVATE ACCOUNT </a> <button>"
  mail.send(msg)
  # server = SMTP("smtp.gmail.com",587)
  # server.starttls()
  # server.login("juanjosepikon05@gmail.com", "clave255")
  # server.sendmail("juanjosepikon05@gmail.com","juanjosepikon05@gmail.com", "hola")