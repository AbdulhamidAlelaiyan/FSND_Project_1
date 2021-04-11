import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from flaskr.__init__ import QUESTIONS_PER_PAGE


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            os.environ.get('DATABASE_USER', ''),
            os.environ.get('DATABASE_PASSWORD', ''),
            os.environ.get('DATABASE_URL', 'localhost'),
            os.environ.get('DATABASE_PORT', '5432'),
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    # GET /categories
    def test_get_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertTrue(data["categories"])

    # GET /categories
    def test_get_categories_with_put_method(self):
        response = self.client().put("/categories")

        self.assertEqual(response.status_code, 405)

    # GET /questions
    def test_get_paginated_questions(self):
        response = self.client().get("/questions?page=1")
        data = json.loads(response.data)

        total_questions = QUESTIONS_PER_PAGE
        categories_total = len(Category.query.all())

        self.assertEqual(len(data["questions"]), 10)
        self.assertEqual(data["totalQuestions"], total_questions)
        self.assertEqual(len(data["categories"]), categories_total)
        self.assertTrue(data["currentCategory"])

    # GET /questions
    def test_get_paginated_questions_with_invalid_page_number(self):
        response = self.client().get("/questions?page=1000")

        self.assertEqual(response.status_code, 404)

    # DELETE /questions/<int:question_id>
    def test_delete_question(self):
        response = self.client().delete("/questions/11")

        self.assertEqual(response.status_code, 204)

    # DELETE /questions/<int:question_id>
    def test_delete_question_with_invalid_id(self):
        response = self.client().delete("/questions/1000")

        self.assertEqual(response.status_code, 404)

    # POST /questions
    def test_create_question(self):
        response = self.client().post(
            "/questions",
            json={
                "question": "What is my name?",
                "answer": "Abdulhamid",
                "difficulty": 4,
                "category": 1,
            },
        )

        self.assertEqual(response.status_code, 201)

    # POST /questions
    def test_create_question_with_no_question_key(self):
        response = self.client().post(
            "/questions",
            json={
                "answer": "Abdulhamid",
                "difficulty": 4,
                "category": 1})

        self.assertEqual(response.status_code, 400)

    # POST /questions
    def test_search_questions_with_results(self):
        response = self.client().post(
            "/questions",
            json={
                "searchTerm": "indian",
            },
        )
        data = json.loads(response.data)

        self.assertTrue(data["questions"])
        self.assertEqual(data["totalQuestions"], 1)
        self.assertTrue(data["currentCategory"])

    # POST /questions
    def test_search_questions_without_results(self):
        response = self.client().post(
            "/questions",
            json={
                "searchTerm": "north pole",
            },
        )
        data = json.loads(response.data)

        self.assertFalse(data["questions"])
        self.assertEqual(data["totalQuestions"], 0)
        self.assertTrue(data["currentCategory"])

    # GET /categories/<int:category_id>/questions
    def test_get_questions_by_category(self):
        response = self.client().get("/categories/1/questions")
        data = json.loads(response.data)

        self.assertTrue(data["questions"])
        self.assertEqual(data["totalQuestions"], len(data["questions"]))
        self.assertEqual(data["currentCategory"], 1)

    # GET /categories/<int:category_id>/questions
    def test_get_questions_by_invalid_category(self):
        response = self.client().get("/categories/9/questions")

        self.assertEqual(response.status_code, 404)

    # GET /quizzes
    def test_get_next_question(self):
        response = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {
                    "id": 1},
                "previous_questions": [17]})
        data = json.loads(response.data)

        self.assertTrue(data["question"])

    # GET /quizzes
    def test_get_next_question_with_invalid_category_id(self):
        response = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {
                    "id": 100},
                "previous_questions": [17]})
        data = json.loads(response.data)

        self.assertFalse(data["question"])

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and
    for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
