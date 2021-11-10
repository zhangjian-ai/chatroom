<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar dark color="teal">
        <v-col offset="2" md="1">
          <v-toolbar-title>Search</v-toolbar-title>
        </v-col>
        <v-col md="6" sm="8" align-self="auto">
          <v-text-field v-model="search" label="What are you want to search?" flat></v-text-field>
        </v-col>
        <v-col md="1">
          <v-btn icon>
            <v-icon>mdi-send</v-icon>
          </v-btn>
        </v-col>
      </v-toolbar>
    </v-app-bar>
    <v-main>
      <v-container>
        <v-col offset-md="2" offset-lg="3" md="8" lg="6" id="news" ref="news"></v-col>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      loading: false,
      search: null
    };
  },
  methods: {
    queryState(val) {
      console.log(val);
    }
  },
  watch: {
    search(val) {
      val && this.queryState(val);
    }
  }
};
</script>
<style scoped>
.v-text-field {
  margin-top: 2em !important;
}
</style>