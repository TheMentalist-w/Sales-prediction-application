module.exports = {
  devServer: {
    proxy: {
      '^/pitbull': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  transpileDependencies: [
    'vuetify'
  ]
}
