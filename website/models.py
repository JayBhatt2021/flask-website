"""Contains the User and Note database models."""
from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    """A data class that represents the user."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(127))
    notes = db.relationship("Note")


class Note(db.Model):
    """A data class that represents the note."""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(8191))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
