from pydantic import BaseModel


class DrawingPoint(BaseModel):
    x: float
    y: float


class CaertsianCoordinateColor(BaseModel):
    start: DrawingPoint
    end: DrawingPoint
    color: str


class QuestionGroup(BaseModel):
    name: str
    type_: str | None = None

    class Config:
        allow_population_by_field_name = True
        fields = {"type_": "type"}
