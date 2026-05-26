/**
 * Standalone map demo for GitHub Pages (no backend required).
 * Demo cases: SCUT Guangzhou University Town campus area (华南理工大学大学城校区).
 */

const CAMPUS_REGION = "华南理工大学大学城校区";
const CAMPUS_CENTER = { lat: 23.0542, lng: 113.3974 };

const DEMO_CASES = [
  {
    id: "theft-bicycle",
    title: "自行车失窃（未上锁）",
    summary: "财物遗失 · 北区教学楼",
    transcript_id: "transcript-theft-005（改编）",
    text:
      "我是华南理工大学大学城校区的学生。3月8日上午我把蓝色捷安特自行车停在北区教学楼北侧非机动车位，" +
      "下课忘记上锁，下午四点回来发现车不见了，原地只剩一把未锁好的车锁挂在栏杆上。购买价大约1800元。",
    extracted_addresses: [
      "华南理工大学大学城校区北区教学楼北侧",
      "北区教学楼北侧非机动车位",
    ],
    map_locations: [
      {
        query: `${CAMPUS_REGION}北区教学楼北侧`,
        display_name: "华南理工大学大学城校区 · 北区教学楼北侧",
        lat: 23.0568,
        lng: 113.3992,
        source: "demo",
        map_url:
          "https://uri.amap.com/marker?position=113.3992,23.0568&name=华工大学城校区北区教学楼北侧",
      },
    ],
  },
  {
    id: "theft-ebike-battery",
    title: "电瓶车电瓶被偷",
    summary: "财物遗失 · 宿舍楼下",
    transcript_id: "transcript-theft-013",
    text:
      "今天早上6点多，我在华南理工大学大学城校区宿舍楼下非机动车停放区取电动车，发现电瓶仓被撬空了。" +
      "电瓶是48V20Ah锂电池，买了大概8个月。监控里看到凌晨4点有个戴鸭舌帽的人靠近，我已经向保卫处登记申请调监控。",
    extracted_addresses: [
      "华南理工大学大学城校区宿舍楼下",
      "宿舍楼下非机动车停放区",
    ],
    map_locations: [
      {
        query: `${CAMPUS_REGION}宿舍楼下非机动车停放区`,
        display_name: "华南理工大学大学城校区 · 宿舍楼下停放区",
        lat: 23.0525,
        lng: 113.3958,
        source: "demo",
        map_url:
          "https://uri.amap.com/marker?position=113.3958,23.0525&name=华工大学城校区宿舍停放区",
      },
    ],
  },
  {
    id: "fight-street",
    title: "街道斗殴",
    summary: "肢体冲突 · 小贝大街",
    transcript_id: "transcript-fight-008（改编）",
    text:
      "3月9日凌晨，我和同学在南沙区小谷围岛大学城小贝大街吃大排档，喝酒后和邻桌发生口角，" +
      "对方三个人围过来动手，我头部受伤已经去急诊包扎。对方不认识，像是附近社会人员，" +
      "事发位置就在华南理工大学大学城校区西门往外那条商业街。",
    extracted_addresses: ["大学城小贝大街", "华南理工大学大学城校区西门商业街"],
    map_locations: [
      {
        query: "广州大学城小贝大街",
        display_name: "广州大学城 · 小贝大街（华工大学城校区附近）",
        lat: 23.0508,
        lng: 113.4045,
        source: "demo",
        map_url: "https://uri.amap.com/marker?position=113.4045,23.0508&name=大学城小贝大街",
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
      demoModeBadge.textContent = "高德地图 · 广州大学城";
      return mapEngine;
    } catch {
      demoModeBadge.textContent = "备用地图 · 广州大学城";
    }
  }

  mapEngine = {
    type: "leaflet",
    instance: L.map("map", { zoomControl: true }).setView(
      [CAMPUS_CENTER.lat, CAMPUS_CENTER.lng],
      16
    ),
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
  const ref = caseData.transcript_id ? `（笔录参考：${caseData.transcript_id}）` : "";
  mapIntro.textContent =
    `示例坐标位于${CAMPUS_REGION}及周边（广东省广州市番禺区小谷围岛）${ref}。`;
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
