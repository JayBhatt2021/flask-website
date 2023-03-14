"""Contains the site blueprint."""
from json import loads

from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import current_user, login_required

from . import db
from .models import Note

# "site" corresponds to the Blueprint's name
# "__name__" helps locate the root path of the Blueprint
bp = Blueprint("site", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    """Displays the Home Page and allows users to add notes to it.

    :return: The rendered HTML of the Home Template.
    """

    if request.method == "POST":
        # Obtains the note from the Notes Form
        note_text = request.form["note"]

        # Adds a note to the Home Page if it isn't empty
        if len(note_text) == 0:
            flash("You cannot post an empty note!", category="error")
        else:
            flash("Note added!", category="success")
            new_note = Note(text=note_text, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return render_template("site/home.html", user=current_user)


@bp.route("/delete-note", methods=["POST"])
def delete_note():
    """Deletes the note if it belongs to the current user.

    :return: An empty JSON object.
    """

    # Receives the note JSON object from the deleteNote JS function and assigns
    # it to note_id
    note = loads(request.data)
    note_id = note["noteId"]

    # Queries the database for the note by the note ID
    queried_note = Note.query.get(note_id)

    # Deletes the intended note only if it was published by the current user
    if queried_note:
        if queried_note.user_id == current_user.id:
            db.session.delete(queried_note)
            db.session.commit()

    return jsonify({})
