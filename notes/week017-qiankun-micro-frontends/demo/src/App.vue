<template>
  <div>
    <h1>Hello qiankun!</h1>
    <el-menu :router="true" mode="horizontal">
      <el-menu-item index="/hello">Hello</el-menu-item>
      <el-menu-item index="/about">About</el-menu-item>
      <el-menu-item index="/app1">App1</el-menu-item>
      <el-menu-item index="/app2">App2</el-menu-item>
    </el-menu>
    <router-view></router-view>
    <div id="app1"></div>
    <div id="app2"></div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
