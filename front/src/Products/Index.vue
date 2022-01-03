<template>
  <div style="display: flex; flex-direction: column; height: 100%">
    <v-container fluid :style="layoutStyle">
      <v-layout column>
        <v-flex>
          <v-data-table

            style="width: 90%"
            :headers="headers"
            :items="products"
            :hide-default-footer="true"
            :disable-pagination="true"
            loading-text="Loading... Please wait"
            class="elevation-1 mx-auto mt-16 stockTable"
            :key="stockKey"
            v-if="stockTable"
            :loading="loading"
          >
            <template v-slot:top>
              <v-toolbar
                flat
              >
                <v-text-field
                  style="margin-top: 3px;"
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  @click:append="searchProducts"
                  @keyup.enter="searchProducts"
                  single-line
                  hide-details
                ></v-text-field>
                <v-col
                  cols="2"
                >
                  <FeatureFilter
                    :key="featureKey"
                    :filters="features"
                    :filtered="filteredFeatures"
                    @filterProducts="filterFeatures"
                  />
                </v-col>
                <v-col
                  cols="2"
                >
                  <GroupFilter
                    :key="filterKey"
                    :filters="groups"
                    :filtered="filteredGroups"
                    @filterProducts="filterProducts"
                  />
                </v-col>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>

                <v-select
                  style="margin-top: 25px; width: 1%"
                  v-model="pageSize"
                  :items="pageSizes"
                  @change="changePageSize"
                  label="Items on page"
                >
                </v-select>
              </v-toolbar>
            </template>
            <template v-slot:header.prediction="{ header }">
              {{ header.text }}<v-btn x-small text @click="sortByDesc"><v-icon>{{arrow}}</v-icon></v-btn>
            </template>
            <template v-slot:item.group_name="{ item }">
              <v-btn
                class="mr-2"
                color="primary"
                rounded
              >
                {{ item.group_name }}
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
        </v-flex>
      </v-layout>
    </v-container>
    <v-pagination
      style="align-items: flex-end"
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
import FeatureFilter from "./components/FeatureFilter"

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
      pageSize: 10,
      pageSizes: [10, 25, 50, 100],
      layoutStyle: 'height: 100%',
      search: '',
      products: [],
      groups: [],
      filteredGroups: [],
      filterKey: 0,
      features: [],
      filteredFeatures: [],
      featureKey: 0,
      sort: -1,
      loading: true,
      headers: [
        {
          text: 'Symbol',
          align: 'start',
          value: 'symbol',
          sortable: false,
          width: '20%'
        },
        {
          text: 'Product',
          align: 'start',
          value: 'name',
          sortable: false,
          width: '40%'
        },
        {
          text: 'State',
          align: 'start',
          value: 'inventory',
          sortable: false,
          width: '20%'
        },
        {
          text: 'Predicted',
          align: 'start',
          value: 'prediction',
          sortable: false,
          width: '40%'
        },
        {
          text: 'Group',
          align: 'start',
          value: 'group_name',
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
  async mounted () {
    let access = this.$cookies.get('access')
    let refresh = this.$cookies.get('refresh')
    if(access || refresh){
      await this.getGroups()
      await this.getFeatures()
      await this.getProducts()
    }
    else {
      this.$router.push('/login')
    }
  },
  components: {
    GroupFilter, FeatureFilter
  },
  computed: {
    arrow() {
      if (this.sort === 1) {
        return 'mdi-sort-numeric-ascending-variant'
      } else if (this.sort === 0) {
        return 'mdi-sort-numeric-descending-variant'
      } else {
        return 'mdi-sort-numeric-variant'
      }
    }
  },
  methods: {
    getRequestParams(search, page, pageSize, filteredGroups, filteredFeatures, sort) {
      let params = {}
      if (search) params["search"] = search
      if (page) params["page"] = page
      if (pageSize) params["size"] = pageSize
      if (filteredGroups) params["filteredGroups"] = filteredGroups
      if (filteredFeatures) params["filteredFeatures"] = filteredFeatures
      params["sort"] = sort

      return params
    },

    getGroups() {
      axios.get('/stock_management/products/groups/')
        .then(response => {
          this.groups = response.data.groups
          this.filterKey += 1
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            })
          }
        })
    },

    getFeatures() {
      axios.get('/stock_management/products/features/')
        .then(response => {
          this.features = response.data.features
          this.featureKey += 1
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            })
          }
        })
    },

    getProducts() {
      this.loading = true
      const params = this.getRequestParams(
        this.search,
        this.page,
        this.pageSize,
        this.filteredGroups,
        this.filteredFeatures,
        this.sort
      )
      axios.get('/stock_management/products/', {params: params})
        .then(response => {
          this.products = response.data.products
          this.totalPages = response.data.totalPages
          this.page = parseInt(response.data.page)
          this.stockTable = true
          this.loading = false
          this.stockKey += 1
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            })
          }
          else {
            this.$router.push('/login')
          }
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

    filterProducts(item) {
      this.page = 1
      this.filteredGroups = item
      this.getProducts()
    },

    filterFeatures(item) {
      this.page = 1
      this.filteredFeatures = item
      this.getProducts()
    },

    sortByDesc() {
      //none - (-1), asc - 0, desc - 1
      if(this.sort === -1) {
        this.sort = 0
      } else if(this.sort === 0) {
        this.sort = 1
      } else {
        this.sort = -1
      }
      this.getProducts()
    },

    changePageSize() {
      this.getProducts()
    }
  },
}
</script>

<style>
.v-select__selections {
  display: contents;
}

#data {
  overflow: auto;
}
</style>
