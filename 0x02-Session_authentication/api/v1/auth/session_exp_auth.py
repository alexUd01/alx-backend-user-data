#!/usr/bin/env python3
"""
Session authentication module that contains a class `SessionExpAuth` that
extends `api.v1.auth.auth.SessionAuth`
"""
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ A class that implements an expirable session. """
    def __init__(self):
        """ Initialization """
