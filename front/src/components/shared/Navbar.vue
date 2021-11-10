<template>
  <v-app-bar
    app
    color="primary"
    dark
  >
      <v-toolbar-title style="font-size: 150%">PITBULL</v-toolbar-title>

    <v-spacer></v-spacer>
    <v-btn
      href="/accounts"
      text
      rounded
      v-if="adminLoggedIn"
      data-test="accounts"
    >
      <span class="mr-2">Accounts</span>
    </v-btn>
    <v-btn
      href="/"
      text
      rounded
      v-if="loggedIn"
      data-test="logout"
    >
      <span class="mr-2">Stock</span>
    </v-btn>
    <v-btn
      text
      rounded
      @click="logOut"
      v-if="loggedIn"
      data-test="logout"
    >
      <span class="mr-2">Logout</span>
    </v-btn>
    <v-btn
      @click="changeTheme"
      text
      rounded
    >
      <v-icon>mdi-brightness-6</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
import VueCookies from 'vue-cookies'
import Vuetify from 'vuetify'
import Vue from 'vue'
import axios from 'axios'
Vue.use(VueCookies)
Vue.use(Vuetify)

export default {
  name: 'Navbar',
  data() {
    return {
      loggedIn: false,
      adminLoggedIn: false,
    }
  },
  beforeMount() {
    axios.get('http://localhost:8000/pitbull/user/current/')
      .then(response => {
        this.loggedIn = true
        if(response.data.is_superuser) {
          this.adminLoggedIn = true
        }
      })
  },
  methods: {
    logOut() {
      axios.post('http://localhost:8000/pitbull/user/logout/')
        .then(() => {
          this.$cookies.remove('access')
          this.$cookies.remove('refresh')
          this.$router.push('/login')
        })
    },
    changeTheme() {
      let theme = sessionStorage.getItem('pit_theme')
      if(theme) {
        theme === "true" ? sessionStorage.setItem('pit_theme', "false") : sessionStorage.setItem('pit_theme', "true")
        this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === "true"
      }
      else {
        sessionStorage.setItem('pit_theme', (!this.$vuetify.theme.dark).toString())
        this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === "true"
      }
    }
  }
}
</script>
