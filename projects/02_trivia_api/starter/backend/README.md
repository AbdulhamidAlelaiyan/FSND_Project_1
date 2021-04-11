# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export DATABASE_USER=
export DATABASE_PASSWORD=
export DATABASE_URL=localhost
export DATABASE_PORT=5432
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. ]

DATABASE_USER, DATABASE_PASSWORD, DATABASE_URL and DATABASE_PORT env variables should be set, if those env variables were not set then the default values will be used which are: localhost for DATABASE_URL and port 5432 for DATABASE_PORT and the rest of env variables will be empty.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

API Endpoints
```
GET '/categories'
- Fetches an object with categories key that refers to the list of categories
- Request Arguments: None
- Returns: An object with categories key that refers to the list of categories
- Sample `curl http://127.0.0.1:5000/categories`
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ]
}

GET '/questions'
- Fetches an object that contains a list of paginated questions, a list of categories, the number of questions in the list and the current category
- Request Arguments: page
- Returns: an object that contains a list of paginated questions, a list of categories, the number of questions in the list and the current category
- Sample: `curl http://127.0.0.1:5000/questions`
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "currentCategory": "Science", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "totalQuestions": 10
}

DELETE /questions/<int:question_id>
- Delete a question with a certain by id.
- Request Arguments: None
- Returns: HTTP Status code 204
- Sample: `curl -X DELETE -I http://127.0.0.1:5000/questions/10`
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Methods: *
Access-Control-Allow-Origin: *
Server: Werkzeug/0.15.5 Python/3.9.2
Date: Sat, 10 Apr 2021 23:01:51 GMT

POST /questions
- Create a question with question text, question answer, diffculty, and category or it can be used for searching questions by question text
- Request Arguments: None
- Returns: if used for creating questions and object with success key set to true and 201 http status code, if used for searching then an object with questions list that contains questions relevant to the search term and totalQuestions key that has the count of questions returned and the currentCategory.
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d "{
    \"question\": \"What is the capital city of KSA\", 
    \"answer\":\"Riyadh\",
    \"difficulty\": 3,
    \"category\": 3
}"`
{
  "success": true
}
- Another Sample:  `curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d "{
    \"search_term\": \"capital city of KSA\"
}"`
{
  "currentCategory": 1, 
  "questions": [
    {
      "answer": "Riyadh", 
      "category": 3, 
      "difficulty": 3, 
      "id": 24, 
      "question": "What is the capital city of KSA"
    }
  ], 
  "totalQuestions": 1
}

GET /categories/<int:category_id>/questions
- Fetches an object that contains questions key that has a list of question related to certain category supplied by category_id paramter and totalQuestions key contains the count of questions returned.
- Request Argument: None
- Returns: An object that contains questions key that has a list of question related to certain category supplied by category_id paramter and totalQuestions key contains the count of questions returned.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
{
  "currentCategory": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "totalQuestions": 3
}

POST /quizzes 
- Fetches a not repeated question from certain quiz category.
- Request Arguments: None
- Returns: An object with question key containing the question object
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -H 'Content-Type: application/json' -d "{\"quiz_category\": {\"id\": \"1\"}}"`
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```