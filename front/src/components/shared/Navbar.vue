<template>
  <v-app-bar
    app
    color="primary"
    dark
  >
    <div class="d-flex align-center">
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
        transition="scale-transition"
        width="40"
      />

      <v-toolbar-title style="font-size: 150%">PITBULL</v-toolbar-title>
    </div>

    <v-spacer></v-spacer>
    <v-btn
      href="/accounts"
      text
      rounded
    >
      <span class="mr-2">Accounts</span>
    </v-btn>
    <v-btn
      @click="$vuetify.theme.dark = !$vuetify.theme.dark"
      text
      rounded
    >
      <v-icon>mdi-brightness-6</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>

export default {
  name: 'Navbar',
  data: () => ({
    //
  })
}
</script>
