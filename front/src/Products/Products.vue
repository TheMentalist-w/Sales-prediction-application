<template>
  <hello-world />
</template>

<script>
import HelloWorld from '../components/HelloWorld'
import Vue from 'vue'
import Vuetify from 'vuetify'
Vue.use(Vuetify)

export default {
  name: 'Products',
  mounted() {
    let access = this.$cookies.get('access')
    let refresh = this.$cookies.get('refresh')
    if(access || refresh){
      this.getEmployees()
    }
    else {
      this.$router.push('/login')
    }
  },
  components: {
    HelloWorld
  },
}
</script>
