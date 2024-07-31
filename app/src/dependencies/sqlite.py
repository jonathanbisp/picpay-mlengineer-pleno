from fastapi import Request
from sqlite3 import Connection


def get_db(request: Request) -> Connection:
    try:
        return request.app.state.db
    except AttributeError:
        return None
