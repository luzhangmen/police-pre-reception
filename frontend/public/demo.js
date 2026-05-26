/**
 * Standalone map demo for GitHub Pages (no backend required).
 * Coordinates are illustrative; replace MAP_DEFAULT_REGION in production geocoding.
 */

const DEMO_CASES = [
  {
    id: "theft-canteen",
    title: "食堂手机被盗",
    summary: "财物遗失 · 一食堂",
    text: "今天下午在一食堂二楼吃饭时手机被偷了，对方往北区宿舍方向跑了，我现在很着急。",
    extracted_addresses: ["一食堂二楼就餐区", "北区宿舍方向"],
    map_locations: [
      {
        query: "一食堂二楼",
        display_name: "第一食堂（示例坐标）",
        lat: 31.2308,
        lng: 121.4742,
        source: "demo",
        map_url: "https://uri.amap.com/marker?position=121.4742,31.2308&name=第一食堂",
      },
    ],
  },
  {
    id: "loss-library",
    title: "图书馆遗失物品",
    summary: "财物遗失 · 图书馆",
    text: "昨晚在图书馆三楼自习区落了一个黑色双肩包，里面有学生证，大概九点半离开的。",
    extracted_addresses: ["图书馆三楼自习区"],
    map_locations: [
      {
        query: "图书馆三楼自习区",
        display_name: "图书馆（示例坐标）",
        lat: 31.2316,
        lng: 121.4728,
        source: "demo",
        map_url: "https://uri.amap.com/marker?position=121.4728,31.2316&name=图书馆",
      },
    ],
  },
  {
    id: "dorm-conflict",
    title: "宿舍冲突",
    summary: "宿舍矛盾 · 302",
    text: "昨晚宿舍302因为卫生问题和室友吵起来，对方推了我一下，发生在宿舍楼区域。",
    extracted_addresses: ["宿舍302", "宿舍楼"],
    map_locations: [
      {
        query: "学生宿舍302",
        display_name: "学生宿舍区（示例坐标）",
        lat: 31.2295,
        lng: 121.4755,
        source: "demo",
        map_url: "https://uri.amap.com/marker?position=121.4755,31.2295&name=学生宿舍",
      },
    ],
  },
];

const NEARBY_RADIUS = 250;
const amapKey = (window.__DEMO_AMAP_KEY__ || "").trim();

const demoCaseList = document.getElementById("demoCaseList");
const demoQuote = document.getElementById("demoQuote");
const demoAddresses = document.getElementById("demoAddresses");
const mapMeta = document.getElementById("mapMeta");
const mapIntro = document.getElementById("mapIntro");
const mapEmpty = document.getElementById("mapEmpty");
const locationList = document.getElementById("locationList");
const demoBanner = document.getElementById("demoBanner");
const demoModeBadge = document.getElementById("demoModeBadge");

let mapEngine = null;
let mapOverlays = [];

function setMapEmptyVisible(visible) {
  mapEmpty.classList.toggle("hidden", !visible);
}

