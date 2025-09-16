<template>
  <div>
    <label>Origin:</label>
    <select v-model="origin">
      <option v-for="s in stations" :key="s[0]" :value="s[0]">
        {{ s[1] }}
      </option>
    </select>

    <label>Destination:</label>
    <select v-model="destination">
      <option v-for="s in stations" :key="s[0]" :value="s[0]">
        {{ s[1] }}
      </option>
    </select>

    <button @click="getRoute">Get Route</button>

    <RouteResult :fare="fare" :route="route" :time="time"/>
  </div>
</template>

<script>
import RouteResult from "./RouteResult.vue";

export default {
  name: "RoutePlanner",
  components: { RouteResult },
  data() {
    return {
      stations: null,
      origin: null,
      destination: null,
      fare: null,
      route: null, // will hold the /route API result
      time: null,
    };
  },
  async mounted() {
    const res = await fetch(`http://localhost:5000/stations`);
    const data = await res.json();
    this.stations = data.station;

    if (this.stations && this.stations.length > 1) {
      this.origin = this.stations[0][0];
      this.destination = this.stations[1][0];
    }
  },
  methods: {
    async getRoute() {
      const [fareRes, routeRes, timeRes] = await Promise.all([
        fetch(`http://localhost:5000/fares?from=${this.origin}&to=${this.destination}`),
        fetch(`http://localhost:5000/route?from=${this.origin}&to=${this.destination}`),
        fetch(`http://localhost:5000/time?from=${this.origin}&to=${this.destination}`)
      ]);
      
      const fareData = await fareRes.json();
      console.log(fareData);
      const routeData = await routeRes.json();
      const timeData = await timeRes.json();

      this.fare = fareData.fare;
      this.route = routeData;
      this.time = timeData.time;
    },
  },
};
</script>
