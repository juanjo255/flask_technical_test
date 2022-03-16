from email.mime import base
from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine, DateTime
from sqlalchemy.orm import registry


engine = create_engine("postgresql://postgres:2020@localhost:5433/hospital")
# registry es un objeto que contiene la metadata
# esta metadata es toda la informacion de las tablas, ususarios y demas
# aqui se agrupan todas las clases y se saca la clase base
mapper_registry = registry()
# Todas las clases descienden de esta base
base = mapper_registry.generate_base()
# Los pasos de instaciar registry y sacar la clase base se pueden resumir a:
# base = declarative_base()
#db = SQLAlchemy()
class userModel(base):
    __tablename__ = 'users'
    
    #id = db.Column(db.Integer, primary_key=True)
    identification = Column(String, unique=True, nullable=False,primary_key=True)
    email = Column(String, unique=True, nullable=False)
    cellphone = Column(String, unique=True, nullable=False)
    password = Column (String, nullable=False)
    userType= Column (String, nullable=False)
    address= Column (String, nullable=False)
    
    def __init__(self, identification, email, cellphone, password, userType, address):
        self.identification= identification
        self.email= email
        self.cellphone= cellphone
        self.password= password
        self.userType= userType
        self.address= address
    
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
    
    specialty = Column (String)
    
    def __init__(self, identification, email, cellphone, password, userType, address, specialty):
        super().__init__(identification, email, cellphone, password, userType, address)
        self.service = specialty
    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }
mapper_registry.metadata.create_all(engine)
#print (list(mapper_registry.metadata.sorted_tables))