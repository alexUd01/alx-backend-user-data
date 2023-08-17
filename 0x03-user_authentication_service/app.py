#!/usr/bin/env python3
""" the app """
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index() -> str:
    """ Welcome page """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ Registers a new user """
    email = request.form.get('email')
    password = request.form.get('password')

    user = None
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify(
            {"email": user.email, "message": "user created"}
        )


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login page """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Logout function """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            redirect(url_for('index'))
    abort(403)


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    """ Profile function """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Reset user password """
    email = request.form.get('email')

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if email == user.email:
        reset_pass_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_pass_token})

    abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ Update the user password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
