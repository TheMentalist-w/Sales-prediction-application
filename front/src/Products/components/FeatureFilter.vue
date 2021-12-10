<template>
  <v-container fluid>
    <v-select
      style="margin-top: 25px"
      v-model="filteredFeatures"
      :items="features"
      item-text="name"
      item-value="id"
      @change="filterProducts"
      label="Feature"
      multiple
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
              @input="searchFeatures"
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
  name: "FeatureFilter",
  data() {
    return {
      features: [],
      filteredFeatures: [],
      filterSearch: null,
    }
  },
  props: {
    filters: Array,
    filtered: Array
  },
  mounted() {
    this.features = this.filters.map(x => x)
    this.filteredFeatures = this.filtered.map(x => x)
  },
  methods: {
    filterProducts() {
      this.$emit('filterProducts', this.filteredFeatures)
    },

    searchFeatures() {
      this.features = this.filters.filter(x => x.name.toUpperCase().includes(this.filterSearch.toUpperCase()))
    }
  }
}
</script>

<style scoped>

</style>
