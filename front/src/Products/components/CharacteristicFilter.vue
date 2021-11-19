<template>
  <v-container fluid>
    <v-select
      style="margin-top: 25px"
      v-model="filteredCharacteristics"
      :items="characteristics"
      @change="filterProducts"
      label="Filter"
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
              @input="searchCharacteristics"
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
  name: "CharacteristicFilter",
  data() {
    return {
      characteristics: [],
      filteredCharacteristics: [],
      filterSearch: null,
    }
  },
  props: {
    filters: Array,
    filtered: Array
  },
  mounted() {
    this.characteristics = this.filters.map(x => x)
    this.filteredCharacteristics = this.filtered.map(x => x)
  },
  methods: {
    filterProducts() {
      this.$emit('filterProducts', this.filteredCharacteristics)
    },

    searchCharacteristics() {
      console.log("change")
      this.characteristics = this.filters.filter(x => x.includes(this.filterSearch))
    }
  }
}
</script>

<style scoped>

</style>
