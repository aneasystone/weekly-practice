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

import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import About from './components/About.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/hello', component: HelloWorld },
    { path: '/about', component: About }
  ]
})

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

createApp(App).use(router).use(ElementPlus).mount('#app')
