from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    EmailField,
)
from hamming_messages.models import User


class SignupForm(FlaskForm):
    """User signup form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Validate username is not taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different username."
            )

    def validate_email(self, email):
        """Validate email is not in use."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                """
                The email is already in use. Please enter a different email.
                Alternatively, if you forgot your password, go to the signin
                page and click \"Forgot Password\".
                """
            )


class SigninForm(FlaskForm):
    """User signin form."""

    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UpdateAccountForm(FlaskForm):
    """User update account form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """Validate username is not taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different username."
            )

    def validate_email(self, email):
        """Validate email is not in use."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                """
                    The email is already in use. Please enter a different email.
                    Alternatively, if you forgot your password, go to the signin
                    page and click \"Forgot Password\".
                    """
            )


class RequestResetForm(FlaskForm):
    """Request password reset form."""

    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """Validate email is associated with a user."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                """
                There is no account associated with that email.
                Please sign up for an account.
                """
            )


class ResetPasswordForm(FlaskForm):
    """Reset password form."""

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    submit = SubmitField("Reset Password")
