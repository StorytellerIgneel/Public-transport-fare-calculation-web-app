<template>
  <div v-if="route">
    <h3>Route Details</h3>
    <p><b>Total Fare:</b> RM {{ route.total_fare }}</p>
    <p><b>Total Hops:</b> {{ route.total_hops }}</p>

    <h4>Path:</h4>
    <ul>
      <li v-for="(station, i) in route.path" :key="i">
        {{ station }}
      </li>
    </ul>
  </div>
  <div v-else>
    <p>No route selected yet.</p>
  </div>
</template>

<script>
export default {
  name: "RouteResult",
  props: {
    route: {
      type: Object,
      required: false,
    },
  },
};
</script>



