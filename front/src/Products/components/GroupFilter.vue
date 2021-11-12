<template>
  <v-card>
    <v-card-title class="text-h5">Filter options</v-card-title>
    <v-card-text>
      <v-container>
        <v-col>
          <v-checkbox
            label="All"
            v-model="isCheckAll"
            @click="checkAll"
            color="primary"
            hide-details
          ></v-checkbox>
        </v-col>
        <v-col
          v-for="group in showGroups"
          :key="group.title"
        >
          <v-checkbox
            :label="group.title"
            v-model="group.checked"
            @change='updateCheckall'
            color="primary"
            hide-details
          ></v-checkbox>
        </v-col>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="red darken-1" rounded text @click="closeFilter">Cancel</v-btn>
      <v-btn color="green darken-1" rounded text @click="filterProducts">Filter</v-btn>
      <v-spacer></v-spacer>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "GroupFilter",
  data() {
    return {
      isCheckAll: false,
      checked: [],
      showGroups: [],
    }
  },
  props: {
    groups: Array,
  },
  mounted() {
    this.checked = this.groups.filter(x => x.checked)
    this.showGroups = JSON.parse(JSON.stringify(this.groups));
    this.updateCheckall()
  },
  methods: {
    updateCheckall() {
      let check = this.showGroups.every(x => x.checked)
      this.isCheckAll = !!check
    },

    checkAll() {
      if(this.isCheckAll) {
        this.showGroups = this.showGroups.map(x => Object({title: x.title, checked: true}))
      }
    },

    filterProducts() {
      this.checked = this.showGroups.filter(x => x.checked)
      this.$emit('filterProducts', this.checked)
    },

    closeFilter() {
      this.$emit('closeFilter')
    }
  }
}
</script>

<style scoped>

</style>
