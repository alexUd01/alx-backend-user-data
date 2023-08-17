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
        assert resp.status_code == 200
        temp = resp.json()
        assert len(temp.keys()) == 2
        assert 'email' in temp.keys()
        assert 'message' in temp.keys()
        assert temp == {"email": email, "message": "user created"}


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
        assert len(resp.json().keys()) == 2
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
        assert len(resp.json().keys()) == 1
        assert 'email' in resp.json().keys()


def log_out(session_id: str) -> None:
    """ Test logout endpoint `DELETE /session` """
    if session_id:
        url = f'{HOST:s}:{PORT:d}/sessions'
        resp = requests.request('DELETE', url, allow_redirects=False,
                                cookies={'session_id': session_id})
        assert resp.ok
        assert resp.status_code == 302


def reset_password_token(email: str) -> str:
    """ Test `POST /reset_password` endpoint. """
    if email:
        url = f'{HOST:s}:{PORT:d}/reset_password'
        data = {'email': email}

        resp = requests.request('POST', url, data=data)

        assert resp.ok
        assert resp.status_code == 200
        temp = resp.json()
        assert len(temp.keys()) == 2
        assert 'email' in temp.keys()
        assert 'reset_token' in temp.keys()
        assert temp.get('email') == email
        return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test `PUT /update_password` endpoint. """
    if email and reset_token and new_password:
        url = f'{HOST:s}:{PORT:d}/reset_password'
        data = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
        resp = requests.request('PUT', url, data=data)
        assert resp.ok
        assert resp.status_code == 200
        temp = resp.json()
        assert len(temp.keys()) == 2
        assert 'email' in temp.keys()
        assert 'message' in temp.keys()
        assert temp.get('email') == email
        assert temp.get('message') == 'Password updated'


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