function loadAmapScript(key) {
  return new Promise((resolve, reject) => {
    if (window.AMap) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${encodeURIComponent(key)}`;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Amap load failed"));
    document.head.appendChild(script);
  });
}

async function initMapEngine() {
  if (mapEngine) {
    return mapEngine;
  }

  if (amapKey) {
    try {
      await loadAmapScript(amapKey);
      mapEngine = { type: "amap", instance: null };
      demoBanner.classList.add("hidden");
      demoModeBadge.textContent = "高德地图演示";
      return mapEngine;
    } catch {
      demoModeBadge.textContent = "备用地图演示";
    }
  }

  mapEngine = {
    type: "leaflet",
    instance: L.map("map", { zoomControl: true }).setView([31.231, 121.474], 16),
    layer: L.layerGroup(),
  };
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap",
  }).addTo(mapEngine.instance);
  mapEngine.layer.addTo(mapEngine.instance);
  return mapEngine;
}

function clearMapOverlays() {
  mapOverlays.forEach((item) => {
    if (typeof item.setMap === "function") {
      item.setMap(null);
    } else if (typeof item.remove === "function") {
      item.remove();
    }
  });
  mapOverlays = [];
  if (mapEngine?.type === "leaflet" && mapEngine.layer) {
    mapEngine.layer.clearLayers();
  }
}

async function renderAmap(locations) {
  const engine = await initMapEngine();
  if (engine.type !== "amap") {
    return false;
  }

  if (!engine.instance) {
    engine.instance = new AMap.Map("map", {
      zoom: 16,
      center: [locations[0].lng, locations[0].lat],
    });
  }

  clearMapOverlays();
  locations.forEach((loc, index) => {
    const center = [loc.lng, loc.lat];
    const marker = new AMap.Marker({
      position: center,
      title: loc.display_name,
      label: { content: `<div class="amap-label">${index + 1}</div>`, direction: "top" },
    });
    marker.setMap(engine.instance);
    mapOverlays.push(marker);

    const circle = new AMap.Circle({
      center,
      radius: NEARBY_RADIUS,
      strokeColor: "#0d8f6f",
      strokeWeight: 2,
      fillColor: "#0d8f6f",
      fillOpacity: 0.12,
    });
    circle.setMap(engine.instance);
    mapOverlays.push(circle);
  });

  engine.instance.setFitView(
    mapOverlays.filter((o) => o instanceof AMap.Marker),
    false,
    [36, 36, 36, 36]
  );
  return true;
}

async function renderLeaflet(locations) {
  const engine = await initMapEngine();
  clearMapOverlays();
  const latLngs = [];

  locations.forEach((loc, index) => {
    const latLng = [loc.lat, loc.lng];
    latLngs.push(latLng);
    const marker = L.marker(latLng).addTo(engine.layer);
    marker.bindPopup(`<strong>${loc.display_name}</strong>`);
    mapOverlays.push(marker);

    const circle = L.circle(latLng, {
      radius: NEARBY_RADIUS,
      color: "#0d8f6f",
      fillColor: "#0d8f6f",
      fillOpacity: 0.12,
      weight: 2,
    }).addTo(engine.instance);
    mapOverlays.push(circle);
  });

  engine.instance.fitBounds(latLngs, { padding: [32, 32], maxZoom: 17 });
  setTimeout(() => engine.instance.invalidateSize(), 100);
}

function renderLocationCards(locations) {
  locationList.innerHTML = "";
  const linkLabel = amapKey ? "在高德地图中打开" : "查看地图链接";

  locations.forEach((loc, index) => {
    const li = document.createElement("li");
    li.className = "location-card";
    li.innerHTML = `
      <div class="location-pin">${index + 1}</div>
      <div>
        <strong>${loc.display_name}</strong>
        <div class="muted">检索：${loc.query}</div>
        <a href="${loc.map_url}" target="_blank" rel="noreferrer">${linkLabel} →</a>
      </div>`;
    locationList.appendChild(li);
  });
}

async function showCase(caseData) {
  demoQuote.textContent = caseData.text;
  demoAddresses.textContent = caseData.extracted_addresses.join("；");

  document.querySelectorAll(".demo-case-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.caseId === caseData.id);
  });

  const locations = caseData.map_locations;
  if (!locations.length) {
    setMapEmptyVisible(true);
    mapMeta.textContent = "无线下地点";
    return;
  }

  setMapEmptyVisible(false);
  const usedAmap = await renderAmap(locations);
  if (!usedAmap) {
    await renderLeaflet(locations);
  }
  renderLocationCards(locations);

  mapMeta.textContent = `已标出 ${locations.length} 处 · 附近约 ${NEARBY_RADIUS} 米`;
  mapIntro.textContent = "演示数据为示例坐标；接入后端与高德 Key 后将按真实地址解析。";
}

function buildCaseButtons() {
  DEMO_CASES.forEach((caseData) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "demo-case-btn";
    btn.dataset.caseId = caseData.id;
    btn.innerHTML = `<strong>${caseData.title}</strong><span>${caseData.summary}</span>`;
    btn.addEventListener("click", () => showCase(caseData));
    demoCaseList.appendChild(btn);
  });
}

buildCaseButtons();
initMapEngine().then(() => showCase(DEMO_CASES[0]));
