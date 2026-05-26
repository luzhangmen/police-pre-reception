import pytest

from app.core.pipeline import run_pipeline
from app.core.state import MapLocation, UserMessage
from app.modules import geocoder
from app.modules.address_extractor import extract_addresses
from app.modules.geocoder import geocode_address, geocode_addresses


def test_extract_addresses_from_slots_and_text():
    text = "今天下午在一食堂二楼吃饭时手机被偷了，我现在还在图书馆三楼。"
    slots = {
        "lost_item": "手机",
        "lost_time": "今天下午",
        "lost_location": "一食堂二楼就餐区",
        "item_features": "黑色手机壳",
    }

    addresses = extract_addresses(text, slots)

    assert "一食堂二楼就餐区" in addresses
    assert any("一食堂" in item or "图书馆" in item for item in addresses)


def test_extract_skips_online_only_locations():
    slots = {"incident_location": "网络平台/微信转账"}

    assert extract_addresses("我在闲鱼被骗了", slots) == []


def test_geocode_addresses_deduplicates(monkeypatch):
    def fake_geocode(query: str):
        return MapLocation(
            query=query,
            display_name=f"resolved:{query}",
            lat=31.23,
            lng=121.47,
            source="test",
            map_url="https://example.com",
        )

    monkeypatch.setattr(geocoder, "geocode_address", fake_geocode)
    monkeypatch.setattr(geocoder, "_geocoding_enabled", lambda: True)

    locations = geocode_addresses(["一食堂", "学校食堂"], max_results=3)

    assert len(locations) == 1


def test_pipeline_attaches_map_fields(monkeypatch):
    monkeypatch.setattr(
        "app.modules.schema_extractor.call_llm_json",
        lambda **_: {
            "lost_item": "手机",
            "lost_time": "今天下午",
            "lost_location": "一食堂二楼",
            "item_features": "黑色",
        },
    )
    monkeypatch.setattr(
        "app.modules.dialogue_policy.call_llm_json",
        lambda **_: {"next_question": "手机型号是什么？"},
    )
    monkeypatch.setattr(
        "app.modules.summary_generator.call_llm_json",
        lambda **_: {"summary": "食堂手机被盗。", "key_facts": [], "suggested_next_steps": []},
    )

    def fake_geocode_addresses(queries, *, max_results=2):
        if not queries:
            return []
        return [
            MapLocation(
                query=queries[0],
                display_name="一食堂",
                lat=31.1,
                lng=121.4,
                source="test",
                map_url="https://example.com",
            )
        ]

    monkeypatch.setattr("app.core.pipeline.geocode_addresses", fake_geocode_addresses)

    state = run_pipeline(
        UserMessage(text="今天下午在一食堂二楼手机被偷了。", case_id="map-case")
    )

    assert state.extracted_addresses
    assert state.map_locations
    assert state.map_locations[0].lat == 31.1


def test_geocode_disabled_in_pytest_by_default():
    assert geocode_address("一食堂二楼") is None


def test_amap_geocode_parses_location(monkeypatch):
    monkeypatch.setenv("AMAP_API_KEY", "test-amap-key")
    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    monkeypatch.setattr(geocoder, "_geocoding_enabled", lambda: True)

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "status": "1",
                "geocodes": [
                    {
                        "formatted_address": "上海市某大学一食堂",
                        "location": "121.473701,31.230416",
                    }
                ],
            }

    monkeypatch.setattr(geocoder.httpx, "get", lambda *args, **kwargs: FakeResponse())

    location = geocode_address("一食堂二楼")

    assert location is not None
    assert location.source == "amap"
    assert location.lat == pytest.approx(31.230416)
    assert location.lng == pytest.approx(121.473701)
    assert "uri.amap.com" in location.map_url


def test_resolve_map_provider_prefers_amap(monkeypatch):
    monkeypatch.setenv("AMAP_API_KEY", "k")
    provider_id, label = geocoder.resolve_map_provider()
    assert provider_id == "amap"
    assert "高德" in label
