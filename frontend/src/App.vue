<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
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
