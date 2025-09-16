<template>
  <LMap :zoom="zoom" :center="center" style="height: 100vh; width: 100vw">
    <LTileLayer :url="url" :attribution="attribution" />
    <LCircleMarker
      v-for="station in stations"
      :key="station[0]"
      :lat-lng="[station[2], station[3]]"
      :radius="6"
      :color="station[4] === 'KJL' ? 'red' : 'green'"
      :fillColor="station[4] === 'KJL' ? 'red' : 'green'"
      :fillOpacity="0.9"
    >
      <LPopup>
        <b>{{ station[1] }}</b
        ><br />
        Line: {{ station[4] }}
      </LPopup>
    </LCircleMarker>
    <!-- Train markers -->
    <LCircleMarker
      v-for="(train, id) in trains"
      :key="id"
      :lat-lng="[train.lat, train.lng]"
      :radius="10"
      :color="'orange'"
      :fillColor="'orange'"
      :fillOpacity="1.0"
    >
      <LPopup>
        🚆 Train: {{ train.train_id }} <br />
        Line: {{ train.line }} <br />
        Station ID: {{ train.current_station_id }}
      </LPopup>
    </LCircleMarker>

    <!-- LRT Kelana Jaya Line (KJL) -->
    <LPolyline v-if="lrtCoords.length > 0" :lat-lngs="lrtCoords" color="red" />

    <!-- MRT Sungai Buloh–Kajang Line (SBK) -->
    <LPolyline
      v-if="mrtCoords.length > 0"
      :lat-lngs="mrtCoords"
      color="green"
    />
  </LMap>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { io } from "socket.io-client";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
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
      stations: null,
      lrtCoords: null,
      mrtCoords: null,
      trains: {},
    };
  },
  async mounted() {
    const res = await fetch(`http://localhost:5000/stations`);
    const data = await res.json();
    this.stations = data.station;

    if (this.stations && this.stations.length > 0) {
      this.lrtCoords = this.stations
        .filter((s) => s[4] === "KJL")
        .map((s) => [s[2], s[3]]);

      this.mrtCoords = this.stations
        .filter((s) => s[4] === "SBK")
        .map((s) => [s[2], s[3]]);
    }

    const socket = io("http://localhost:5000");

    socket.on("connect", () => {
      console.log("Connected to WebSocket");
      socket.emit("start_updates");
    });

    socket.on("train_update", (data) => {
      // Lookup station coords from ID
      const station = this.stations.find(
        (s) => Number(s[0]) === Number(data.current_station_id)
      );
      if (station) {
        this.trains = {
          ...this.trains,
          [data.train_id]: {
            ...data,
            lat: station[2],
            lng: station[3],
          },
        };
      }
    });
  },
};
</script>
