import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', '*')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [c.format()['type'] for c in categories]


    return jsonify({
      'categories': formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)

    questions = Question.query.limit(QUESTIONS_PER_PAGE).offset(QUESTIONS_PER_PAGE * (page - 1)).all()
    if len(questions) == 0:
      return abort(404)
    
    formatted_questions = [q.format() for q in questions]

    categories = Category.query.all()
    formatted_categories = [c.format()['type'] for c in categories]



    return jsonify({
      'questions': formatted_questions, 
      'totalQuestions': len(questions),
      'categories': formatted_categories,
      'currentCategory': categories[0].format()['type']
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).all()
    if not question:
      return abort(404)
    question = question[0]
    question.delete()

    
    return Response(status=204)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_post():
    data = request.get_json()
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    if data.get('searchTerm'):
      results = Question.query.filter(Question.question.ilike(f"%{data['searchTerm']}%")).all()
      return jsonify({
        'questions': [q.format() for q in results],
        'totalQuestions': len(results),
        'currentCategory': 1,
      })
    else:  
      try:
        question = Question(question=data['question'], answer=data['answer'], difficulty=data['difficulty'], category=data['category'])
        question.insert()

        return jsonify({
          'success': True
        }), 201
      except:
        return  Response(status=400)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    questions_formatted = [q.format() for q in questions]

    if questions:
      return jsonify({
        'questions': questions_formatted,
        'totalQuestions': len(questions_formatted),
        'currentCategory': Category.query.filter_by(id=category_id).all()[0].format()['id']
      })
    else:
      return abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    try:
      data_set = set(data['previous_questions'])
      available_questions_ids = {q.id for q in Question.query.filter_by(category=data['quiz_category']['id']).all()}
      available_questions_ids.difference_update(data_set)

      next_question = Question.query.filter_by(id=list(available_questions_ids)[0]).all()[0].format()

      return jsonify({
        'question': next_question
      })
    except:
      return jsonify({
        'question': False
      })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return Response(status=404)

  @app.errorhandler(405)
  def not_found(error):
    return Response(status=405)

  @app.errorhandler(422)
  def unproccessable(error):
    return Response(status=422)

  
  return app

    