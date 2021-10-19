<template>
<v-content :key="loggedKey" v-if="loggedIn">
  <v-card width="30%" class="mx-auto mt-16">
    <v-card-title style="justify-content: center">Login</v-card-title>
    <v-card-text>
      <v-divider></v-divider>
      <div class="mt-6"/>
      <v-text-field
        type="text"
        label="Username or Email"
        prepend-icon="mdi-account-circle"
        v-model="email"
        :rules="[rules.required]"
      />
      <v-text-field
        :type="showPassword ? 'text' : 'password'"
        id="password"
        label="Password"
        prepend-icon="mdi-lock"
        v-model="password"
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
</v-content>
</template>

<script>
import Vue from 'vue'
import axios from "axios"
import VueCookies from 'vue-cookies'
import Notifications from 'vue-notification'
Vue.use(Notifications)
Vue.use(VueCookies)

export default {
  name: "Login",
  data() {
    return {
      showPassword: false,
      email: null,
      password: null,
      loggedIn: false,
      loggedKey: 0,
      rules: {
        required: value => !!value || 'Required.'
      },
    }
  },
  mounted() {
    let logged = this.$cookies.get('sessionid')
    if(logged){
      this.$router.push(this.$route.query.redirect || '/accounts')
    }
    else {
      this.loggedIn = true
      this.loggedKey += 1
    }
  },
  methods: {
    logIn () {
      let data = new FormData(); // 2

      data.append("username", this.email)
      data.append("password", this.password)
      axios.post('http://localhost:8000/pitbull/user/login/', data) // 4
      .then((response) => {
        console.log(response)
        this.$cookies.set('sessionid', response.headers, {
          expires: 1
        })
        this.$router.push(this.$route.query.redirect || '/accounts')
      })
      .catch(errors => this.$notify({group: 'notifications-bottom-left', title: 'Error', text:'Niepoprawne dane logowania', type: 'error text-white' })) // 6

    }
  }
}
</script>

<style scoped>

</style>
