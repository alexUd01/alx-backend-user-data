#!/usr/bin/env python3
""" the app """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
