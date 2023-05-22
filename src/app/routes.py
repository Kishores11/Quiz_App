from flask import request, jsonify
from app import app
from app.models import User, Question, Quiz, QuizQuestions, db
from sqlalchemy import delete, func
from sqlalchemy.exc import SQLAlchemyError, DataError, IntegrityError



@app.errorhandler(SQLAlchemyError)
def handle_scheduler_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": f"{e.orig}"}, 400


@app.route("/users", methods=["GET"])
def list_all_users():
    users = User.query
    users = users.paginate(page=1, per_page=13, error_out=False)
    return {
        "success":True,
        "users": users.items,
        "currentPage": users.page,
        "totalPages": users.pages,
        "totalCount": users.total,

    }


# @app.route('/users', methods=['POST'])
# def add_users():
#     user_id = request.json.get('user_id')
#     name = request.json.get('name')
#     email = request.json.get('email')
#     User.save_user_info(name,email,user_id)
#     return "success"
    

@app.route('/questions', methods=["GET"])
@app.route('/questions/<question_id>', methods=["GET"])
def list_all_questions(question_id=None):

    questions = Question.query

    if question_id:
        questions = questions.filter(
            Question.id == question_id
        )
        if questions.first() is None:
            return {"success": False, "message": " No such Question ID"}

    questions = questions.paginate(page=1,per_page=13, error_out=False)
    return {
        "success":True,
        "questions": questions.items,
        "currentPage": questions.page,
        "totalPages": questions.pages,
        "totalCount": questions.total,
    }


@app.route("/questions", methods=["POST"])
def add_questions():
    try:
        # Extract JSON data from the request body
        json_source = request.get_json()

        # Get the list of existing id from the database
        existing_id = {
            id[0]
            for id in Question.query.with_entities(
                Question.id
            ).all()
        }

        # Perform the bulk insert
        new_users = []
        for record in json_source:
            id = record["id"]

            # Check if the id already exists in the database
            if id not in existing_id:
                question = record["question"]
                answer = record["answer"]
                created_by = record["created_by"]
                updated_by = record["updated_by"]

                # Create a new User object and add it to the session
                questions = Question(
                    id=id,
                    question=question,
                    answer=answer,
                    created_by=created_by,
                    updated_by=updated_by,
                )
                new_users.append(questions)
                existing_id.add(id)

            else:
                return jsonify({"error": " Question ID already present"})
        db.session.add_all(new_users)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Questions insert successfully", "success": True})
    except Exception as e:
        return jsonify({"error"})
    


@app.route("/questions", methods=["PUT"])
def update_questions():
    try:
        # Extract JSON data from the request body
        json_data = request.get_json()

        # Get the list of existing names from the database
        existing_id = {
            id[0] for id in Question.query.with_entities(Question.id).all()
        }

        # Perform the bulk update
        for record in json_data:
            id = record["id"]

            # Check if the name already exists in the database
            if id in existing_id:
                question = Question.query.filter_by(id=id).first()
                question.question = record.get("question",question.question)
                question.answer = record.get("answer",question.answer)
                db.session.add(question)

        db.session.commit()
        return jsonify({"message": "Bulk update successful"})
    except Exception as e:
        return jsonify({"error"})



@app.route("/questions", methods=["DELETE"])
@app.route("/questions/<question_id>", methods=["DELETE"])
def delete_questions(question_id=None):
    questions = Question.query
    ids = request.json.get("ids")

    if question_id:
        ids = [id]
    else:
        ids = ids

    ids = [(id) for id in ids]
    questions = questions.filter(Question.id.in_(ids)).all()
    if ids:
        ids = [question.id for question in questions]
        statement = delete(Question).where(
            Question.id.in_(ids)
        )
        db.session.execute(statement)
        db.session.commit()
        return {
            "success": True,
            "Question": ids,
            "message": f"deleted questions with ids '{ids}'",
        }
    else:
        raise  handle_scheduler_exception(DataError)


@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    try:
        # Extract JSON data from the request body
        json_source = request.get_json()

        # Get the list of existing id from the database
        existing_id = {
            id[0]
            for id in Question.query.with_entities(
                Question.id
            ).all()
        }

        # Perform the bulk insert
        new_users = []
        for record in json_source:
            quiz_id = record["quiz_id"]

            # Check if the id already exists in the database
            if id not in existing_id:
                quiz_name = record["quiz_name"]
                created_by = record["created_by"]
                updated_by = record["updated_by"]

                # Create a new User object and add it to the session
                quiz = Quiz(
                    quiz_id=quiz_id,
                    quiz_name=quiz_name,
                    created_by=created_by,
                    updated_by=updated_by,
                )
                new_users.append(quiz)
                existing_id.add(quiz_id)

            else:
                return jsonify({"error": " Quiz ID already present"})
        db.session.add_all(new_users)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Quizes inserted successfully", "success": True})
    except Exception as e:
        return jsonify({"error"})
    

@app.route('/quiz_questions', methods=['POST'])
def quiz_questions():
    try:
        id = request.json.get('id')
        quiz_id = request.json.get('quiz_id')
        quiz_data = Quiz.query
        if quiz_id:
            quiz = quiz_data.filter(
                Quiz.quiz_id == quiz_id
            )
            if quiz.first() is None:
                return {"success": False, "message": " No such Quiz ID"}
        
        for i in request.json['question_id']:           
            p = QuizQuestions(id=id,quiz_id=quiz_id, question_id=i)
            db.session.add(p)
            
            db.session.commit()
            return  {"message": 'Questiond Quiz created successfully'}, 200
    except:
        return{
            "success":False,
            "message": "No questions added"
        }
