<template>
<v-content>
  <v-card width="30%" class="mx-auto mt-16">
    <v-card-title style="justify-content: center">Login</v-card-title>
    <v-card-text>
      <v-divider></v-divider>
      <div class="mt-6"/>
      <v-text-field
        type="email"
        label="Email"
        prepend-icon="mdi-account-circle"
        v-model="email"
        :rules="[rules.required, rules.email]"
      />
      <v-text-field
        :type="showPassword ? 'text' : 'password'"
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
      <v-btn x-large class="mx-auto mt-5 success">Login</v-btn>
    </v-card-actions>
  </v-card>
</v-content>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      showPassword: false,
      email: null,
      password: null,
      rules: {
        required: value => !!value || 'Required.',
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail.'
        },
      },
    }
  }
}
</script>

<style scoped>

</style>
