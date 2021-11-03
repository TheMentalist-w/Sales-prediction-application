import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)
import colors from 'vuetify/lib/util/colors'
export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.green,
        secondary: colors.green,
        accent: colors.shades.black,
        error: colors.red.accent3,
      },
      dark: {
        primary: colors.grey.darken2,
        secondary: colors.shades.white
      },
    },
  },
})
