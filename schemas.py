from pydantic import BaseModel, ConfigDict

class PaintingCreate(BaseModel):
    title: str
    artist: str
    price: float

class PaintingOut(BaseModel):
    title: str
    artist: str
    price: float

    model_config = ConfigDict(from_attributes=True)

class LikeResponse(BaseModel):
    message: str

class PaintingScore(BaseModel):
    title: str
    score: float

