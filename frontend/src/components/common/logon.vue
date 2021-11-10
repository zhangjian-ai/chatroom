<template>
  <v-form ref="form">
    <p class="title">用 户 注 册</p>
    <v-text-field v-model="Form.username" label="账号" :rules="rules[0]" dense></v-text-field>
    <v-text-field v-model="Form.nickname" label="昵称" :rules="rules[1]" dense></v-text-field>
    <v-text-field v-model="Form.password" label="密码" type="password" :rules="rules[2]" dense></v-text-field>
    <v-text-field v-model="Form.confirm" label="确认密码" type="password" :rules="rules[3]" dense></v-text-field>
    <v-text-field v-model="Form.mobile" label="手机号" :rules="rules[4]" dense></v-text-field>
    <v-select
      v-model="Form.grade"
      :items="items"
      item-text="text"
      item-value="id"
      label="职级"
      :rules="rules[5]"
      dense
    ></v-select>
    <div style="text-align: right;">
      <v-btn color="primary" @click="submit()" small>Submit</v-btn>
      <v-btn @click="$emit('update:show', false)" small>Cancel</v-btn>
    </div>
  </v-form>
</template>

<script>
import { userLogon } from "@/api";
export default {
  data() {
    return {
      Form: {},
      items: [],

      rules: [
        [v => !!v || "username is required"],
        [v => !!v || "nickname is required"],
        [v => !!v || "password is required"],
        [
          v => !!v || "confirm password is required",
          v => {
            if (v === this.Form.password) {
              return true;
            }
            return "check whether the two passwords are consistent";
          }
        ],
        [
          v => !!v || "mobile is required",
          v => {
            let patt = /1[3-9]\d{9}/;
            if (patt.test(v)) {
              return true;
            }
            return "the mobile number format error";
          }
        ],
        [v => !!v || "grade is required"]
      ]
    };
  },

  methods: {
    // 提交
    submit() {
      // 表单校验
      if (this.$refs.form.validate()) {
        // 注册
        userLogon(this.Form).then(res => {
          // 用户信息持久保存
          this.$store.commit("setUserInfo", res.data);

          // 清空注册表单，并关闭弹窗
          this.$refs.form.reset();
          this.$emit("update:show", false);
        });
      }
    }
  },

  mounted() {
    this.items = this.$store.state.constance.grade;
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
.v-text-field {
  margin: 1.5em;
}
</style>