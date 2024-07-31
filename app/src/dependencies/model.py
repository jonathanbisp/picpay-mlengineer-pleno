from fastapi import Request
from models.weights import LinRegWeights


def get_weights(request: Request) -> LinRegWeights | None:
    try:
        return request.app.state.weights
    except AttributeError:
        return None
