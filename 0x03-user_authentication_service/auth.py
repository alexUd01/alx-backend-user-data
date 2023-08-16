#!/usr/bin/env python3
""" auth module """
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User

salt = gensalt()


def _hash_password(password: str) -> bytes:
    """
    A method that returns a salted hash of the input password in bytes,
    hashed with `bcrypt.hashpw`.
    """
    passwd_hash = hashpw(password.encode(), salt)
    return passwd_hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Documentation
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            hashed_passwd = _hash_password(password)
            user = self._db.add_user(email, hashed_passwd)
            return user
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        A method that tries to locate the user by email. If it exists,
        checks the password with `bcrypt.checkpw`. If it matches return `True`.
        In any other case, return `False`.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        else:
            if checkpw(password.encode(), user.hashed_password):
                return True
        return False

    def _generate_uuid(self) -> str:
        """
        Generates a string representation of a new UUID using uuid module.
        """
        from uuid import uuid4
        return str(uuid4())

    def create_session(self, email: str) -> str:
        """
        A method that finds the user corresponding to the email, generates
        a new UUID and stores it in the database as the user’s session_id,
        then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        else:
            session_id = self._generate_uuid()
            user.session_id = session_id
            return session_id
        return None
