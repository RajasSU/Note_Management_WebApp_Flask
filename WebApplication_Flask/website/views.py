"""
The file contains the standard routes for our websites. Basically where users will navigate to.
E.g. Home page, About us Page
"""

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Now we need to define that this file is the blueprint of our applications (URLs, routes etc)
views = Blueprint('views', __name__)

# Define a route
@views.route('/', methods=['GET', 'POST'])
@login_required #Now we cannot go to homepage unless we are logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note= Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')

    return render_template("home.html", user=current_user) # using current_user we can reference the user in the template.


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note= json.loads(request.data) #We will receive the data in form of JSON object as we request it
    noteId= note['noteId'] # we need to access this noteID
    note= Note.query.get(noteId) #Look for the node that has an ID
    #Check if it exists
    if note:
        # Check if the user who is signed in owns the Note
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({}) #Return an empty response