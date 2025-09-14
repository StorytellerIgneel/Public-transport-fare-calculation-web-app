<template>
  <LMap :zoom="zoom" :center="center" style="height: 100vh; width: 100vw;">
    <LTileLayer :url="url" :attribution="attribution" />
    <LMarker :lat-lng="markerLatLng" />
  </LMap>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default {
  components: { LMap, LTileLayer, LMarker },
  data() {
    return {
      zoom: 12,
      center: [3.139, 101.6869],
      markerLatLng: [3.139, 101.6869],
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    };
  },
};
</script>
