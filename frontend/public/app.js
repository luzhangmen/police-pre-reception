const apiBase = window.location.origin;

const caseIdInput = document.getElementById("caseId");
const userTextInput = document.getElementById("userText");
const voiceBtn = document.getElementById("voiceBtn");
const submitBtn = document.getElementById("submitBtn");
const errorBox = document.getElementById("errorBox");
const speechSupport = document.getElementById("speechSupport");
const mapProviderBadge = document.getElementById("mapProviderBadge");
const voiceHint = document.getElementById("voiceHint");
const resultBody = document.getElementById("resultBody");
const resultMeta = document.getElementById("resultMeta");
const mapMeta = document.getElementById("mapMeta");
const mapIntro = document.getElementById("mapIntro");
const mapEmpty = document.getElementById("mapEmpty");
const mapSetupNote = document.getElementById("mapSetupNote");
const locationList = document.getElementById("locationList");

let mapConfig = {
  nearby_radius_meters: 250,
  map_provider: "nominatim",
  map_provider_label: "备用地图",
  amap_js_key: "",
};

let mapEngine = null;
let mapOverlays = [];
let recognition = null;
let recognizing = false;

const scenarioLabels = {
  telecom_fraud: "电信 / 网络诈骗",
  property_loss: "财物遗失或被盗",
  dorm_conflict: "宿舍矛盾纠纷",
  personal_safety_threat: "人身安全威胁",
  unknown: "待进一步判断",
};

const riskLabels = {
  low: { text: "较低", className: "tag-risk-low", hint: "可先按指引补充信息" },
  medium: { text: "中等", className: "tag-risk-medium", hint: "建议尽快补充关键信息" },
  high: {
    text: "较高",
    className: "tag-risk-high",
    hint: "若您感到紧迫危险，请同时拨打 110 或联系校内保卫部门",
  },
};

function showError(message) {
  if (!message) {
    errorBox.hidden = true;
    errorBox.textContent = "";
    return;
  }
  errorBox.hidden = false;
  errorBox.textContent = message;
}

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
    script.onerror = () => reject(new Error("高德地图脚本加载失败"));
    document.head.appendChild(script);
  });
}

