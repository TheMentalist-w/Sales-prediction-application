<template>
  <v-container fluid>
    <v-select
      ref="selectComponent"
      v-model="shop"
      label="Shop"
      style="margin-top: 25px"
      :items="shops"
      item-text="name"
      item-value="id"
      @change="changeShop"
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
              v-model="filterSearch"
              dense
              placeholder="Search"
              @input="searchShops"
            />
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2" />
      </template>
    </v-select>
  </v-container>
</template>

<script>
export default {
  name: 'ShopFilter',
  props: {
    // eslint-disable-next-line vue/require-default-prop
    filters: Array,
    // eslint-disable-next-line vue/require-default-prop
    filtered: Number
  },
  data () {
    return {
      shops: [],
      shop: null,
      filterSearch: null
    };
  },
  mounted () {
    this.shops = this.filters.map(x => x);
    this.shop = this.filtered;
  },
  methods: {
    changeShop () {
      this.$emit('changeShop', this.shop);
    },

    searchShops () {
      this.shops = this.filters.filter(x => x.name.toUpperCase().includes(this.filterSearch.toUpperCase()));
    }
  }
};
</script>

<style scoped>

</style>
