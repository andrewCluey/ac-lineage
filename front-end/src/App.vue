<script setup>
import { RouterLink, RouterView } from 'vue-router'
import TheNavbar from './components/TheNavbar.vue';
import "bootstrap"
import "bootstrap-icons/font/bootstrap-icons.css"
import "bootstrap/dist/css/bootstrap.min.css"
</script>

<template>
  <header>
    <TheNavbar />
  </header>
  <div>
    <RouterView />
  </div>
</template>

<style>
.body {
  font-family: Ubuntu, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

</style>
