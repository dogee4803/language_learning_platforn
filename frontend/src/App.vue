<script setup>
import MenuBar from '@/components/MenuBar.vue';
import AppHeader from '@/components/AppHeader.vue';
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    <MenuBar />
    <main class="py-6">
      <router-view></router-view> <!-- Здесь отображаются страницы -->
    </main>
  </div>
</template>

<style>
</style>
