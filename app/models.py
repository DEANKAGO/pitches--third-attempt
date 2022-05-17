from datetime import datetime
from flask_login import UserMixin

from app import db,login_manager

@login_manager.user_loader
def login_manager(user_id):
  return User.query.get(int(user_id))

class User(db.Model,UserMixin):
  """
  """
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String,nullable=False,unique=True)
  phoneNumber=db.Column(db.String,nullable=False,unique=True)
  houseNumber=db.Column(db.String,nullable=False,unique=True)
  typeUser= db.Column(db.String,nullable=False) 
  email=db.Column(db.String,nullable=False,unique=True)
  password=db.Column(db.String,nullable=False)
  image_file=db.Column(db.String(20),nullable=False,default='default.png')
  post = db.relationship('Receipts', backref='author', lazy=True)

  def __repr__(self):
      return f"id: {self.id} , username: {self.username} , email: {self.email} "

class Receipts(db.Model):
  """
  """
  id=db.Column(db.Integer,primary_key=True)
  account_number=db.Column(db.String,nullable=False)
  amount=db.Column(db.String,nullable=False)
  receipt_image=db.Column(db.String,nullable=False,default='default.png')

  date_paid= db.Column(db.Date, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
  def __repr__(self):
      return f"id: {self.id} , title: {self.title}"



class Complaints(db.Model):
  """
  """
  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String,nullable=False)
  content=db.Column(db.String,nullable=False)
  date_created = db.Column(db.Date, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
  def __repr__(self):
      return f"id: {self.id} , title: {self.title}"