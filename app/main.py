from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Create app
app = FastAPI(
    title="JStar Astrology API",
    description="Calculate natal charts using Kerykeion",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}



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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#