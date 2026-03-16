# Chart calculation route — POST /chart

import os
os.environ.setdefault("GEONAMES_USERNAME", "jstar_astrology")

from fastapi import APIRouter, HTTPException
from kerykeion import AstrologicalSubjectFactory, AspectsFactory
from datetime import datetime
import uuid

from ..models import (Planet, House, Aspect, Angle, Subject,
                      ChartRequest, ChartResponse,
                      SynastryRequest, SynastryResponse, SynastryAspect)

router = APIRouter()

# Kerykeion abbreviation → full sign name
SIGN_MAP = {
    "Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Can": "Cancer",
    "Leo": "Leo", "Vir": "Virgo", "Lib": "Libra", "Sco": "Scorpio",
    "Sag": "Sagittarius", "Cap": "Capricorn", "Aqu": "Aquarius", "Pis": "Pisces",
}

# Kerykeion house name → integer
HOUSE_MAP = {
    "First_House": 1, "Second_House": 2, "Third_House": 3,
    "Fourth_House": 4, "Fifth_House": 5, "Sixth_House": 6,
    "Seventh_House": 7, "Eighth_House": 8, "Ninth_House": 9,
    "Tenth_House": 10, "Eleventh_House": 11, "Twelfth_House": 12,
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def deg_to_sign(longitude: float) -> tuple[str, float]:
    """Convert absolute longitude to (sign_name, degree_within_sign)."""
    sign_index = int(longitude // 30)
    return SIGNS[sign_index], longitude % 30


@router.post("/chart", response_model=ChartResponse)
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
            tz_str=req.timezone,
        )

        # ── Planets ──
        planet_objects = [
            subject.sun, subject.moon, subject.mercury, subject.venus, subject.mars,
            subject.jupiter, subject.saturn, subject.uranus, subject.neptune, subject.pluto,
            subject.chiron, subject.true_south_lunar_node, subject.true_north_lunar_node,
        ]
        planets = [
            Planet(
                id=str(uuid.uuid4()),
                name=p.name,
                symbol=p.emoji,
                longitude=p.abs_pos,
                sign=SIGN_MAP.get(p.sign, p.sign),
                signDegree=p.position,
                house=HOUSE_MAP.get(p.house, 0),
                speed=p.speed,
                retrograde=p.retrograde,
            )
            for p in planet_objects
        ]

        # ── Houses ──
        kerykeion_houses = [
            subject.first_house, subject.second_house, subject.third_house,
            subject.fourth_house, subject.fifth_house, subject.sixth_house,
            subject.seventh_house, subject.eighth_house, subject.ninth_house,
            subject.tenth_house, subject.eleventh_house, subject.twelfth_house,
        ]
        houses = []
        for i, h in enumerate(kerykeion_houses):
            current_cusp = h.abs_pos
            next_cusp = kerykeion_houses[(i + 1) % 12].abs_pos
            size = (next_cusp - current_cusp) % 360
            houses.append(House(
                id=i + 1,
                cusp=current_cusp,
                sign=SIGN_MAP.get(h.sign, h.sign),
                signDegree=h.position,
                size=size,
            ))

        # ── Aspects ──
        natal_result = AspectsFactory.single_chart_aspects(subject)
        aspects = [
            Aspect(
                id=str(uuid.uuid4()),
                planet1=a.p1_name,
                planet2=a.p2_name,
                type=a.aspect,
                angle=360 - a.diff if a.diff > 180 else a.diff,
                orb=a.orbit,
                applying=(a.aspect_movement == "Applying"),
            )
            for a in natal_result.aspects
        ]

        # ── Angles ──
        angle_data = [
            ("ASC", subject.first_house.abs_pos),
            ("DSC", subject.seventh_house.abs_pos),
            ("MC", subject.tenth_house.abs_pos),
            ("IC", subject.fourth_house.abs_pos),
        ]
        angles = []
        for name, lng in angle_data:
            sign, sign_degree = deg_to_sign(lng)
            angles.append(Angle(
                id=str(uuid.uuid4()),
                name=name,
                longitude=lng,
                sign=sign,
                signDegree=sign_degree,
            ))

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
                timezone=req.timezone,
            ),
            planets=planets,
            houses=houses,
            aspects=aspects,
            angles=angles,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def _extract_chart_data(subject):
    """Extract planets, houses, and angles from a kerykeion subject."""
    planet_objects = [
        subject.sun, subject.moon, subject.mercury, subject.venus, subject.mars,
        subject.jupiter, subject.saturn, subject.uranus, subject.neptune,
        subject.pluto, subject.chiron,
        subject.true_south_lunar_node, subject.true_north_lunar_node,
    ]
    planets = [
        Planet(
            id=str(uuid.uuid4()),
            name=p.name,
            symbol=p.emoji,
            longitude=p.abs_pos,
            sign=SIGN_MAP.get(p.sign, p.sign),
            signDegree=p.position,
            house=HOUSE_MAP.get(p.house, 0),
            speed=p.speed,
            retrograde=p.retrograde,
        )
        for p in planet_objects
    ]

    kerykeion_houses = [
        subject.first_house, subject.second_house, subject.third_house,
        subject.fourth_house, subject.fifth_house, subject.sixth_house,
        subject.seventh_house, subject.eighth_house, subject.ninth_house,
        subject.tenth_house, subject.eleventh_house, subject.twelfth_house,
    ]
    houses = []
    for i, h in enumerate(kerykeion_houses):
        current_cusp = h.abs_pos
        next_cusp = kerykeion_houses[(i + 1) % 12].abs_pos
        size = (next_cusp - current_cusp) % 360
        houses.append(House(
            id=i + 1,
            cusp=current_cusp,
            sign=SIGN_MAP.get(h.sign, h.sign),
            signDegree=h.position,
            size=size,
        ))

    angle_data = [
        ("ASC", subject.first_house.abs_pos),
        ("DSC", subject.seventh_house.abs_pos),
        ("MC", subject.tenth_house.abs_pos),
        ("IC", subject.fourth_house.abs_pos),
    ]
    angles = []
    for name, lng in angle_data:
        sign, sign_degree = deg_to_sign(lng)
        angles.append(Angle(
            id=str(uuid.uuid4()),
            name=name,
            longitude=lng,
            sign=sign,
            signDegree=sign_degree,
        ))

    return planets, houses, angles


