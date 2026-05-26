/**
 * 360° panorama viewer (Pannellum) — drag to look around, fullscreen, optional gyro on mobile.
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
  const fullscreenBtn = document.getElementById("panoramaFullscreenBtn");
  const gyroBtn = document.getElementById("panoramaGyroBtn");

  let viewer = null;
  let orientationActive = false;
  const activePoiKeyDefault = window.CAMPUS_COORDS.panorama?.defaultPoiKey || "northTeachingBikeRack";

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

  let interactionsBound = false;

  function bindViewerInteractions() {
    if (interactionsBound) {
      return;
    }
    interactionsBound = true;

    fullscreenBtn?.addEventListener("click", () => {
      if (viewer && typeof viewer.toggleFullscreen === "function") {
        viewer.toggleFullscreen();
      }
    });

    container.addEventListener("dblclick", () => {
      if (viewer && typeof viewer.toggleFullscreen === "function") {
        viewer.toggleFullscreen();
      }
    });

    if (gyroBtn && typeof window.DeviceOrientationEvent !== "undefined") {
      gyroBtn.hidden = false;
      gyroBtn.addEventListener("click", async () => {
        if (!viewer || typeof viewer.startOrientation !== "function") {
          return;
        }
        if (!viewer) {
          return;
        }
        try {
          if (
            typeof DeviceOrientationEvent.requestPermission === "function" &&
            !orientationActive
          ) {
            const permission = await DeviceOrientationEvent.requestPermission();
            if (permission !== "granted") {
              return;
            }
          }
          if (orientationActive) {
            viewer.stopOrientation();
            orientationActive = false;
            gyroBtn.textContent = "开启陀螺仪环视（手机）";
          } else {
            viewer.startOrientation();
            orientationActive = true;
            gyroBtn.textContent = "关闭陀螺仪环视";
          }
        } catch {
          // User dismissed permission dialog.
        }
      });
    }
  }


  async function loadPanorama(poiKey) {
    const cfg = panoramaConfig(poiKey);
    const { url, fromLocal } = await resolveImageUrl(poiKey);

    if (titleEl) {
      titleEl.textContent = cfg?.title || "全景概念";
    }
    if (noteEl) {
      noteEl.textContent = fromLocal
        ? "华工本地 360° 全景：在画面内拖动环视，或点「全屏沉浸浏览」。"
        : "当前为示例全景图（演示交互）。放入 panoramas/*.jpg 后可换为广州大学城实拍。";
    }

    buildExternalLinks(poiKey);
    updateMapillary(poiKey);

    if (viewer) {
      viewer.destroy();
      viewer = null;
      orientationActive = false;
      if (gyroBtn) {
        gyroBtn.textContent = "开启陀螺仪环视（手机）";
      }
    }

    viewer = pannellum.viewer("panoramaViewer", {
      type: "equirectangular",
      panorama: url,
      yaw: cfg?.yaw ?? 0,
      pitch: cfg?.pitch ?? 0,
      hfov: 100,
      minHfov: 50,
      maxHfov: 120,
      autoLoad: true,
      showControls: true,
      showFullscreenCtrl: true,
      showZoomCtrl: true,
      mouseZoom: true,
      draggable: true,
      keyboardZoom: true,
      compass: true,
      friction: 0.12,
    });

    bindViewerInteractions();
  }

  window.updatePanoramaConcept = loadPanorama;

  loadPanorama(activePoiKeyDefault);
})();
