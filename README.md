# Quiz_App

In this quiz app I created four models
1)User model - For storing user details
2)Questios model - For storing questions and answers.
3)Quiz model - For storing quiz names and information
4)Quiz Questions -This model will store all the questions that are allocated to quiz models.


Routes

1)http://127.0.0.1:5000/users - This shows all the users.
2)http://127.0.0.1:5000/questions, methods(GET) - This shows all the questions available in this model and also when we pass specific question id in the end point it returns only that question/.
3)http://127.0.0.1:5000/questions, methods(POST) - This route allows you to post question to the question model.We can also add multiple questions at a time by passing this as a list.
4)http://127.0.0.1:5000/questions, methods(DELETE) - This allows you to delete questions from the question table.You can pass the question id's in the form of list to delete multiple questions at a time.
5)http://127.0.0.1:5000/questions, methods(PUT) - This allows you to update questions from the question table.You can pass the question id's in the form of list to update multiple questions at a time by passing the required information in json format.
6)http://127.0.0.1:5000/create_quiz, methods=[POST] - This allows you to create quiz with id and quiz names.
7)http://127.0.0.1:5000/quiz_questions, methods[POST] - This allows to add questions to multiple quiz by mentioning multiple question ids to each quiz id in the list format.
Eg:
  {
    "id":"1",
    "quiz_questions":[
        "1","2","3"
    ]
  }
  
   In this the quiz with id 1 get allocated with question id's 1,2,3.
   
   Initially I created one json file(initial_load.json) where the data is present and user can work from that.
   Inorder to load that use command bin/load_initial_data.py
   
  After loading the data you can start the flask application by run.py command.
  

I tried to create a quiz instance but I don't know the correct way how to answer the questions and save the response via json format.


