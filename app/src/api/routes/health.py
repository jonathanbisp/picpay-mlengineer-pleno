from fastapi import APIRouter, Depends
from services.models import model_predict
from dependencies.model import get_weights
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from models.weights import LinRegWeights
from sqlite3 import Connection
from dependencies.sqlite import get_db

router = APIRouter(prefix="/health")


@router.get("/")
def predict(
    weights: LinRegWeights | None = Depends(get_weights),
    db: Connection = Depends(get_db),
):
    db_status = db.execute("SELECT 1 FROM history").fetchone()
    if weights is None and db_status is None:
        raise HTTPException(status_code=500, detail="Model not loaded and no database")
    if weights is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    if db_status is None:
        raise HTTPException(status_code=500, detail="No database connected")

    return JSONResponse({"status": "ok"}, status_code=200)
