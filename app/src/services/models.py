from fastapi import UploadFile
import joblib
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from datetime import datetime
from models.weights import LinRegWeights
from models.features import Features
import numpy as np
from fastapi.datastructures import State
from sqlite3 import Connection


def model_predict(
    features: Features, model: LinRegWeights, db: Connection
) -> JSONResponse:
    try:
        prediction: np.float64 = (
            np.dot(np.array([features.dep_time, features.arr_time]), model.coefficients)
            + model.intercept
        )
        db.execute(
            "INSERT INTO history (dep_time, arr_time, prediction) VALUES (?, ?, ?)",
            (features.dep_time, features.arr_time, float(prediction)),
        )
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting: {e}")

    return JSONResponse({"prediction": prediction}, status_code=200)


def model_load(file: UploadFile, state: State) -> JSONResponse:
    if not file.filename.endswith(".pkl") or file.filename is None:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .pkl files are allowed."
        )

    file_location = (
        f"./storage/{file.filename.split(".")[0]}_{datetime.now().timestamp()}.pkl"
    )
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    try:
        state.weights = LinRegWeights.model_validate(joblib.load(file_location))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {e}")

    return JSONResponse(
        {"info": f"Model '{file.filename}' uploaded and loaded successfully"},
        status_code=200,
    )


def model_history(db: Connection) -> JSONResponse:
    try:
        history = db.execute("SELECT * FROM history").fetchall()
        history = [
            {
                "id": row[0],
                "features": {"dep_time": row[1], "arr_time": row[2]},
                "prediction": row[3],
                "updated_at": row[4],
            }
            for row in history
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {e}")

    return JSONResponse({"history": history}, status_code=200)
