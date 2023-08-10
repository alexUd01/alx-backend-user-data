#!/usr/bin/env python3
""" Documentation Here """
from models.base import Base


class UserSession(Base):
    """ UserSession class """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initializations """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    @property
    def user_id(self):
        """ `user_id` getter method """
        return self.user_id

    @user_id.setter
    def user_id(self, user_id):
        """ `use_id` setter method """
        self.user_id = user_id

    @property
    def session_id(self):
        """ `session_id` getter method """
        return self.session_id

    @session_id.setter
    def session_id(self, session_id):
        """ `session_id` getter method """
        self.session_id = session_id
