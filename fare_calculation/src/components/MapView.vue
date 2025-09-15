<template>
  <LMap :zoom="zoom" :center="center" style="height: 100vh; width: 100vw">
    <LTileLayer :url="url" :attribution="attribution" />
    <LCircleMarker
      v-for="station in stations"
      :key="station.id"
      :lat-lng="[station.Latitude, station.Longitude]"
      :radius="6"
      :color="station.Line === 'KJL' ? 'red' : 'green'"
      :fillColor="station.Line === 'KJL' ? 'red' : 'green'"
      :fillOpacity="0.9"
    >
      <LPopup>
        <b>{{ station.station }}</b
        ><br />
        Line: {{ station.Line }}
      </LPopup>
    </LCircleMarker>

    <!-- LRT Kelana Jaya Line (KJL) -->
    <LPolyline v-if="lrtCoords.length > 0" :lat-lngs="lrtCoords" color="red" />

    <!-- MRT Sungai Buloh–Kajang Line (SBK) -->
    <LPolyline v-if="mrtCoords.length > 0" :lat-lngs="mrtCoords" color="green" />
  </LMap>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import station from "../assets/stations.json";
import { LPopup } from "@vue-leaflet/vue-leaflet";
import { LPolyline } from "@vue-leaflet/vue-leaflet";
import { LCircleMarker } from "@vue-leaflet/vue-leaflet";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default {
  components: { LMap, LTileLayer, LMarker, LPopup, LPolyline, LCircleMarker },
  data() {
    return {
      zoom: 12,
      center: [3.139, 101.6869],
      markerLatLng: [3.139, 101.6869],
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      stations: station,
      lrtCoords: station
        .filter((s) => s.Line === "KJL")
        .map((s) => [s.Latitude, s.Longitude]),
      mrtCoords: station
        .filter((s) => s.Line === "SBK")
        .map((s) => [s.Latitude, s.Longitude]),
    };
  },
};
</script>
