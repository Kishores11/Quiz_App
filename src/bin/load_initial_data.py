#!/usr/bin/env python3
"""
does the inital load of db to get local host up and running
"""


import os
import sys
import json
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(parentdir)
sys.path.insert(0, parentdir)

from app import app, models
from app.models import User, Question, db


def create_object_in_db_at_startup(json_file_path):
    # Read the data from load.json
    with open(json_file_path) as file:
        data = json.load(file)

    # Iterate over the User objects and insert them into the database
    for user_data in data["User"]:
        existing_user = db.session.get(User, user_data["id"])
        if not existing_user:
            user = User(
                id=user_data["id"], name=user_data["name"], email=user_data["email"]
            )
            db.session.add(user)

    # Iterate over the Question objects and insert them into the database
    for question_data in data["Question"]:
        existing_question = db.session.get(Question, question_data["id"])
        if not existing_question:
            question = Question(
                id=question_data["id"],
                question=question_data["question"],
                answer=question_data["answer"],
                created_by=question_data["created_by"],
                updated_by=question_data["updated_by"],
            )
            db.session.add(question)

    # Commit the changes to the database
    db.session.commit()

    print("Data loaded successfully")


create_object_in_db_at_startup("bin/initial_data.json")
