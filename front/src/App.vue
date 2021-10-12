<template>
  <v-app>
    <Navbar/>
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
  data: () => ({
    max:3
  })
}
</script>