async function initMapEngine() {
  if (mapEngine) {
    return mapEngine;
  }

  if (mapConfig.amap_js_key) {
    try {
      await loadAmapScript(mapConfig.amap_js_key);
      mapEngine = { type: "amap", instance: null, layer: null };
      return mapEngine;
    } catch {
      mapProviderBadge.textContent = "高德加载失败，已切换备用底图";
    }
  }

  mapEngine = {
    type: "leaflet",
    instance: L.map("map", { zoomControl: true }).setView([31.23, 121.47], 15),
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

async function renderAmapLocations(locations, radius) {
  const engine = await initMapEngine();
  if (engine.type !== "amap") {
    return false;
  }

  if (!engine.instance) {
    engine.instance = new AMap.Map("map", {
      viewMode: "2D",
      zoom: 16,
      center: [locations[0].lng, locations[0].lat],
    });
  }

  clearMapOverlays();

  const bounds = [];
  locations.forEach((loc, index) => {
    const center = [loc.lng, loc.lat];
    bounds.push(center);

    const marker = new AMap.Marker({
      position: center,
      title: loc.display_name,
      label: {
        content: `<div class="amap-label">${index + 1}</div>`,
        direction: "top",
      },
    });
    marker.setMap(engine.instance);
    mapOverlays.push(marker);

    const circle = new AMap.Circle({
      center,
      radius,
      strokeColor: "#0d8f6f",
      strokeWeight: 2,
      fillColor: "#0d8f6f",
      fillOpacity: 0.12,
    });
    circle.setMap(engine.instance);
    mapOverlays.push(circle);
  });

  engine.instance.setFitView(mapOverlays.filter((o) => o instanceof AMap.Marker), false, [40, 40, 40, 40]);
  return true;
}

async function renderLeafletLocations(locations, radius) {
  const engine = await initMapEngine();
  if (engine.type !== "leaflet") {
    return;
  }

  clearMapOverlays();
  const latLngs = [];

  locations.forEach((loc, index) => {
    const latLng = [loc.lat, loc.lng];
    latLngs.push(latLng);

    const marker = L.marker(latLng).addTo(engine.layer);
    marker.bindPopup(
      `<strong>地点 ${index + 1}</strong><br>${loc.display_name}<br><span style="color:#5c6f64">检索：${loc.query}</span>`
    );
    mapOverlays.push(marker);

    const circle = L.circle(latLng, {
      radius,
      color: "#0d8f6f",
      fillColor: "#0d8f6f",
      fillOpacity: 0.12,
      weight: 2,
    }).addTo(engine.instance);
    mapOverlays.push(circle);
  });

  engine.instance.fitBounds(latLngs, { padding: [32, 32], maxZoom: 17 });
  setTimeout(() => engine.instance.invalidateSize(), 120);
}

function renderLocationCards(locations) {
  locationList.innerHTML = "";
  const linkLabel =
    mapConfig.map_provider === "amap" ? "在高德地图中打开" : "在地图 App 中查看";

  locations.forEach((loc, index) => {
    const li = document.createElement("li");
    li.className = "location-card";
    li.innerHTML = `
      <div class="location-pin" aria-hidden="true">${index + 1}</div>
      <div>
        <div><strong>${loc.display_name}</strong></div>
        <div class="muted">根据您的描述检索：${loc.query}</div>
        <a href="${loc.map_url}" target="_blank" rel="noreferrer">${linkLabel} →</a>
      </div>
    `;
    locationList.appendChild(li);
  });
}

async function renderMap(locations) {
  await initMapEngine();
  clearMapOverlays();
  locationList.innerHTML = "";

  if (!locations.length) {
    setMapEmptyVisible(true);
    mapMeta.textContent = "本次未标出地点";
    mapIntro.textContent =
      "若案情主要发生在网上（如转账、刷单），通常不会出现地图，这属于正常情况。";
    return;
  }

  setMapEmptyVisible(false);
  const radius = mapConfig.nearby_radius_meters || 250;
  const usedAmap = await renderAmapLocations(locations, radius);
  if (!usedAmap) {
    await renderLeafletLocations(locations, radius);
  }

  renderLocationCards(locations);

  const providerLabel = mapConfig.map_provider_label || "地图";
  mapMeta.textContent = `已标出 ${locations.length} 处 · 附近约 ${radius} 米`;
  mapIntro.textContent = `使用 ${providerLabel} 展示，浅色区域供接警员参考，不代表精确管辖边界。`;
}

function renderResult(state) {
  const scenario = scenarioLabels[state.scenario] || state.scenario;
  const risk = riskLabels[state.risk_level] || {
    text: state.risk_level,
    className: "tag-risk-medium",
    hint: "",
  };

  resultMeta.textContent = scenario;

  const cards = [
    {
      title: "风险与类型",
      body: `<span class="tag ${risk.className}">风险：${risk.text}</span>
        <p style="margin:10px 0 0">${risk.hint}</p>
        <p class="muted" style="margin:6px 0 0">场景：${scenario}</p>`,
    },
    {
      title: "建议您补充回答",
      body: `<p style="margin:0">${state.next_question || "暂无追问，请留意下方摘要。"}</p>`,
    },
    {
      title: "给接警员的摘要",
      body: `<p style="margin:0">${state.police_summary || "暂无摘要"}</p>`,
    },
    {
      title: "从描述中识别到的地点",
      body: `<p style="margin:0">${
        (state.extracted_addresses || []).join("；") ||
        "未识别到线下具体地点（若仅涉及网上转账，可忽略此项）"
      }</p>`,
    },
    {
      title: "已抽取的关键信息",
      body: `<pre>${JSON.stringify(state.slots || {}, null, 2)}</pre>`,
    },
  ];

  resultBody.innerHTML = cards
    .map(
      (card) =>
        `<article class="result-card"><h3>${card.title}</h3><div>${card.body}</div></article>`
    )
    .join("");
}

function updateMapProviderBadge() {
  const label = mapConfig.map_provider_label || "备用地图";
  if (mapConfig.map_provider === "amap") {
    mapProviderBadge.textContent = `🗺 已启用 ${label}`;
    mapProviderBadge.style.background = "#e3f5ef";
    mapProviderBadge.style.color = "#08725a";
    mapSetupNote.textContent = "";
  } else {
    mapProviderBadge.textContent = `🗺 当前：${label}`;
    mapSetupNote.textContent =
      mapConfig.setup_hint ||
      "提示：配置高德 Key 后，校内「一食堂、图书馆」等地点定位会更准。";
  }

  if (mapConfig.default_region) {
    mapIntro.textContent = `将以「${mapConfig.default_region}」为范围辅助理解校内地点。`;
  }
}

async function loadMapConfig() {
  try {
    const response = await fetch(`${apiBase}/api/v1/map/config`);
    if (response.ok) {
      mapConfig = { ...mapConfig, ...(await response.json()) };
    }
  } catch {
    mapConfig.setup_hint = "请启动后端服务以加载地图配置。";
  }
  updateMapProviderBadge();
}

async function submitCase() {
  const text = userTextInput.value.trim();
  if (!text) {
    showError("请先说说发生了什么，或使用语音输入。");
    return;
  }

  showError("");
  submitBtn.disabled = true;
  submitBtn.textContent = "正在整理…";

  const payload = { text };
  const caseId = caseIdInput.value.trim();
  if (caseId) {
    payload.case_id = caseId;
  }

  try {
    const response = await fetch(`${apiBase}/api/v1/reason`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || `请求失败（${response.status}）`);
    }

    const state = await response.json();
    renderResult(state);
    await renderMap(state.map_locations || []);
  } catch (error) {
    showError(error.message || "暂时无法连接服务，请确认后端已启动。");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "提交，帮我整理";
  }
}

function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    speechSupport.textContent = "此浏览器暂不支持语音";
    voiceBtn.disabled = true;
    return;
  }

  speechSupport.textContent = "✓ 支持语音输入";
  recognition = new SpeechRecognition();
  recognition.lang = "zh-CN";
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      if (event.results[i].isFinal) {
        transcript += event.results[i][0].transcript;
      }
    }
    if (transcript) {
      const prefix = userTextInput.value.trim();
      userTextInput.value = prefix ? `${prefix} ${transcript}` : transcript;
    }
  };

  recognition.onerror = (event) => {
    showError(`语音识别遇到问题：${event.error}。您也可以改用打字。`);
    stopVoice();
  };

  recognition.onend = () => {
    if (recognizing) {
      recognition.start();
    }
  };
}

