"""Geocode addresses for China-first map display (Amap > Google > Nominatim)."""

from __future__ import annotations

import logging
import os
import urllib.parse

import httpx

from app.core.state import MapLocation

logger = logging.getLogger(__name__)

_USER_AGENT = "police-pre-reception/0.1 (campus demo; contact=local-dev)"

_PROVIDER_LABELS = {
    "amap": "高德地图",
    "google": "Google 地图",
    "nominatim": "OpenStreetMap（备用）",
}


def _geocoding_enabled() -> bool:
    if os.getenv("PYTEST_CURRENT_TEST"):
        return False
    return os.getenv("MAP_GEOCODING_ENABLED", "true").lower() not in {"0", "false", "no"}


def _default_region() -> str:
    return os.getenv("MAP_DEFAULT_REGION", "").strip()


def _amap_api_key() -> str:
    return os.getenv("AMAP_API_KEY", "").strip()


def _amap_web_key() -> str:
    return os.getenv("AMAP_WEB_KEY", "").strip() or _amap_api_key()


def _google_api_key() -> str:
    return os.getenv("GOOGLE_MAPS_API_KEY", "").strip()


def resolve_map_provider() -> tuple[str, str]:
    """Return (provider_id, human-readable label)."""
    if _amap_api_key():
        return "amap", _PROVIDER_LABELS["amap"]
    if _google_api_key():
        return "google", _PROVIDER_LABELS["google"]
    return "nominatim", _PROVIDER_LABELS["nominatim"]


def _with_region_bias(query: str) -> str:
    region = _default_region()
    if not region:
        return query
    if region in query:
        return query
    return f"{region} {query}"


def _amap_map_link(lng: float, lat: float, label: str) -> str:
    name = urllib.parse.quote(label)
    return f"https://uri.amap.com/marker?position={lng},{lat}&name={name}"


def _google_maps_link(lat: float, lng: float, label: str) -> str:
    encoded = urllib.parse.quote(f"{label}@{lat},{lng}")
    return f"https://www.google.com/maps/search/?api=1&query={encoded}"


def _geocode_amap(query: str, api_key: str) -> MapLocation | None:
    params: dict[str, str] = {
        "key": api_key,
        "address": query,
    }
    city = os.getenv("MAP_AMAP_CITY", "").strip() or _default_region()
    if city:
        params["city"] = city

    try:
        response = httpx.get(
            "https://restapi.amap.com/v3/geocode/geo",
            params=params,
            timeout=8.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Amap geocoding failed for %r: %s", query, exc)
        return None

    if payload.get("status") != "1":
        return None

    geocodes = payload.get("geocodes") or []
    if not geocodes:
        return None

    top = geocodes[0]
    location = top.get("location", "")
    if not location or "," not in location:
        return None

    lng_str, lat_str = location.split(",", 1)
    display = top.get("formatted_address") or query
    lng_f = float(lng_str)
    lat_f = float(lat_str)

    return MapLocation(
        query=query,
        display_name=display,
        lat=lat_f,
        lng=lng_f,
        source="amap",
        map_url=_amap_map_link(lng_f, lat_f, display),
    )


def _geocode_google(query: str, api_key: str) -> MapLocation | None:
    params = {
        "address": query,
        "key": api_key,
        "language": "zh-CN",
        "region": "cn",
    }

    try:
        response = httpx.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params=params,
            timeout=8.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Google geocoding failed for %r: %s", query, exc)
        return None

    results = payload.get("results") or []
    if payload.get("status") != "OK" or not results:
        return None

    top = results[0]
    location = top.get("geometry", {}).get("location") or {}
    lat = location.get("lat")
    lng = location.get("lng")
    if lat is None or lng is None:
        return None

    display = top.get("formatted_address") or query
    lat_f = float(lat)
    lng_f = float(lng)
    return MapLocation(
        query=query,
        display_name=display,
        lat=lat_f,
        lng=lng_f,
        source="google",
        map_url=_google_maps_link(lat_f, lng_f, display),
    )


def _geocode_nominatim(query: str) -> MapLocation | None:
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "accept-language": "zh-CN",
    }
    headers = {"User-Agent": _USER_AGENT}

    try:
        response = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers=headers,
            timeout=8.0,
        )
        response.raise_for_status()
        results = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Nominatim geocoding failed for %r: %s", query, exc)
        return None

    if not results:
        return None

    top = results[0]
    lat = top.get("lat")
    lon = top.get("lon")
    if lat is None or lon is None:
        return None

    display = top.get("display_name") or query
    lat_f = float(lat)
    lng_f = float(lon)
    map_url = _amap_map_link(lng_f, lat_f, display) if _amap_api_key() else _google_maps_link(lat_f, lng_f, display)
    return MapLocation(
        query=query,
        display_name=display,
        lat=lat_f,
        lng=lng_f,
        source="nominatim",
        map_url=map_url,
    )


def geocode_address(query: str) -> MapLocation | None:
    """Resolve one address string to coordinates."""
    cleaned = query.strip()
    if not cleaned or not _geocoding_enabled():
        return None

    biased = _with_region_bias(cleaned)

    amap_key = _amap_api_key()
    if amap_key:
        result = _geocode_amap(biased, amap_key)
        if result:
            return result

    google_key = _google_api_key()
    if google_key:
        result = _geocode_google(biased, google_key)
        if result:
            return result

    return _geocode_nominatim(biased)


def geocode_addresses(queries: list[str], *, max_results: int = 2) -> list[MapLocation]:
    """Geocode multiple queries; skips failures and duplicates by coordinates."""
    locations: list[MapLocation] = []
    seen_coords: set[tuple[float, float]] = set()

    for query in queries:
        if len(locations) >= max_results:
            break
        location = geocode_address(query)
        if location is None:
            continue
        key = (round(location.lat, 5), round(location.lng, 5))
        if key in seen_coords:
            continue
        seen_coords.add(key)
        locations.append(location)

    return locations
