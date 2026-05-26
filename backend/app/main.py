import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.pipeline import run_pipeline
from app.core.state import CaseState, GeocodeRequest, GeocodeResponse, UserMessage
from app.modules.address_extractor import extract_addresses
from app.modules.geocoder import _amap_web_key, geocode_addresses, resolve_map_provider

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public"

app = FastAPI(
    title="Police Pre-Reception API",
    version="0.2.0",
    description=(
        "Campus police pre-reception: classify reports, extract structured fields, "
        "triage risk, suggest follow-ups, and optionally resolve incident locations on a map."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/about")
def about() -> dict[str, str]:
    return {
        "name": "Police Pre-Reception API",
        "ui": "/index.html" if FRONTEND_DIR.is_dir() else "",
        "docs": "/docs",
        "health": "/health",
        "reason_endpoint": "/api/v1/reason",
        "map_geocode_endpoint": "/api/v1/map/geocode",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/map/config")
def map_config() -> dict[str, object]:
    provider_id, provider_label = resolve_map_provider()
    amap_web_key = _amap_web_key()
    return {
        "geocoding_enabled": os.getenv("MAP_GEOCODING_ENABLED", "true").lower()
        not in {"0", "false", "no"},
        "default_region": os.getenv("MAP_DEFAULT_REGION", "").strip(),
        "map_provider": provider_id,
        "map_provider_label": provider_label,
        "amap_js_key": amap_web_key if provider_id == "amap" else "",
        "has_amap_key": bool(amap_web_key),
        "nearby_radius_meters": int(os.getenv("MAP_NEARBY_RADIUS_METERS", "250")),
        "setup_hint": (
            "国内推荐配置高德地图：在 .env 填写 AMAP_API_KEY 与 MAP_DEFAULT_REGION（学校名称）。"
            if provider_id != "amap"
            else ""
        ),
    }


@app.post("/api/v1/map/geocode", response_model=GeocodeResponse)
def geocode_from_text(payload: GeocodeRequest) -> GeocodeResponse:
    addresses = extract_addresses(payload.text, payload.slots, max_items=payload.max_results)
    locations = geocode_addresses(addresses, max_results=payload.max_results)
    provider_id, _ = resolve_map_provider()
    return GeocodeResponse(
        extracted_addresses=addresses,
        map_locations=locations,
        map_provider=provider_id,
    )


@app.post("/api/v1/reason", response_model=CaseState)
def reason(message: UserMessage) -> CaseState:
    return run_pipeline(message)


if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
