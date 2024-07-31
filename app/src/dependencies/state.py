from fastapi import Request
from fastapi.datastructures import State


def get_state(request: Request) -> State:
    return request.app.state
