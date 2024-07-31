from pydantic import BaseModel


class Features(BaseModel):
    dep_time: int
    arr_time: int
