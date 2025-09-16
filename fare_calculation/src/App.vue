<template>
  <div>
    <div class="header">
      <h2>Metro Tracking & Fare Kiosk</h2>
      <RoutePlanner />
    </div>
    <MapView />
  </div>
</template>

<script>
import MapView from "./components/MapView.vue";
import RoutePlanner from "./components/RoutePlanner.vue";

export default {
  name: "MainKiosk",
  components: { MapView, RoutePlanner },
};
</script>

<style>

.header{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-bottom: 10px;
}
</style>
