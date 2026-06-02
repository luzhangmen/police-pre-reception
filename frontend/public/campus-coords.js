/**
 * 华南理工大学大学城校区（广州市番禺区小谷围岛）参考坐标
 * - gcj02：高德地图 / 国内图商（GCJ-02）
 * - wgs84：OpenStreetMap / Leaflet（WGS-84）
 *
 * 校区中心参考：外环东路382号；维基 WGS 约 23.04862°N, 113.40062°E
 */
window.CAMPUS_COORDS = {
  region: "华南理工大学大学城校区",
  city: "广州市",
  province: "广东省",
  address: "广东省广州市番禺区广州大学城外环东路382号",

  center: {
    gcj02: { lat: 23.053981, lng: 113.413298 },
    wgs84: { lat: 23.04862, lng: 113.40062 },
  },

  pois: {
    northTeachingBikeRack: {
      label: "华南理工大学大学城校区 · 北区教学楼北侧",
      query: "华南理工大学大学城校区北区教学楼",
      gcj02: { lat: 23.05645, lng: 113.41185 },
      wgs84: { lat: 23.05105, lng: 113.39925 },
    },
    dormEbikeParking: {
      label: "华南理工大学大学城校区 · 宿舍楼下非机动车停放区",
      query: "华南理工大学大学城校区宿舍区",
      gcj02: { lat: 23.05162, lng: 113.40948 },
      wgs84: { lat: 23.04622, lng: 113.39688 },
    },
    xiaobeiStreet: {
      label: "广州大学城 · 小贝大街（华工大学城校区西门附近）",
      query: "广州市番禺区大学城小贝大街",
      gcj02: { lat: 23.04688, lng: 113.41762 },
      wgs84: { lat: 23.04148, lng: 113.40502 },
    },
  },

  /**
   * 全景概念（Pannellum 等距柱状图）。
   * 本地全景：panoramas/1.jpg ~ 3.jpg，与三个 Demo 案例一一对应。
   */
  panorama: {
    defaultPoiKey: "northTeachingBikeRack",
    fallbackImage: "panoramas/1.jpg",
    pois: {
      northTeachingBikeRack: {
        title: "北区教学楼北侧 · 全景",
        imageUrl: "panoramas/1.jpg",
        yaw: 0,
        pitch: 0,
      },
      dormEbikeParking: {
        title: "宿舍楼下停放区 · 全景",
        imageUrl: "panoramas/2.jpg",
        yaw: 0,
        pitch: 0,
      },
      xiaobeiStreet: {
        title: "小贝大街 · 全景",
        imageUrl: "panoramas/3.jpg",
        yaw: 0,
        pitch: 0,
      },
    },
  },
};

window.campusMapLocation = function campusMapLocation(poiKey, source) {
  const poi = window.CAMPUS_COORDS.pois[poiKey];
  const coords = source === "wgs84" ? poi.wgs84 : poi.gcj02;
  const lng = coords.lng;
  const lat = coords.lat;
  const name = encodeURIComponent(poi.label);
  return {
    query: poi.query,
    display_name: poi.label,
    lat,
    lng,
    coord_system: source === "wgs84" ? "wgs84" : "gcj02",
    source: "scut_campus_poi",
    map_url: `https://uri.amap.com/marker?position=${lng},${lat}&name=${name}`,
  };
};
