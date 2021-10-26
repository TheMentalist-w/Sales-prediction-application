<template>
  <v-app>
    <Navbar :key="navbarKey" />
    <v-main>
      <router-view/>
    </v-main>
    <notifications group="notifications-bottom-left" position="bottom left" :max="max"/>
    <Footer/>
  </v-app>
</template>

<script>
import Vue from 'vue'
import Notifications from 'vue-notification'
import Navbar from './components/shared/Navbar';
import Footer from "./components/shared/Footer";
Vue.use(Notifications)

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      max:3,
      navbarKey: 0
    }
  },
  watch: {
    $route: function() {
      this.navbarKey += 1
    }
  },
  beforeMount() {
    this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === "true" ? true : false
  },
}
</script>
