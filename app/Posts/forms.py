from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField,DateField,IntegerField, BooleanField,TextAreaField,RadioField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime

class ReceiptForm(FlaskForm):
    """
    Args:
        FlaskForm (_type_): _description_
    """
    account_number=StringField('Account Number', validators=[DataRequired()])
    amount=IntegerField('Amount', validators=[DataRequired()])
    receipt_image= FileField('Receipt Image', validators=[FileAllowed(['jpg','png','svg','jpeg','gif'])])
    date_paid = DateField(' Date Paid', format = "%Y-%m-%d",default= datetime.utcnow)

    submit = SubmitField('Post Receipt')
    