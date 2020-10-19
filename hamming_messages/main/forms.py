from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, SubmitField


class AddRoomForm(FlaskForm):
    """Add chat room form."""

    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=30)]
    )
    description = StringField(
        "Description", validators=[DataRequired(), Length(min=2, max=60)]
    )
    submit = SubmitField("Add Room")
