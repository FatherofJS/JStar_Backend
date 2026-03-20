from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Planet(BaseModel):
    id: str = ""
    name: str
    symbol: str
    longitude: float
    sign: str
    signDegree: float
    house: int
    speed: float = 0
    retrograde: bool = False


class House(BaseModel):
    id: int
    cusp: float
    sign: str
    signDegree: float
    size: float = 30


class Aspect(BaseModel):
    id: str = ""
    planet1: str
    planet2: str
    type: str
    angle: float
    orb: float
    applying: bool = False


class Angle(BaseModel):
    id: str = ""
    name: str
    longitude: float
    sign: str
    signDegree: float


class Subject(BaseModel):
    name: str
    birthDate: str
    birthTime: str
    location: str
    latitude: float
    longitude: float
    timezone: str = "UTC"


class ChartRequest(BaseModel):
    name: str
    date: str           # YYYY-MM-DD
    time: str           # HH:MM
    latitude: float
    longitude: float
    city: str = "Unknown"
    country: str = ""
    timezone: str = "UTC"


class ChartResponse(BaseModel):
    id: str
    timestamp: datetime
    subject: Subject
    planets: List[Planet]
    houses: List[House]
    aspects: List[Aspect]
    angles: List[Angle]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str = Field(..., max_length=500)
    chart_data: dict = Field(default_factory=dict, json_schema_extra={"example": {}})
    chart_type: str = "natal"
    history: List[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    tokens_used: int


class SynastryAspect(BaseModel):
    id: str = ""
    person1_planet: str
    person2_planet: str
    type: str
    angle: float
    orb: float

class SynastryRequest(BaseModel):
    person1: ChartRequest
    person2: ChartRequest

class SynastryResponse(BaseModel):
    id: str
    timestamp: datetime
    person1: Subject
    person2: Subject
    person1_planets: List[Planet]
    person2_planets: List[Planet]
    person1_houses: List[House]
    person2_houses: List[House]
    person1_angles: List[Angle]
    person2_angles: List[Angle]
    aspects: List[SynastryAspect]
