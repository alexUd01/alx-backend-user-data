#!/usr/bin/env python3
""" auth module """
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from uuid import uuid4
from typing import Union

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
        if not email:
            pass  # NOTE: Dont know what to do
        if not password:
            pass  # NOTE: Dont know what to do
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
        if not email:
            return False
        if not password:
            return False
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
        u_id = uuid4()
        return str(u_id)

    def create_session(self, email: str) -> str:
        """
        A method that finds the user corresponding to the email, generates
        a new UUID and stores it in the database as the user’s session_id,
        then return the session ID.
        """
        if not email:
            return
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        else:
            session_id = self._generate_uuid()
            user.session_id = session_id
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        If the session ID is None or no user is found, return None. Otherwise
        return the corresponding user
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
            except Exception:
                return None
            else:
                return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """
        A method that updates the dorresponding user's session id to None
        """
        if user_id:
            try:
                user = self._db.find_user_by(id=user_id)
            except Exception:
                return None
            else:
                user.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        A method that find the user corresponding to the email. If the user
        does not exist, raise a ValueError exception. If it exists, generate
        a UUID and update the user’s reset_token database field. Return the
        token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        else:
            user.reset_token = self._generate_uuid()
            return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Use the `reset_token` to find the corresponding user. If it does not
        exist, raise a `ValueError` exception.

        Otherwise, hash the password and update the user’s `hashed_password`
        field with the new hashed password and the `reset_token` field to None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
