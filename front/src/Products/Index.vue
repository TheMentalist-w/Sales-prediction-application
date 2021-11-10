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
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            @click:append="searchProducts"
            @keyup.enter="searchProducts"
            single-line
            hide-details
          ></v-text-field>        
        </v-toolbar>
      </template>

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
  name: 'Index',
  data() {
    return {
      stockKey: 0,
      stockTable: true,
      page: 1,
      totalPages: 1,
      pageSize: 8,
      search: '',
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
    getRequestParams(search, page, pageSize) {
      let params = {}
      if (search) params["search"] = search
      if (page) params["page"] = page
      if (pageSize) params["size"] = pageSize

      return params
    },

    getProducts() {
      const params = this.getRequestParams(
        this.search,
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

    searchProducts() {
      this.page = 1
      this.getProducts()
    },

    pageChange(value) {
      this.page = value
      this.getProducts()
    },

    productDetails(item) {
      this.$router.push('/product/' + item.id)
    },

  },
}
</script>
