from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AnalyzeForm(FlaskForm):
    handle = StringField("Twitter Handle (no @):", validators=[DataRequired()])
    submit = SubmitField("Analyze!")
