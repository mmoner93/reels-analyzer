<script setup lang="ts">
import TasksView from './views/TasksView.vue'
</script>

<template>
  <div id="app">
    <TasksView />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
}
</style>
