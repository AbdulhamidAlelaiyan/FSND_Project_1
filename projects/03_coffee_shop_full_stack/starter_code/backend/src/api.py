import os
from flask import Flask, request, jsonify, abort, Response
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
"""
db_drop_and_create_all()

# ROUTES
"""
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json
    {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()
    return jsonify(
        {"drinks": [drink.short() for drink in drinks], "success": True}
    )


"""
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_details(*args):
    drinks = Drink.query.all()
    return jsonify(
        {"drinks": [drink.long() for drink in drinks], "success": True}
    )


"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {"success": True, "drinks": drink} where drink an array containing
    only the newly created drink
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(*args):
    data = request.get_json()
    if isinstance(data.get("recipe"), list):
        data_recipe = json.dumps(data["recipe"])
    else:
        data_recipe = json.dumps([data["recipe"]])

    new_drink = Drink(title=data["title"], recipe=data_recipe)
    new_drink.insert()

    return jsonify({"success": True, "drinks": new_drink.long()}), 200


"""
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {"success": True, "drinks": drink} where drink an array
    containing only the updated drink
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(*args, **kwargs):
    id = kwargs["id"]
    data = request.get_json()

    try:
        drink = Drink.query.filter_by(id=id).one()
    except BaseException:
        return abort(404)

    if data.get("title"):
        drink.title = data.get("title")

    if data.get("recipe"):
        drink.recipe = json.dumps(data.get("recipe"))

    drink.update()

    return jsonify(
        {
            "success": True,
            "drinks": [Drink.query.filter_by(id=id).one().long()],
        }
    )


"""
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json
    {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(*args, **kwargs):
    id = kwargs["id"]

    drink = Drink.query.filter_by(id=id).all()[0]
    drink.delete()

    return jsonify({"success": True, "delete": id})


# Error Handling
"""
Example error handling for unprocessable entity
"""
"""
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""
"""
@TODO implement error handler for AuthError
    error handler should conform to general task above
"""


@app.errorhandler(401)
def unauthenticated_access(error):
    return (
        jsonify(
            {"success": False, "error": 401, "message": "user unauthenticated"}
        ),
        401,
    )


@app.errorhandler(403)
def unauthorized_access(error):
    return (
        jsonify(
            {"success": False, "error": 403, "message": "user unauthorized"}
        ),
        403,
    )


"""
@TODO implement error handler for 404
    error handler should conform to general task above
"""


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {"success": False, "error": 404, "message": "resource not found"}
        ),
        404,
    )


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )


@app.errorhandler(500)
def unprocessable(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error",
            }
        ),
        500,
    )