@router.post("/synastry", response_model=SynastryResponse)
def calculate_synastry(req: SynastryRequest):
    try:
        # -------- PERSON 1 --------
        subject1 = AstrologicalSubjectFactory.from_birth_data(
            name=req.person1.name,
            year=int(req.person1.date.split("-")[0]),
            month=int(req.person1.date.split("-")[1]),
            day=int(req.person1.date.split("-")[2]),
            hour=int(req.person1.time.split(":")[0]),
            minute=int(req.person1.time.split(":")[1]),
            city=req.person1.city,
            nation=req.person1.country,
            lat=req.person1.latitude,
            lng=req.person1.longitude,
            tz_str=req.person1.timezone,
        )
        planets1, houses1, angles1 = _extract_chart_data(subject1)

        # -------- PERSON 2 --------
        subject2 = AstrologicalSubjectFactory.from_birth_data(
            name=req.person2.name,
            year=int(req.person2.date.split("-")[0]),
            month=int(req.person2.date.split("-")[1]),
            day=int(req.person2.date.split("-")[2]),
            hour=int(req.person2.time.split(":")[0]),
            minute=int(req.person2.time.split(":")[1]),
            city=req.person2.city,
            nation=req.person2.country,
            lat=req.person2.latitude,
            lng=req.person2.longitude,
            tz_str=req.person2.timezone,
        )
        planets2, houses2, angles2 = _extract_chart_data(subject2)

        # -------- CROSS-CHART ASPECTS --------
        cross_result = AspectsFactory.synastry_aspects(subject1, subject2)
        aspects = [
            SynastryAspect(
                id=str(uuid.uuid4()),
                person1_planet=a.p1_name,
                person2_planet=a.p2_name,
                type=a.aspect,
                angle=360 - a.diff if a.diff > 180 else a.diff,
                orb=a.orbit,
            )
            for a in cross_result.aspects
        ]

        return SynastryResponse(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            person1=Subject(
                name=req.person1.name,
                birthDate=req.person1.date,
                birthTime=req.person1.time,
                location=f"{req.person1.city}, {req.person1.country}",
                latitude=req.person1.latitude,
                longitude=req.person1.longitude,
                timezone=req.person1.timezone,
            ),
            person2=Subject(
                name=req.person2.name,
                birthDate=req.person2.date,
                birthTime=req.person2.time,
                location=f"{req.person2.city}, {req.person2.country}",
                latitude=req.person2.latitude,
                longitude=req.person2.longitude,
                timezone=req.person2.timezone,
            ),
            person1_planets=planets1,
            person2_planets=planets2,
            person1_houses=houses1,
            person2_houses=houses2,
            person1_angles=angles1,
            person2_angles=angles2,
            aspects=aspects,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))