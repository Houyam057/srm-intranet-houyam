<script setup>
const sapBiUrl = import.meta.env.VITE_SAP_BI_URL
</script>

<template>
  <div class="dashboard">
   <iframe
      :src="sapBiUrl"
      width="100%"
      height="600"
      style="border: none;"
    ></iframe>
  </div>
</template>