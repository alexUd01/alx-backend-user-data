#!/usr/bin/env python3
"""
Basic authentication module that contains a class `BasicAuth` that
extends `api.v1.auth.auth.Auth`
"""
from .auth import Auth


class BasicAuth(Auth):
    """ A class that implements Basic Authentication """
    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        A method that returns the base64 part of the `Authorization` header
        for basic authentication
        """
        if authorization_header:
            if isinstance(authorization_header, str):
                if authorization_header.startswith('Basic '):
                    return authorization_header.split()[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """
        A method that returns the decoded value of a Base64 string stored
        in `base64_authorization_header` argument
        """
        from base64 import b64decode, binascii

        if base64_authorization_header:
            if isinstance(base64_authorization_header, str):
                try:
                    bin_val = b64decode(base64_authorization_header)
                except binascii.Error:
                    return None
                else:
                    str_val = bin_val.decode(encoding='utf-8')
                    return str_val
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        A method that returns the user email and password from the Base64
        decoded value
        """
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                if ":" in decoded_base64_authorization_header:
                    idx = decoded_base64_authorization_header.find(':')
                    u_email = decoded_base64_authorization_header[:idx]
                    u_passwd = decoded_base64_authorization_header[idx + 1:]
                    return u_email, u_passwd
        return None, None
