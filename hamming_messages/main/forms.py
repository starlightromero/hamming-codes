from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import StringField, SubmitField


class AddRoomForm(FlaskForm):
    """Add chat room form."""

    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Add Room")
