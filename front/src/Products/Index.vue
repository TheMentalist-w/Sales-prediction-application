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
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                dark
                rounded
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Filter
              </v-btn>
            </template>
            <GroupFilter
              @closeFilter="closeFilter"
              @filterProducts="filterProducts"
              :groups="groups"
              :key="dialogKey"
            />
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.product_group="{ item }">
        <v-btn
          class="mr-2"
          color="primary"
          rounded
        >
          {{ item.product_group }}
        </v-btn>
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
import GroupFilter from "./components/GroupFilter"
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
      dialog: false,
      dialogKey: 0,
      products: [],
      groups: [],
      filteredGroups: [],
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
          text: 'Predicted',
          align: 'start',
          value: 'product_prediction',
          sortable: false,
          width: '30%'
        },
        {
          text: 'Group',
          align: 'start',
          value: 'product_group',
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
  components: {
    GroupFilter
  },
  watch: {
    dialog (val) {
      val || this.closeFilter()
    },
  },
  async mounted () {
    let access = this.$cookies.get('access')
    let refresh = this.$cookies.get('refresh')
    if(access || refresh){
      await this.getGroups()
      await this.getProducts()
    }
    else {
      await this.$router.push('/login')
    }
  },
  methods: {
    getRequestParams(search, page, pageSize, filteredGroups) {
      let params = {}
      if (search) params["search"] = search
      if (page) params["page"] = page
      if (pageSize) params["size"] = pageSize
      if (filteredGroups) params["filteredGroups"] = filteredGroups

      return params
    },

    getGroups() {
      axios.get('http://localhost:8000/pitbull/products/groups')
        .then(response => {
          this.groups = response.data.groups.map(x => Object({title: x, checked: false}))
          this.filteredGroups = response.data.groups
        })
    },

    getProducts() {
      const params = this.getRequestParams(
        this.search,
        this.page,
        this.pageSize,
        this.filteredGroups
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
          this.$router.push('/login')
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

    filterProducts(filters) {
      this.page = 1
      this.filteredGroups = filters.map(x => x.title)
      this.groups = this.groups.map(x => {
        let check = filters.find(y => y.title === x.title)
        if(check) {
          return Object({title: x.title, checked: true})
        } else {
          return Object({title: x.title, checked: false})
        }
      })
      this.getProducts()
      this.closeFilter()
    },

    closeFilter() {
      this.dialog = false
      this.dialogKey += 1
    }
  },
}
</script>
