module.exports = {
  devServer: {
    proxy: {
      '^/user_authorization': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/stock_management': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
    }
  },
  transpileDependencies: [
    'vuetify'
  ]
}
