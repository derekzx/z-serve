from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class generateForm(FlaskForm):
    pubKey = StringField('Public Key', validators=[DataRequired()])
    birthdayHash = StringField('birthdayHash', validators=[DataRequired()])
    birthday = PasswordField('Birthday (Format: dd/mm/yyyy)', validators=[DataRequired()])
    secret = PasswordField('Secret', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Generate Smart Contract')

class deployForm(FlaskForm):
    txHash = StringField('txHash', validators=[DataRequired()])
    contractAddress = StringField('contractAddress', validators=[DataRequired()])
    submit = SubmitField('Continue to Verification')