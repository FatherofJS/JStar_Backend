from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from kerykeion import AstrologicalSubjectFactory, AspectsFactory
import uuid

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

@app.post("/chart", response_model=ChartResponse)
def calculate_chart(req: ChartRequest):
    try:
        subject = AstrologicalSubjectFactory.from_birth_data(
            name=req.name,
            year=int(req.date.split("-")[0]),
            month=int(req.date.split("-")[1]),
            day=int(req.date.split("-")[2]),
            hour=int(req.time.split(":")[0]),
            minute=int(req.time.split(":")[1]),
            city=req.city,
            nation=req.country,
            lat=req.latitude,
            lng=req.longitude,
            tz_str=req.timezone
        )
        planet_objects = [subject.sun,subject.moon,subject.mercury,subject.venus,subject.mars,
                          subject.jupiter,subject.saturn,subject.uranus,subject.neptune,subject.pluto]

        # -------- PLANETS --------
        house_map = {
            "First_House": 1, "Second_House": 2, "Third_House": 3,
            "Fourth_House": 4, "Fifth_House": 5, "Sixth_House": 6,
            "Seventh_House": 7, "Eighth_House": 8, "Ninth_House": 9,
            "Tenth_House": 10, "Eleventh_House": 11, "Twelfth_House": 12}
        planets = []
        for i, p in enumerate(planet_objects):
            planets.append(Planet(
                id = str(i),
                name=p.name,
                symbol=p.emoji,
                longitude=p.abs_pos,
                sign=p.sign,
                signDegree=p.position,
                house=house_map.get(p.house, 0),
                speed=p.speed,
                retrograde=p.retrograde))

        # -------- HOUSES --------
        houses = []
        kerykeion_houses = [subject.first_house, subject.second_house, subject.third_house,
                            subject.fourth_house, subject.fifth_house, subject.sixth_house,
                            subject.seventh_house, subject.eighth_house, subject.ninth_house,
                            subject.tenth_house, subject.eleventh_house, subject.twelfth_house,]

        for i, h in enumerate(kerykeion_houses):
            current_cusp = h.abs_pos
            next_cusp = kerykeion_houses[(i + 1) % 12].abs_pos
            size = (next_cusp - current_cusp) % 360
            houses.append(House(
                id=i + 1,
                cusp=current_cusp,
                sign=h.sign,
                signDegree=h.position,
                size=size
                ))

        # -------- ASPECTS --------
        natal_result = AspectsFactory.single_chart_aspects(subject)
        aspects = []
        for a in natal_result.aspects:
            aspects.append(Aspect(
                planet1=a.p1_name,
                planet2=a.p2_name,
                type=a.aspect,
                angle=a.aspect_degrees,
                orb=a.orbit,
                applying = (a.aspect_movement == "Applying")
                ))

        '''# -------- ANGLES --------
        angles = [Angle(
        name="Ascendant",
        longitude=subject.ascendant.position,
        sign=subject.ascendant.sign,
        signDegree=subject.ascendant.sign_pos),
        Angle(
        name="Midheaven",
        longitude=subject.midheaven.position,
        sign=subject.midheaven.sign,
        signDegree=subject.midheaven.sign_pos)]'''

        return ChartResponse(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            subject=Subject(
                name=req.name,
                birthDate=req.date,
                birthTime=req.time,
                location=f"{req.city}, {req.country}",
                latitude=req.latitude,
                longitude=req.longitude,
                timezone=req.timezone
            ),
            planets=planets,
            houses=houses,
            aspects=aspects,
            #angles=angles
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
