<template>
  <v-container fluid>
    <v-select
      style="margin-top: 25px"
      v-model="shop"
      :items="shops"
      item-text="name"
      item-value="id"
      @change="changeShop"
      label="Shop"
      ref="selectComponent"
    >
      <template v-slot:prepend-item>
        <v-list-item
          ripple
        >
          <v-list-item-action>
            <v-icon>
              mdi-magnify
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-text-field
              dense
              placeholder="Search"
              v-model="filterSearch"
              @input="searchShops"
            />
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
    </v-select>
  </v-container>
</template>

<script>
export default {
  name: "ShopFilter",
  data() {
    return {
      shops: [],
      shop: null,
      filterSearch: null,
    }
  },
  props: {
    filters: Array,
    filtered: Array
  },
  mounted() {
    this.shops = this.filters.map(x => x)
    this.shop = this.filtered
  },
  methods: {
    changeShop() {
      this.$emit('changeShop', this.shop)
    },

    searchShops() {
      this.shops = this.filters.filter(x => x.name.toUpperCase().includes(this.filterSearch.toUpperCase()))
    }
  }
}
</script>

<style scoped>

</style>
