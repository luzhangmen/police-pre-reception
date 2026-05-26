/**
 * 360° panorama concept viewer (Pannellum) + Mapillary embed fallback.
 */
(function initPanoramaConcept() {
  const container = document.getElementById("panoramaViewer");
  if (!container || !window.CAMPUS_COORDS) {
    return;
  }

  const titleEl = document.getElementById("panoramaTitle");
  const noteEl = document.getElementById("panoramaNote");
  const mapillaryFrame = document.getElementById("mapillaryEmbed");
  const externalLinks = document.getElementById("panoramaExternalLinks");

  let viewer = null;
  let activePoiKey = window.CAMPUS_COORDS.panorama?.defaultPoiKey || "northTeachingBikeRack";

  function panoramaConfig(poiKey) {
    const pano = window.CAMPUS_COORDS.panorama || {};
    return pano.pois?.[poiKey] || pano.pois?.[pano.defaultPoiKey];
  }

  function poiCoords(poiKey) {
    const poi = window.CAMPUS_COORDS.pois[poiKey];
    return poi?.gcj02 || window.CAMPUS_COORDS.center.gcj02;
  }

  function buildExternalLinks(poiKey) {
    const cfg = panoramaConfig(poiKey);
    const c = poiCoords(poiKey);
    const name = encodeURIComponent(cfg?.title || window.CAMPUS_COORDS.region);
    const amap = `https://uri.amap.com/marker?position=${c.lng},${c.lat}&name=${name}`;
    const google = `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${c.lat},${c.lng}`;
    const baidu = `https://map.baidu.com/mobile/webapp/search/search/qt=s&wd=${encodeURIComponent(
      window.CAMPUS_COORDS.region
    )}`;

    externalLinks.innerHTML = `
      <a href="${amap}" target="_blank" rel="noreferrer">高德地图打开该点 →</a>
      <a href="${baidu}" target="_blank" rel="noreferrer">百度地图搜索校区 →</a>
      <a href="${google}" target="_blank" rel="noreferrer">Google 街景（可能有/无覆盖）→</a>
    `;
  }

  function updateMapillary(poiKey) {
    const c = poiCoords(poiKey);
    mapillaryFrame.src = `https://www.mapillary.com/embed?lat=${c.lat}&lng=${c.lng}&z=17&style=photo`;
  }

  function imageExists(url) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => resolve(false);
      img.src = url;
    });
  }

  async function resolveImageUrl(poiKey) {
    const cfg = panoramaConfig(poiKey);
    const fallback = window.CAMPUS_COORDS.panorama?.fallbackImage;
    if (cfg?.imageUrl) {
      const ok = await imageExists(cfg.imageUrl);
      if (ok) {
        return { url: cfg.imageUrl, fromLocal: true };
      }
    }
    return { url: fallback, fromLocal: false };
  }

  async function loadPanorama(poiKey) {
    activePoiKey = poiKey;
    const cfg = panoramaConfig(poiKey);
    const { url, fromLocal } = await resolveImageUrl(poiKey);

    if (titleEl) {
      titleEl.textContent = cfg?.title || "全景概念";
    }
    if (noteEl) {
      noteEl.textContent = fromLocal
        ? "当前为本地/仓库内 360° 全景图（可环视拖动）。"
        : "未检测到本地全景文件，正在使用开源示例图作交互演示；可往 panoramas/ 目录放入华工实拍 JPG 替换。";
    }

    buildExternalLinks(poiKey);
    updateMapillary(poiKey);

    const scene = {
      type: "equirectangular",
      panorama: url,
      yaw: cfg?.yaw ?? 0,
      pitch: cfg?.pitch ?? 0,
      hfov: 100,
      autoLoad: true,
      showControls: true,
    };

    if (viewer) {
      viewer.destroy();
      viewer = null;
    }

    viewer = pannellum.viewer("panoramaViewer", scene);
  }

  window.updatePanoramaConcept = loadPanorama;

  loadPanorama(activePoiKey);
})();
