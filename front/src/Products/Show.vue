<template>
    <div :key="cardKey" v-if="show">
      <v-card width="80%" class="mx-auto mt-16">
        <v-card-title style="justify-content: left">{{product.name}}</v-card-title>
        <v-card-text>
          <v-divider></v-divider>
          <v-container>
            <v-row>
              <v-col sm="2" md="3">
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title>Symbol</v-list-item-title>
                    <v-list-item-subtitle>{{ product.symbol }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title>Name</v-list-item-title>
                    <v-list-item-subtitle>{{ product.name }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title>State</v-list-item-title>
                    <v-list-item-subtitle>{{ product.inventory }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title>Group</v-list-item-title>
                    <v-list-item-subtitle>{{ product.group }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title>Features</v-list-item-title>
                    <v-list-item-subtitle>
                      <ul>
                        <li v-for="feature in product.features" :key="feature.id">{{ feature.name }}</li>
                      </ul>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              <v-col sm="1" md="1"><v-divider vertical></v-divider></v-col>
              <v-col sm="7" md="8">
                <PredictionChart />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </div>
</template>

<script>
import axios from "axios"
import PredictionChart from "./components/PredictionChart"

export default {
    name: 'Show',
    data() {
        return {
          show: false,
          cardKey: 0,
          product: {
            symbol: 'Tw_Bl',
            name: 'Bluza',
            inventory: 200,
            group: 'Odzież',
            features: [
              {
                id: 1,
                name: 'S'
              },
              {
                id: 2,
                name: 'zielona'
              },
              {
                id: 3,
                name: 'kaptur'
              },
            ]
          }
        }
    },
    mounted () {
      let access = this.$cookies.get('access')
      let refresh = this.$cookies.get('refresh')
      if(access || refresh){
        this.getProduct()
      }
      else {
        this.$router.push('/login')
      }
    },
    components: {
      PredictionChart
    },
    methods: {
      getProduct() {
        axios.get(`/stock_management/product/${this.$route.params.id}`)
        .then(response => {
          this.product = Object.assign({}, response.data)
          this.show = true
          this.cardKey += 1
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            })
          }
        })
      },
    }

}
</script>
