<template>
  <v-container fluid>
    <v-select
      style="margin-top: 25px"
      v-model="filteredGroups"
      :items="groups"
      item-text="name"
      item-value="id"
      @change="filterProducts"
      label="Group"
      multiple
      ref="selectComponent"
    >
      <template v-slot:prepend-item>
        <v-list-item
          ripple
          @click="toggle"
        >
          <v-list-item-action>
            <v-icon :color="filteredGroups.length > 0 ? 'green' : ''">
              {{ icon }}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              Select All
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
    </v-select>
  </v-container>
</template>

<script>
export default {
  name: "GroupFilter",
  data() {
    return {
      groups: [],
      filteredGroups: [],
    }
  },
  props: {
    filters: Array,
    filtered: Array,
  },
  mounted() {
    this.groups = this.filters.map(x => x)
    this.filteredGroups = this.filtered.map(x => x)
  },
  computed: {
    checkAllFilters() {
      return this.filteredGroups.length === this.groups.length
    },
    checkSomeFilters() {
      return this.filteredGroups.length > 0 && !this.checkAllFilters
    },
    icon() {
      if (this.checkAllFilters) return 'mdi-close-box'
      if (this.checkSomeFilters) return 'mdi-minus-box'
      return 'mdi-checkbox-blank-outline'
    },
  },
  methods: {
    filterProducts() {
      this.$emit('filterProducts', this.filteredGroups)
    },

    toggle () {
      this.$nextTick(() => {
        if (this.checkAllFilters) {
          this.filteredGroups = []
          this.filterProducts()
        } else {
          this.filteredGroups = this.groups.slice().map(x => x.id)
          this.filterProducts()
        }
      })
    },
  }
}
</script>

<style>

</style>
