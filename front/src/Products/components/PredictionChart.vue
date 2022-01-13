<template>
  <div>
    <ShopFilter
      :key="shopKey"
      :filters="shops"
      :filtered="selectedShop"
      @changeShop="changeShop"
    />
    <line-chart
      :key="chartKey"
      :data="chartData"
      :colors="['#4CAF50']"
    />
  </div>
</template>

<script>
import axios from 'axios';
import ShopFilter from './ShopFilter';

export default {
  name: 'PredictionChart',
  components: {
    ShopFilter
  },
  data () {
    return {
      chartData: null,
      shops: [],
      selectedShop: null,
      shopKey: 0,
      chartKey: 0
    };
  },
  async mounted () {
    await this.getShops();
  },
  methods: {
    getShops () {
      const params = {
        productId: this.$route.params.id
      };
      axios.get('/stock_management/shops/', { params: params })
        .then(response => {
          this.shops = response.data.shops;
          this.selectedShop = response.data.shops[0].id;
          this.shopKey += 1;
          this.getPredictionHistory();
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            });
          }
        });
    },

    getPredictionHistory () {
      const params = {
        shopId: this.selectedShop,
        productId: this.$route.params.id
      };
      axios.get('/stock_management/product/prediction_history/', { params: params })
        .then(response => {
        // assign data to chart
          this.chartData = response.data.history;
          this.chartKey += 1;
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            });
          }
        });
    },

    changeShop (value) {
      this.selectedShop = value;
      this.getPredictionHistory();
    }
  }
};
</script>

<style scoped>

</style>
