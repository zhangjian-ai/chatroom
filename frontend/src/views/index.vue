<template>
  <div class="main">
    <div class="hall"></div>
    <el-input v-model="input" placeholder="Please input" />
    <el-button type="primary" onclick="publish">发表</el-button>
  </div>
</template>
<script>
export default {
  data() {
    return {
      input: ""
    };
  },
  method: {
    publish() {
      console.log("aa");
    }
  }
};
</script>
<style scoped>
.main {
  width: 80%;
  margin-left: 10%;
}
.hall {
  height: 30em;
  border: 1px solid black;
}
.el-input {
  margin: 2% 2% 0 0;
  width: 30%;
}
</style>
