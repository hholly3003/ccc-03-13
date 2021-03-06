from flask import Blueprint, abort, jsonify, request
from schemas.UserSchema import user_schema
from models.User import User
from main import db, bcrypt

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if user:
        return abort(400, description="Email already registered")
    
    user = User()
    user.email = user_fields["email"]
    #user.password = user_fields["password"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))

@auth.route("/login", methods=["POST"])
def auth_login():
    #check if we have the user in our database
    #if yes, compare the hash of password inputted with the one we have in database

    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort (401, description="Incorrect username and password")
    
    return "token"