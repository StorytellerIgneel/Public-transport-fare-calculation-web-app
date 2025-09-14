<template>
  <div>
    <label>Origin:</label>
    <select v-model="origin">
      <option v-for="s in stations" :key="s.id" :value="s.id">{{ s.name }}</option>
    </select>

    <label>Destination:</label>
    <select v-model="destination">
      <option v-for="s in stations" :key="s.id" :value="s.id">{{ s.name }}</option>
    </select>

    <button @click="getRoute">Get Route</button>

    <div v-if="fare">Fare: RM {{ fare }}</div>
  </div>
</template>

<script>
export default {
  name: "RoutePlanner",
  data() {
    return {
      stations: [],
      origin: null,
      destination: null,
      fare: null,
    };
  },
  async mounted() {
    // Replace with API call
    const res = await fetch("/stations.json");
    this.stations = await res.json();
  },
  methods: {
    async getRoute() {
      // later: fetch(`/route?from=${this.origin}&to=${this.destination}`)
      const res = await fetch(`/fare.json`); 
      const data = await res.json();
      this.fare = data.price;
    }
  }
};
</script>
