const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8081,
    headers:{
      'Access-Control-Allow-Origin':'*'
    }
  },
  configureWebpack:{
    output:{
      library: `app1`,
      libraryTarget: 'umd'
    }
  }
})
