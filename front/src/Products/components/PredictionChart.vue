<template>
  <div>
    <v-select
      :items="shops"
      item-value="id"
      item-text="name"
      v-model="selectedShop"
      label="Shop"
    >
    </v-select>
    <line-chart :data="chartData" :colors="['#4CAF50']"></line-chart>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "PredictionChart",
  data() {
    return {
      chartData: {
        '2017-05-01': 2, '2017-05-02': 5, '2017-05-03': 2, '2017-05-04': 5, '2017-05-05': 2, '2017-05-06': 5, '2017-05-07': 2,
        '2017-05-08': 5, '2017-05-09': 2, '2017-05-10': 5, '2017-05-11': 2, '2017-05-12': 5, '2017-05-13': 2, '2017-05-14': 5,
        '2017-05-15': 2, '2017-05-16': 5, '2017-05-17': 2, '2017-05-18': 5, '2017-05-19': 2, '2017-05-20': 5, '2017-05-21': 2,
        '2017-05-22': 5, '2017-05-23': 2, '2017-05-24': 5, '2017-05-25': 2, '2017-05-26': 5, '2017-05-27': 2, '2017-05-28': 5,
        '2017-05-29': 2, '2017-05-30': 5, '2017-05-31': 2},
      shops: [{id: 1, name: 'raz'}, {id:2, name:'dwa'}],
      selectedShop: '',
    }
  },
  async mounted() {
    await this.getShops()
    await this.getPredictionHistory()
  },
  components: {

  },
  watch: {
    selectedShop() {
      this.getPredictionHistory()
    }
  },
  methods: {
    getShops() {
      axios.get('/pitbull/shops/')
      .then(response => {
        this.shops = response.data.shops
        this.selectedShop = response.data.shops[0]
      })
    },

    getPredictionHistory() {
      const params = {
        'shopId': this.selectedShop,
        'productId': this.$route.params.id
      }
      axios.get('/pitbull/prediction/history/', {params: params})
      .then(response => {
        //assign data to chart
        this.chartData = response.data.history
      })
    }
  }
}
</script>

<style scoped>

</style>
