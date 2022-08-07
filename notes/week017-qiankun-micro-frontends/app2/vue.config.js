const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8082,
    headers:{
      'Access-Control-Allow-Origin':'*'
    }
  },
  configureWebpack:{
    output:{
      library: `app2`,
      libraryTarget: 'umd'
    }
  }
})
