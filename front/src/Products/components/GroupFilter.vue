<template>
  <v-container fluid>
    <v-select
      ref="selectComponent"
      v-model="filteredGroups"
      label="Group"
      style="margin-top: 25px"
      :items="groups"
      item-text="name"
      item-value="id"
      multiple
      @change="filterProducts"
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
        <v-divider class="mt-2" />
      </template>
    </v-select>
  </v-container>
</template>

<script>
export default {
  name: 'GroupFilter',
  props: {
    // eslint-disable-next-line vue/require-default-prop
    filters: Array,
    // eslint-disable-next-line vue/require-default-prop
    filtered: Array
  },
  data () {
    return {
      groups: [],
      filteredGroups: []
    };
  },
  computed: {
    checkAllFilters () {
      return this.filteredGroups.length === this.groups.length;
    },
    checkSomeFilters () {
      return this.filteredGroups.length > 0 && !this.checkAllFilters;
    },
    icon () {
      if (this.checkAllFilters) return 'mdi-close-box';
      if (this.checkSomeFilters) return 'mdi-minus-box';
      return 'mdi-checkbox-blank-outline';
    }
  },
  mounted () {
    this.groups = this.filters.map(x => x);
    this.filteredGroups = this.filtered.map(x => x);
  },
  methods: {
    filterProducts () {
      this.$emit('filterProducts', this.filteredGroups);
    },

    toggle () {
      this.$nextTick(() => {
        if (this.checkAllFilters) {
          this.filteredGroups = [];
          this.filterProducts();
        } else {
          this.filteredGroups = this.groups.slice().map(x => x.id);
          this.filterProducts();
        }
      });
    }
  }
};
</script>

<style>

</style>
