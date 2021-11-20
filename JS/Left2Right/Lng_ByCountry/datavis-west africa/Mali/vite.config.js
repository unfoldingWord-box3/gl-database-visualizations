const { resolve } = require('path')

module.exports = {
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        tree: resolve(__dirname, 'tree/index.html')
      }
    }
  }
}
