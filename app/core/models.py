from pydantic import BaseModel


class DrawingPoint(BaseModel):
    x: float
    y: float


class CaertsianCoordinateColor(BaseModel):
    start: DrawingPoint
    end: DrawingPoint
    color: str