function startVoice() {
  if (!recognition) {
    return;
  }
  recognizing = true;
  voiceBtn.textContent = "⏹ 停止录音";
  voiceBtn.classList.add("active");
  voiceBtn.setAttribute("aria-pressed", "true");
  voiceHint.textContent = "正在听您说… 请放慢语速，尽量说清楚时间、地点和经过。";
  recognition.start();
}

function stopVoice() {
  recognizing = false;
  if (recognition) {
    recognition.stop();
  }
  voiceBtn.textContent = "🎙 语音输入";
  voiceBtn.classList.remove("active");
  voiceBtn.setAttribute("aria-pressed", "false");
  voiceHint.textContent =
    "语音会转成文字显示在上方，您可继续修改后再提交。推荐使用 Chrome 或 Edge 浏览器。";
}

voiceBtn.addEventListener("click", () => {
  if (recognizing) {
    stopVoice();
  } else {
    showError("");
    startVoice();
  }
});

submitBtn.addEventListener("click", submitCase);

if (location.hostname.endsWith("github.io")) {
  const notice = document.getElementById("pagesNotice");
  if (notice) {
    notice.classList.remove("hidden");
  }
}

loadMapConfig().then(() => {
  setupSpeechRecognition();
  setMapEmptyVisible(true);
});
