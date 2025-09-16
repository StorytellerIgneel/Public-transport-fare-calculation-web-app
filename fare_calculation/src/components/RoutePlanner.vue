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

    <div v-if="fare"><span>Fare</span>: RM {{ fare }}</div>
  </div>
</template>

<script>
export default {
  name: "RoutePlanner",
  data() {
    return {
      stations: null,
      origin: null,
      destination: null,
      fare: null,
    };
  },
  async mounted() {
    const res = await fetch(`http://localhost:5000/stations`);
    const data = await res.json();
    this.stations = data.station;

    if (this.stations && this.stations.length > 0) {
      this.origin = this.stations[0][0];
      this.destination = this.stations[1][0];
    }
  },
  methods: {
    async getRoute() {
      const res = await fetch(
        `http://localhost:5000/fares?from=${this.origin}&to=${this.destination}`
      );
      const data = await res.json();
      this.fare = data.fare;
    },
  },
};
</script>

<style scoped>
div > label {
  margin-right: 15px;
  font-weight: bold;
}

span{
  font-weight: bold;
}

select {
  margin-right: 20px;
}
</style>
