<script setup>
const odooAppUrl = import.meta.env.VITE_ODOO_APP_URL
</script>

<template>
  <div class="dashboard">
   <iframe
      :src="odooAppUrl"
      width="100%"
      height="600"
      style="border: none;"
    ></iframe>
  </div>
</template>