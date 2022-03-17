from models.models import *
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt
import os


def searchUser(data):
  sqlcommand= select(userModel).where(userModel.identification == data["identification"] )
  session = Session(engine)
  result = session.scalars(sqlcommand).first()
  session.close()
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

def getTokenData(token):
  userData = jwt.decode(token, os.environ.get("SECRET_KEY_TOKEN") ,algorithms=["HS256"])
  return userData