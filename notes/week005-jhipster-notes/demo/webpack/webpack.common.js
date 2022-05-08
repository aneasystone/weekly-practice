'use strict';
const path = require('path');
const { merge } = require('webpack-merge');
const { VueLoaderPlugin } = require('vue-loader');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { hashElement } = require('folder-hash');
const MergeJsonWebpackPlugin = require('merge-jsons-webpack-plugin');

const { DefinePlugin, EnvironmentPlugin } = require('webpack');
const { vueLoaderConfig } = require('./vue.utils');
const config = require('./config');

function resolve(dir = '') {
  return path.join(__dirname, '..', dir);
}

module.exports = async (env, options) => {
  const development = options.mode === 'development';
  const languagesHash = await hashElement(resolve('src/main/webapp/i18n'), {
    algo: 'md5',
    encoding: 'hex',
    files: { include: ['*.json'] },
  });

  return merge(
    {
      mode: options.mode,
      context: resolve(),
      entry: {
        app: './src/main/webapp/app/main.ts',
      },
      output: {
        path: resolve('target/classes/static/'),
      },
      resolve: {
        extensions: ['.ts', '.js', '.vue', '.json'],
        alias: {
          vue$: 'vue/dist/vue.esm.js',
          '@': resolve('src/main/webapp/app'),
        },
      },
      devServer: {
        static: {
          directory: './target/classes/static/',
        },
        port: 9060,
        proxy: [
          {
            context: ['/api', '/services', '/management', '/v3/api-docs', '/h2-console', '/auth'],
            target: 'http://localhost:8080',
            secure: false,
          },
        ],
        historyApiFallback: true,
      },
      cache: {
        // 1. Set cache type to filesystem
        type: 'filesystem',
        cacheDirectory: resolve('target/webpack'),
        buildDependencies: {
          // 2. Add your config as buildDependency to get cache invalidation on config change
          config: [
            __filename,
            path.resolve(__dirname, 'config.js'),
            path.resolve(__dirname, 'vue.utils.js'),
            path.resolve(__dirname, `webpack.${development ? 'dev' : 'prod'}.js`),
            path.resolve(__dirname, '../.postcssrc.js'),
            path.resolve(__dirname, '../tsconfig.json'),
          ],
        },
      },
      module: {
        rules: [
          {
            test: /\.vue$/,
            loader: 'vue-loader',
            options: vueLoaderConfig(!development),
          },
          {
            test: /\.ts$/,
            use: [
              {
                loader: 'ts-loader',
                options: {
                  appendTsSuffixTo: ['\\.vue$'],
                  happyPackMode: true,
                  transpileOnly: true,
                },
              },
            ],
            include: [resolve('src'), resolve('test')],
          },
          {
            test: /\.(png|jpe?g|gif|svg|mp4|webm|ogg|mp3|wav|flac|aac|woff2?|eot|ttf|otf)/,
            type: 'asset/resource',
          },
        ],
      },
      plugins: [
        new EnvironmentPlugin({
          // Required by vuelidate https://github.com/vuelidate/vuelidate/issues/365
          BUILD: 'web',
        }),
        new DefinePlugin({
          I18N_HASH: JSON.stringify(languagesHash.hash),
          VERSION: JSON.stringify(config.version),
          SERVER_API_URL: JSON.stringify(config.serverApiUrl),
        }),
        new HtmlWebpackPlugin({
          base: '/',
          template: './src/main/webapp/index.html',
        }),
        new VueLoaderPlugin(),
        new CopyWebpackPlugin({
          patterns: [
            {
              context: './node_modules/swagger-ui-dist/',
              from: '*.{js,css,html,png}',
              to: 'swagger-ui/',
              globOptions: { ignore: ['**/index.html'] },
            },
            { from: './node_modules/axios/dist/axios.min.js', to: 'swagger-ui/' },
            { from: './src/main/webapp/swagger-ui/', to: 'swagger-ui/' },
            { from: './src/main/webapp/content/', to: 'content/' },
            { from: './src/main/webapp/favicon.ico', to: 'favicon.ico' },
            {
              from: './src/main/webapp/manifest.webapp',
              to: 'manifest.webapp',
            },
            // jhipster-needle-add-assets-to-webpack - JHipster will add/remove third-party resources in this array
            { from: './src/main/webapp/robots.txt', to: 'robots.txt' },
          ],
        }),
        new MergeJsonWebpackPlugin({
          output: {
            groupBy: [
              { pattern: './src/main/webapp/i18n/zh-cn/*.json', fileName: './i18n/zh-cn.json' },
              // jhipster-needle-i18n-language-webpack - JHipster will add/remove languages in this array
            ],
          },
        }),
      ],
    },
    await require(`./webpack.${development ? 'dev' : 'prod'}`)(env, options)
    // jhipster-needle-add-webpack-config - JHipster will add custom config
  );
};
