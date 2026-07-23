<script setup>
const sapUrl = import.meta.env.VITE_SAP_URL
</script>

<template>
  <div class="dashboard">
   <iframe
      :src="sapUrl"
      width="100%"
      height="600"
      style="border: none;"
    ></iframe>
  </div>
</template>