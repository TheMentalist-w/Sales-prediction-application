<template>
  <div
    v-if="loginBox"
    :key="loggedKey"
    class="loginBox"
  >
    <v-card
      width="30%"
      class="mx-auto mt-16"
    >
      <v-card-title style="justify-content: center">
        Login
      </v-card-title>
      <v-card-text>
        <v-divider />
        <div class="mt-6" />
        <v-text-field
          v-model="email"
          :rules="[rules.required]"
          class="username"
          data-test="username"
          type="text"
          label="Username or Email"
          prepend-icon="mdi-account-circle"
          @keyup.enter="logIn"
        />
        <v-text-field
          id="password"
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          :rules="[rules.required]"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          class="password"
          data-test="password"
          label="Password"
          prepend-icon="mdi-lock"
          @keyup.enter="logIn"
          @click:append="showPassword = !showPassword"
        />
      </v-card-text>
      <v-divider class="mt-16" />
      <v-card-actions>
        <v-btn
          x-large
          class="mx-auto mt-5 success"
          @click="logIn"
        >
          Login
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue';
import axios from 'axios';
import VueCookies from 'vue-cookies';
import Notifications from 'vue-notification';
import Vuetify from 'vuetify';

Vue.use(Vuetify);
Vue.use(Notifications);
Vue.use(VueCookies);

export default {
  name: 'Login',
  data () {
    return {
      showPassword: false,
      email: null,
      password: null,
      loginBox: false,
      loggedKey: 0,
      rules: {
        required: value => !!value || 'Required.'
      }
    };
  },
  mounted () {
    const access = this.$cookies.get('access');
    const refresh = this.$cookies.get('refresh');
    if (access || refresh) {
      axios.get('/user_auth/current/')
        .then(() => {
          this.$router.push('/');
        })
        .catch(() => {
          this.$cookies.remove('access');
          this.$cookies.remove('refresh');
          this.loginBox = true;
          this.loggedKey += 1;
        });
    } else {
      this.loginBox = true;
      this.loggedKey += 1;
    }
  },
  methods: {
    logIn () {
      const data = new FormData();
      data.append('login_data', this.email);
      data.append('password', this.password);
      axios.post('/user_auth/login/', data)
        .then((response) => {
          this.$cookies.set('access', response.data.access, 60 * 30);
          this.$cookies.set('refresh', response.data.refresh, 60 * 1439);
          this.$router.push('/');
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            });
          } else {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Invalid credentials',
              type: 'error text-white'
            });
          }
        });
    }
  }
};
</script>

<style scoped>

</style>
