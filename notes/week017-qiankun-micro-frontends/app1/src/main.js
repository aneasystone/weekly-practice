import { createApp } from 'vue'
import App from './App.vue'

let instance = null
function render() {
  instance = createApp(App).mount('#app')
}

if (!window.__POWERED_BY_QIANKUN__) { // 默认独立运行
  render();
}

export async function bootstrap(props) {
  console.log('bootstrap app1', props)
}
export async function mount(props) {
  console.log('mount app1', props)
  render()
}
export async function unmount(props) {
  console.log('unmount app1', props)
  console.log(instance)
}
