<template>
  <div>
    <v-data-table
      style="width: 90%"
      :headers="headers"
      :items="products"
      :hide-default-footer="true"
      loading-text="Loading... Please wait"
      class="elevation-1 mx-auto mt-16 stockTable"
      :key="stockKey"
      v-if="stockTable"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon
          class="mr-2"
          color="secondary"
          @click="productDetails(item)"
        >
          mdi-magnify
        </v-icon>
      </template>
    </v-data-table>
    <v-pagination
      class="pagination"
      v-model="page"
      :length="totalPages"
      @input="pageChange"
      circle
      total-visible="7"
      next-icon="mdi-menu-right"
      prev-icon="mdi-menu-left"
    >
    </v-pagination>
  </div>
</template>

<script>
import Vue from 'vue'
import Vuetify from 'vuetify'
import VueCookies from "vue-cookies"
import axios from 'axios'
Vue.use(Vuetify)
Vue.use(VueCookies)

export default {
  name: 'Products',
  data() {
    return {
      stockKey: 0,
      stockTable: false,
      page: 1,
      totalPages: 1,
      pageSize: 8,
      products: [],
      headers: [
        {
          text: 'Product',
          align: 'start',
          value: 'product_name',
          sortable: false,
          width: '30%'
        },
        {
          text: 'State',
          align: 'start',
          value: 'state',
          sortable: false,
          width: '30%'
        },
        {
          text: 'Predicted ',
          align: 'start',
          value: 'product_prediction',
          sortable: false,
          width: '30%'
        },
        {
          text: '',
          value: 'actions',
          align: 'end',
          sortable: false,
          width: '10%'
        },
      ],

    }
  },
  mounted() {
    let access = this.$cookies.get('access')
    let refresh = this.$cookies.get('refresh')
    if(access || refresh){
      this.getProducts()
    }
    else {
      this.$router.push('/login')
    }
  },
  methods: {
    getRequestParams(page, pageSize) {
      let params = {}
      if (page) params["page"] = page
      if (pageSize) params["size"] = pageSize

      return params
    },

    getProducts() {
      const params = this.getRequestParams(
        this.page,
        this.pageSize
      )

      axios.get('http://localhost:8000/pitbull/products/', {params: params})
        .then(response => {
          this.products = response.data.products
          this.totalPages = response.data.totalPages
          this.page = parseInt(response.data.page)
          this.stockTable = true
          this.stockKey += 1
        })
        .catch(() => {
          this.$router.push('/')
        })
    },

    pageChange(value) {
      this.page = value
      this.getEmployees()
    },

    productDetails(item) {

    },

  },
}
</script>
