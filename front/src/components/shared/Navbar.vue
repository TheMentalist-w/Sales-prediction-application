<template>
  <v-app-bar
    app
    color="primary"
    dark
  >
    <v-toolbar-title style="font-size: 150%">
      PITBULL
    </v-toolbar-title>
    <v-spacer />
    <v-btn
      v-if="adminLoggedIn"
      href="/accounts"
      text
      rounded
      data-test="accounts"
    >
      <span class="mr-2">Accounts</span>
    </v-btn>
    <v-btn
      v-if="loggedIn"
      href="/"
      text
      rounded
      data-test="logout"
    >
      <span class="mr-2">Stock</span>
    </v-btn>
    <v-btn
      v-if="loggedIn"
      data-test="logout"
      text
      rounded
      @click="logOut"
    >
      <span class="mr-2">Logout</span>
    </v-btn>
    <v-btn
      text
      rounded
      @click="changeTheme"
    >
      <v-icon>mdi-brightness-6</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
import VueCookies from 'vue-cookies';
import Vuetify from 'vuetify';
import Vue from 'vue';
import axios from 'axios';

Vue.use(VueCookies);
Vue.use(Vuetify);

export default {
  name: 'Navbar',
  data () {
    return {
      loggedIn: false,
      adminLoggedIn: false
    };
  },
  beforeMount () {
    axios.get('/user_auth/current/')
      .then(response => {
        this.loggedIn = true;
        if (response.data.is_superuser) {
          this.adminLoggedIn = true;
        }
      })
      .catch(error => {
        if (error.response.status === 500) {
          this.$notify({
            group: 'notifications-bottom-left',
            title: 'Error',
            text: 'Server error.Try later',
            type: 'error text-white'
          });
        }
      });
  },
  methods: {
    logOut () {
      axios.post('/user_auth/logout/')
        .then(() => {
          this.$cookies.remove('access');
          this.$cookies.remove('refresh');
          this.$router.push('/login');
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error.Try later',
              type: 'error text-white'
            });
          }
        });
    },

    changeTheme () {
      const theme = sessionStorage.getItem('pit_theme');
      if (theme) {
        theme === 'true' ? sessionStorage.setItem('pit_theme', 'false') : sessionStorage.setItem('pit_theme', 'true');
        this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === 'true';
      } else {
        sessionStorage.setItem('pit_theme', (!this.$vuetify.theme.dark).toString());
        this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === 'true';
      }
    }
  }
};
</script>
