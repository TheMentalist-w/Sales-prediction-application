<template>
  <hello-world />
</template>

<script>
import HelloWorld from '../components/HelloWorld'
import Vue from 'vue'
import Vuetify from 'vuetify'
Vue.use(Vuetify)

export default {
  name: 'Home',

  components: {
    HelloWorld
  },
  beforeMount() {
    this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === "true" ? true : false
  },
}
</script>
