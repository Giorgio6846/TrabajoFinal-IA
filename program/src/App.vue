<template>
  <formUser></formUser>
  <h1>Screen Share</h1>
  <button id="startButton">Start Screen Share</button>
</template>

<script>
import formUser from "./components/formUser.vue";

export default {
  components: {
    formUser: formUser,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
./components/form.vue
