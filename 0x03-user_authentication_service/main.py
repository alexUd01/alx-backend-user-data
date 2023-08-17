#!/usr/bin/env python3
"""
main - Integration tests module
"""
import requests

HOST = 'http://127.0.0.1'
PORT = 5000


def register_user(email: str, password: str) -> None:
    """ Test `POST /user` endpoint if it can register a new user """
    if email and password:
        data = {'email': email, 'password': password}
        resp = requests.post(f'{HOST:s}:{PORT:d}/users', data=data)
        assert resp.ok
        assert resp.json() == {"email": email, "message": "user created"}
        assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test `POST /sessions` endpoint if it rejects wrong password """
    if email and password:
        data = {'email': email, 'password': password}
        resp = requests.post(f'{HOST:s}:{PORT:d}/sessions', data=data)
        assert not resp.ok
        assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test `POST /sessions` endpoint if it accepts the correct password """
    if email and password:
        data = {'email': email, 'password': password}
        resp = requests.post(f'{HOST:s}:{PORT:d}/sessions', data=data)
        assert resp.ok
        assert resp.status_code == 200
        assert resp.json() == {'email': email, 'message': 'logged in'}
        return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Test `GET /profile` endpoint when not logged in."""
    resp = requests.get(f'{HOST:s}:{PORT:d}/profile')
    assert not resp.ok
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test `GET /profile` endpoint when logged in."""
    if session_id:
        url = f'{HOST:s}:{PORT:d}/profile'
        resp = requests.request('GET', url, cookies={'session_id': session_id})
        assert resp.ok
        assert resp.status_code == 200
        assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Test logout endpoint `DELETE /session` """
    if session_id:
        url = f'{HOST:s}:{PORT:d}/sessions'
        resp = requests.request('DELETE', url, allow_redirects=False,
                                cookies={'session_id': session_id})
        assert resp.ok
        assert resp.status_code == 302


def reset_password_token(email: str) -> str:
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
