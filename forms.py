from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import NumberRange, DataRequired


class ServerSettingsForm(FlaskForm):
    ram_critical = FloatField('ram', validators=[NumberRange(min=10, max=99), DataRequired()])
    cpu_critical = FloatField('cpu', validators=[NumberRange(min=10, max=99), DataRequired()])
    submit = SubmitField('Сохранить')
