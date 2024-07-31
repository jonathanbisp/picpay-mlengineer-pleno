from pydantic import BaseModel
import numpy as np


class LinRegWeights(BaseModel):
    coefficients: np.ndarray[np.float64]
    intercept: float

    class Config:
        arbitrary_types_allowed = True
