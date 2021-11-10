<template>
  <v-form ref="form">
    <p class="title">用 户 登 录</p>
    <v-text-field v-model="username" label="User Name" :rules="rules[0]" outlined dense required></v-text-field>
    <v-text-field
      v-model="password"
      label="Password"
      type="password"
      :rules="rules[1]"
      outlined
      dense
      required
    ></v-text-field>

    <div style="text-align: right;">
      <v-btn color="primary" @click="submit()" small>Submit</v-btn>
      <v-btn @click="$emit('update:show', false)" small>Cancel</v-btn>
    </div>
  </v-form>
</template>

<script>
import { userLogin } from "@/api";
export default {
  data() {
    return {
      username: "",
      password: "",

      rules: [
        [v => !!v || "username is required"],
        [v => !!v || "password is required"]
      ]
    };
  },

  methods: {
    // 提交
    submit() {
      // 表单校验
      if (this.$refs.form.validate()) {
        // 登录操作
        userLogin({
          username: this.username,
          password: this.password
        }).then(res => {
          // 用户信息持久保存
          this.$store.commit("setUserInfo", res.data);

          // 清空注册表单，并关闭弹窗
          this.$refs.form.reset();
          this.$emit("update:show", false);
        });
      }
    }
  }
};
</script>
<style scoped>
.title {
  font-size: 1.5em !important;
  font-weight: bolder;
  color: red;
  text-align: center;
}
.v-form {
  padding: 1em 2em 2em;
  background-color: whitesmoke;
}
.v-btn {
  margin: 0 1em;
}
</style>