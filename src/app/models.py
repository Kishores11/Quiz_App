from app import app
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)
app.app_context().push()


@dataclass
class User(db.Model):
    id: str = db.Column(db.Text, primary_key=True)
    name: str = db.Column(db.Text, nullable=False)
    email: str = db.Column(db.Text, nullable=False)

    @staticmethod
    def save_user_info(name, email, user_id):
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            user = User(id=user_id, name=name, email=email)
            db.session.add(user)
            db.session.commit()
        elif user.name != name or user.email != email:
            user.name = name
            user.email = email
            db.session.add(user)
            db.session.commit()


@dataclass
class Question(db.Model):
    id: str = db.Column(db.Text, primary_key=True)
    question: str = db.Column(db.Text, nullable=False)
    answer: str = db.Column(db.Text, nullable=False)
    created_by: User = db.Column(db.Text, db.ForeignKey("user.id"), nullable=False)
    updated_by: User = db.Column(db.Text, db.ForeignKey("user.id"), nullable=False)


@dataclass
class Quiz(db.Model):
    id = db.Column(db.Text, primary_key=True)
    quiz_name = db.Column(db.String(100), nullable=False)
    created_by: User = db.Column(db.Text, db.ForeignKey("user.id"), nullable=False)
    updated_by: User = db.Column(db.Text, db.ForeignKey("user.id"), nullable=False)


@dataclass
class QuizQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id: Quiz = db.Column(db.Text, db.ForeignKey("quiz.id"))
    question_id: Question = db.Column(db.Text, db.ForeignKey("question.id"))
