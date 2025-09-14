<template>
  <div>
    <h2>Metro Tracking & Fare Kiosk</h2>
    <RoutePlanner />
    <MapView />
  </div>
</template>

<script>
import MapView from "./components/MapView.vue";
import RoutePlanner from "./components/RoutePlanner.vue";

export default {
  name: "MainKiosk",
  components: { MapView, RoutePlanner }
};
</script>
