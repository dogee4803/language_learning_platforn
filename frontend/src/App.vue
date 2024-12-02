<script setup>
import MenuBar from './components/MenuBar.vue';
</script>

<template>
  <div id="app">
    <MenuBar />
    <router-view></router-view> <!-- Здесь отображаются страницы -->
  </div>
</template>

<style>
</style>
