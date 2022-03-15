from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class userModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    cellphone = db.Column(db.Integer(), unique=True, nullable=False)
    password = db.Column (db.String(), nullable=False)
    userType= db.Column (db.String(), nullable=False)
    
    def __init__(self, identification, email, cellphone, password, userType):
        self.identification= identification
        self.email= email
        self.cellphone= cellphone
        self.password= password
        self.userType= userType
        
    def __repr__(self):
        return f"<User {self.identification}>"