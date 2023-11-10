<script setup>
import { RouterLink, RouterView } from 'vue-router'
import SearchView from './views/SearchView.vue'
import axios from 'axios'


</script>

<template>
    <div>
      <nav>
        <h3>MyTube</h3>
        <p>Home</p>
        <RouterLink :to="{ name: 'search' }">Search</RouterLink>
        <p>Later</p>
        <p>Channel</p>
      </nav>
      <RouterView/>
    </div>
</template>

<style>

</style>
