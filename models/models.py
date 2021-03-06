from datetime import datetime
from email.mime import base
from xmlrpc.client import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine, DateTime
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine("postgresql://alnhuxsolqytzh:6dcf58e023a0e79593f84235dbf078e875fdedf9f7acb6e4840e0b57e91fa940@ec2-3-222-204-187.compute-1.amazonaws.com:5432/dev2nagq33c5h0")
# registry es un objeto que contiene la metadata
# esta metadata es toda la informacion de las tablas, ususarios y demas
# aqui se agrupan todas las clases y se saca la clase base
mapper_registry = registry()

# Todas las clases descienden de esta base
base = mapper_registry.generate_base()
# Los pasos de instaciar registry y sacar la clase base se pueden resumir a:
# base = declarative_base()
class userModel(base):
    __tablename__ = 'users'
    
    #id = db.Column(db.Integer, primary_key=True)
    identification = Column(String, unique=True, nullable=False,primary_key=True)
    email = Column(String, unique=True, nullable=False)
    cellphone = Column(String, unique=True, nullable=False)
    password = Column (String, nullable=False)
    userType= Column (String, nullable=False)
    address= Column (String, nullable=False)
    confirmed = Column (Boolean)
    
    # determinar one to many relationship and reverse
    healthRecord= relationship("healthRecords", backref="users")
    
    def __init__(self, identification, email, cellphone, password, userType, address):
        self.identification= identification
        self.email= email
        self.cellphone= cellphone
        self.password= password
        self.userType= userType
        self.address= address
        self.confirmed= False
    
    __mapper_args__ = {
        'polymorphic_on': userType
    }
    
    def __repr__(self):
        return f"User {self.identification}"
class hospitalUser(userModel):
    
    service = Column (String)
    
    def __init__(self, identification, email, cellphone, password, userType, address, service):
        super().__init__(identification, email, cellphone, password, userType, address)
        self.service = service
    __mapper_args__ = {
        'polymorphic_identity': 'hospital'
    }
class patientUser(userModel):
    
    birth = Column(DateTime)
    
    def __init__(self, identification, email, cellphone, password, userType, address, birth):
        super().__init__(identification, email, cellphone, password, userType, address)
        self.birth = birth
    __mapper_args__= {
        'polymorphic_identity': 'patient'
    }
class doctorUser(userModel):
    
    specialty= Column (String)
    firstLogin= Column (Boolean)
    
    def __init__(self, identification, email, cellphone, password, userType, address, specialty):
        super().__init__(identification, email, cellphone, password, userType, address)
        self.specialty = specialty
        self.firstLogin= True
    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }
class healthRecords(base):
    __tablename__ = 'records'
    
    id = Column (Integer, primary_key=True)
    identification = Column (String, ForeignKey(userModel.identification))
    healthStatus= Column(String)
    observations= Column(String)
    specialty= Column(String)
    date = Column(DateTime)
    
    def __init__(self, identification ,healthStatus, observations, specialty) -> None:
        self.identification=identification
        self.healthStatus= healthStatus
        self.observations= observations
        self.specialty= specialty
        self.date= datetime.now()

mapper_registry.metadata.create_all(engine)
#print (list(mapper_registry.metadata.sorted_tables))