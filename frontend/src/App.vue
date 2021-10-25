<template>
  <!-- vuetify组件需要使用该标签，以实现对组件库样式的使用 -->
  <v-app id="app">
    <router-view v-wechat-title="$route.meta.title" />
  </v-app>
</template>