from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# Form template for ./templates/generate.html
class generateForm(FlaskForm):
    pubKey = StringField('Public Key', validators=[DataRequired()])
    birthdayHash = StringField('birthdayHash', validators=[DataRequired()])
    birthday = PasswordField('Birthday', validators=[DataRequired()])
    secret = PasswordField('Secret', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Generate Smart Contract')

# Form template for ./templates/deploy.html
class deployForm(FlaskForm):
    txHash = StringField('Transaction Hash', validators=[DataRequired()])
    contractAddress = StringField('Contract Address', validators=[DataRequired()])
    submit = SubmitField('Continue to Verification')

# Form template for ./templates/verify
class verifyForm(FlaskForm):
    contractAddress = StringField('Contract Address', validators=[DataRequired()])
    deploymentHash = StringField('Deployment Hash', validators=[DataRequired()])
    verifyTxHash = StringField('Verification Tx Hash', validators=[DataRequired()])
    submit = SubmitField('Finish')