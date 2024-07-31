from fastapi import APIRouter, File, UploadFile, Depends
from services.models import model_predict, model_load, model_history
from dependencies.state import get_state
from dependencies.model import get_weights
from fastapi.exceptions import HTTPException
from fastapi.datastructures import State
from models.features import Features
from models.weights import LinRegWeights
from sqlite3 import Connection
from dependencies.sqlite import get_db

router = APIRouter(prefix="/model")


@router.post("/predict")
def predict(
    features: Features,
    weights: LinRegWeights | None = Depends(get_weights),
    db: Connection = Depends(get_db),
):
    if weights is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return model_predict(features, weights, db)


@router.post("/load")
def load(file: UploadFile = File(...), state: State = Depends(get_state)):
    return model_load(file, state)


@router.get("/history")
def history(db: Connection = Depends(get_db)):
    return model_history(db)
