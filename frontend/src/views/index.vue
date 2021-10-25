<template>
  <div>
    <v-app-bar app>
      <v-row>
        <v-col cols="7">
          <v-img max-height="60" max-width="400" src="@/assets/banner.gif"></v-img>
        </v-col>
        <v-col cols="2">
          <p class="user" v-show="$store.state.status">欢迎回来【{{ $store.state.nickname }}】</p>
        </v-col>
        <v-col cols="3">
          <v-btn
            :disabled="$store.state.status"
            color="blue"
            text
            @click="loginDialog = !loginDialog"
          >登陆</v-btn>
          <v-btn :disabled="$store.state.status" text @click="logonDialog = !logonDialog">注册</v-btn>
          <v-btn :disabled="!$store.state.status" text @click="$store.commit('setUserInfo')">注销</v-btn>
        </v-col>
      </v-row>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <!-- 登陆对话框 -->
        <v-dialog v-model="loginDialog" hide-overlay persistent max-width="25em">
          <login :show.sync="loginDialog"></login>
        </v-dialog>
        <!-- 注册对话框 -->
        <v-dialog v-model="logonDialog" hide-overlay persistent max-width="25em">
          <logon :show.sync="logonDialog"></logon>
        </v-dialog>
        <!-- 聊天室 -->
        <v-row class="fill-height" align="center">
          <template v-for="(item, i) in items">
            <v-col :key="i" cols="12" md="3">
              <v-hover v-slot="{ hover }">
                <v-card :elevation="hover ? 12 : 2" :class="{ 'on-hover': hover }">
                  <v-img :src="item.img" height="12em">
                    <v-card-title class="text-h6 red--text">
                      <v-row class="fill-height flex-column" justify="space-between">
                        <p class="mt-4 subheading text-left">{{ item.title }}</p>
                        <div>
                          <p
                            class="ma-0 text-body-1 font-weight-bold font-italic text-left"
                          >{{ item.text }}</p>
                          <p
                            class="text-caption font-weight-medium font-italic text-left"
                          >{{ item.subtext }}</p>
                        </div>

                        <div class="align-self-center">
                          <v-btn
                            :class="{ 'show-btns': hover }"
                            :color="transparent"
                            icon
                            @click="$router.push({path: '/chat_room', query: {id: 123}})"
                          >
                            <v-icon :class="{ 'show-btns': hover }" :color="transparent">mdi-play</v-icon>
                          </v-btn>
                        </div>
                      </v-row>
                    </v-card-title>
                  </v-img>
                </v-card>
              </v-hover>
            </v-col>
          </template>
        </v-row>
        <!-- 工作流 -->
      </v-container>
    </v-main>

    <v-footer app></v-footer>
  </div>
</template>

<script>
import login from "@/components/common/login.vue";
import logon from "@/components/common/logon.vue";

export default {
  data() {
    return {
      items: [
        {
          title: "故事会",
          text: "激情聊天室",
          subtext: "今日话题：王老五的前世今生...",
          img: require("@/assets/image.jpeg")
        }
      ],
      transparent: "rgba(255, 255, 255, 0)",

      // 登陆弹窗对话框
      loginDialog: false,
      // 注册对话框
      logonDialog: false
    };
  },
  components: {
    login,
    logon
  },

  mounted() {
    this.$store.dispatch("loadConstance");
  }
};
</script>
<style scoped>
.v-app-bar .v-btn {
  margin-top: 1em !important;
}

.v-card {
  transition: opacity 0.4s ease-in-out;
}

.v-card:not(.on-hover) {
  opacity: 0.6;
}

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}

/deep/ .v-dialog {
  position: relative;
  z-index: 10000 !important;
}

.user {
  margin-top: 1.2em !important;
  min-width: 8em;
}
</style>
