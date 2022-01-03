module.exports = {
  devServer: {
    proxy: {
      '^/user_auth': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/stock_management': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
    },
  },
  transpileDependencies: [
    'vuetify'
  ],
  productionSourceMap: false,
}
