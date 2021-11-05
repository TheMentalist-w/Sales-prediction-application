<template>
<div :key="loggedKey" v-if="loginBox">
  <v-card width="30%" class="mx-auto mt-16">
    <v-card-title style="justify-content: center">Login</v-card-title>
    <v-card-text>
      <v-divider></v-divider>
      <div class="mt-6"/>
      <v-text-field
        class="username"
        type="text"
        label="Username or Email"
        prepend-icon="mdi-account-circle"
        v-model="email"
        @keyup.enter="logIn"
        :rules="[rules.required]"
      />
      <v-text-field
        :type="showPassword ? 'text' : 'password'"
        id="password"
        label="Password"
        prepend-icon="mdi-lock"
        v-model="password"
        @keyup.enter="logIn"
        :rules="[rules.required]"
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="showPassword = !showPassword"
      />
    </v-card-text>
    <v-divider class="mt-16"></v-divider>
    <v-card-actions>
      <v-btn x-large class="mx-auto mt-5 success" @click="logIn">Login</v-btn>
    </v-card-actions>
  </v-card>
</div>
</template>

<script>
import Vue from 'vue'
import axios from "axios"
import VueCookies from 'vue-cookies'
import Notifications from 'vue-notification'
import Vuetify from 'vuetify'
Vue.use(Vuetify)
Vue.use(Notifications)
Vue.use(VueCookies)

export default {
  name: "Login",
  data() {
    return {
      showPassword: false,
      email: null,
      password: null,
      loginBox: true,
      loggedKey: 0,
      rules: {
        required: value => !!value || 'Required.'
      },
    }
  },
  mounted() {
    let access = this.$cookies.get('access')
    let refresh = this.$cookies.get('refresh')
    if(access || refresh){
      axios.get('http://localhost:8000/pitbull/user/current/')
      .then((response) => {
        this.$router.push('/')
      })
      .catch(() => {
        this.$cookies.remove('access')
        this.$cookies.remove('refresh')
        this.loginBox = true
        this.loggedKey += 1
      })
    }
    else {
      this.loginBox = true
      this.loggedKey += 1
    }
  },
  methods: {
    logIn () {
      let data = new FormData(); // 2
      data.append("login_data", this.email)
      data.append("password", this.password)
      axios.post('http://localhost:8000/pitbull/user/login/', data)
      .then((response) => {
        this.$cookies.set('access', response.data.access, 60 * 30)
        this.$cookies.set('refresh', response.data.refresh, 60 * 1439)
        this.$router.push('/')
      })
      .catch(() => this.$notify({
        group: 'notifications-bottom-left',
        title: 'Error',
        text: 'Invalid credentials',
        type: 'error text-white'
        })
      )
    }
  }
}
</script>

<style scoped>

</style>
