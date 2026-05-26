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
    const candidates = [cfg?.imageUrl, cfg?.sharedImageUrl, fallback].filter(Boolean);

    for (const url of candidates) {
      if (await imageExists(url)) {
        const isPrimary = url === cfg?.imageUrl;
        return {
          url,
          fromLocal: true,
          shared: !isPrimary && url === cfg?.sharedImageUrl,
        };
      }
    }

    return { url: "https://pannellum.org/images/alma.jpg", fromLocal: false, shared: false };
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
    const { url, fromLocal, shared } = await resolveImageUrl(poiKey);

    if (titleEl) {
      titleEl.textContent = cfg?.title || "全景概念";
    }
    if (noteEl) {
      if (!fromLocal) {
        noteEl.textContent =
          "未加载到本地全景文件，正在使用备用示例图。请确认 panoramas/scut-north-teaching.jpg 已随仓库部署。";
      } else if (shared) {
        noteEl.textContent =
          "当前展示已上传的华工北区实拍全景（该案例专属图尚未上传，视角已预置偏移）。拖动环视或点「全屏沉浸浏览」。";
      } else {
        noteEl.textContent =
          "华南理工大学大学城校区 · 北区教学楼北侧实拍 360°。拖动环视或点「全屏沉浸浏览」。";
      }
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
