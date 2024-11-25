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
nav {
    margin-bottom: 20px;
}
nav a {
    margin-right: 15px;
    text-decoration: none;
    color: blue;
}
</style>
