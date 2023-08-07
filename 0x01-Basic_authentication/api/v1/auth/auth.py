#!/usr/bin/env python3
""" Base class for all auth instances """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class Auth """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Doc here """
        if path is None or excluded_paths is None:
            return True
        if path.rstrip('/') not in list(map(lambda x: x.rstrip('/'),
                                            excluded_paths)):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Doc here """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Doc here """
        return None
