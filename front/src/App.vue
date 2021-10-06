<template>
  <v-app>
    <Navbar/>
    <v-main>
      <router-view/>
    </v-main>
    <Footer/>
  </v-app>
</template>

<script>
import Navbar from './components/shared/Navbar';
import Footer from "./components/shared/Footer";

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
  },
  data: () => ({
  })
}
</script>
