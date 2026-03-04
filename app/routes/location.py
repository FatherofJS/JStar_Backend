
from fastapi import APIRouter, Query
import httpx
from timezonefinder import TimezoneFinder

router = APIRouter(prefix="/api/location")

tf = TimezoneFinder()
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {"User-Agent": "JStar-Astrology/1.0"}


@router.get("/search")
async def search_locations(q: str = Query(..., min_length=2), limit: int = Query(5, le=10)):
    """Search for cities using Nominatim geocoding API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(NOMINATIM_URL, params={
                "q": q,
                "format": "json",
                "limit": limit,
                "addressdetails": 1,
                "featuretype": "city",
            }, headers=NOMINATIM_HEADERS, timeout=10)
            resp.raise_for_status()
            results = resp.json()

        data = []
        for r in results:
            lat = float(r.get("lat", 0))
            lon = float(r.get("lon", 0))
            addr = r.get("address", {})
            tz = tf.timezone_at(lat=lat, lng=lon) or "UTC"

            data.append({
                "id": str(r.get("place_id", "")),
                "name": addr.get("city") or addr.get("town") or addr.get("village") or r.get("display_name", "").split(",")[0],
                "latitude": lat,
                "longitude": lon,
                "display_name": r.get("display_name", ""),
                "country_code": addr.get("country_code", "").upper(),
                "country": addr.get("country", ""),
                "administrative_area": addr.get("state") or addr.get("region") or "",
                "timezone": tz,
            })

        return {"success": True, "data": data}

    except httpx.HTTPError as e:
        return {"success": False, "data": [], "error": str(e)}


@router.get("/search-countries")
async def search_countries(q: str = Query(..., min_length=2), limit: int = Query(5, le=10)):
    """Search for countries using Nominatim."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(NOMINATIM_URL, params={
                "q": q,
                "format": "json",
                "limit": limit,
                "addressdetails": 1,
                "featuretype": "country",
            }, headers=NOMINATIM_HEADERS, timeout=10)
            resp.raise_for_status()
            results = resp.json()

        data = []
        for r in results:
            lat = float(r.get("lat", 0))
            lon = float(r.get("lon", 0))
            addr = r.get("address", {})

            data.append({
                "id": str(r.get("place_id", "")),
                "name": addr.get("country", r.get("display_name", "").split(",")[0]),
                "latitude": lat,
                "longitude": lon,
                "display_name": r.get("display_name", ""),
                "country_code": addr.get("country_code", "").upper(),
                "country": addr.get("country", ""),
                "administrative_area": "",
                "timezone": tf.timezone_at(lat=lat, lng=lon) or "UTC",
            })

        return {"success": True, "data": data}

    except httpx.HTTPError as e:
        return {"success": False, "data": [], "error": str(e)}
