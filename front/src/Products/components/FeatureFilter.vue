<template>
  <v-container fluid>
    <v-select
      ref="selectComponent"
      v-model="filteredFeatures"
      label="Feature"
      style="margin-top: 25px"
      :items="features"
      item-text="name"
      item-value="id"
      multiple
      @change="filterProducts"
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
              data-test="group_feature_t"
              placeholder="Search"
              @input="searchFeatures"
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
  name: 'FeatureFilter',
  props: {
    // eslint-disable-next-line vue/require-default-prop
    filters: Array,
    // eslint-disable-next-line vue/require-default-prop
    filtered: Array
  },
  data () {
    return {
      features: [],
      filteredFeatures: [],
      filterSearch: null
    };
  },
  mounted () {
    this.features = this.filters.map(x => x);
    this.filteredFeatures = this.filtered.map(x => x);
  },
  methods: {
    filterProducts () {
      this.$emit('filterProducts', this.filteredFeatures);
    },

    searchFeatures () {
      this.features = this.filters.filter(x => x.name.toUpperCase().includes(this.filterSearch.toUpperCase()));
    }
  }
};
</script>

<style scoped>

</style>
