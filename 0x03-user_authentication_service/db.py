#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict, Any

from user import Base, User

# `NoResultFound` has been moved from `sqlalchemy.orm.exc` to `sqlalchemy.exc`
# between the version 1.3.x and 1.4.x
try:
    from sqlalchemy.orm.exc import NoResultFound
except AttributeError:
    from sqlalchemy.exc import NoResultFound
finally:
    from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        A method that returns a new `User` object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """
        A method that returns the first row found in the `users` table
        as filtered by the method's input arguments.
        """
        user = self._session.query(User).filter_by(**kwargs).one()
        if user:
            return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
        A method that uses `find_user_by` to locate the users to update, then
        will update the user's attribute as passed in the method's arguments
        then commit changes to the database.
        """
        valid_attrs = ['id', 'email', 'hashed_password', 'session_id',
                       'reset_token']
        user = self.find_user_by(id=user_id)

        for k, v in kwargs.items():
            if k not in valid_attrs:
                raise ValueError
            setattr(user, k, v)

        self._session.commit()
