import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Chart } from 'chart.js';
import Chartkick from 'vue-chartkick';
Vue.use(Chartkick.use(Chart));
Vue.config.productionTip = false;

axios.interceptors.request.use(
  config => {
    const token = Cookies.get('access');
    if (token) {
      config.headers.Authorization = 'Bearer ' + token;
    }
    return config;
  },
  error => {
    Promise.reject(error);
  });

axios.interceptors.response.use((response) => {
  return response;
},
function (error) {
  const originalRequest = error.config;
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    return axios.post('/user_auth/user/login/refresh/',
      {
        refresh: Cookies.get('refresh')
      })
      .then(res => {
        if (res.status === 200) {
          Cookies.set('access', res.data.access, { expires: 1 });
          axios.defaults.headers.common.Authorization = 'Bearer ' + Cookies.get('access');
          return axios(originalRequest);
        }
      });
  }
  return Promise.reject(error);
});

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
