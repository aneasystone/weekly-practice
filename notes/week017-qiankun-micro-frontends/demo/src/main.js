import { createApp } from 'vue'
import App from './App.vue'

import { registerMicroApps, start } from 'qiankun';

registerMicroApps([{
  name: 'app1',
  entry: '//localhost:8081',
  container: '#app1',
  activeRule: '/app1'
}, {
  name: 'app2',
  entry: '//localhost:8082',
  container: '#app2',
  activeRule: '/app2'
}]);

start();

createApp(App).mount('#app')
