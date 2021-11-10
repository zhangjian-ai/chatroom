<template>
  <div>
    <v-app-bar app dense src="@/assets/banner.png">
      <v-col offset-md="7" offset-sm="5" sm="3" md="2" align-self="center">
        <p class="user" v-show="$store.state.status">欢迎回来【{{ $store.state.nickname }}】</p>
      </v-col>
      <v-col sm="4" md="3" align-self="center">
        <v-btn
          :disabled="$store.state.status"
          color="white"
          text
          @click="loginDialog = !loginDialog"
        >登陆</v-btn>
        <v-btn
          :disabled="$store.state.status"
          text
          color="white"
          @click="logonDialog = !logonDialog"
        >注册</v-btn>
        <v-btn :disabled="!$store.state.status" text @click="$store.commit('setUserInfo')">注销</v-btn>
      </v-col>
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
        <v-card>
          <v-app-bar dense color="blue">
            <v-toolbar-title>
              <v-icon color="white">mdi-message-text</v-icon>聊天室
            </v-toolbar-title>
          </v-app-bar>
          <template v-for="(item, i) in items">
            <v-col :key="i" sm="4" md="3">
              <v-hover v-slot="{ hover }">
                <v-card :elevation="hover ? 10 : 2" id="item">
                  <v-img :src="item.img" height="12em">
                    <v-col>
                      <p id="room-title">{{ item.title }}</p>
                      <div id="room-desc">
                        <p>{{ item.text }}</p>
                        <p>{{ item.subtext }}</p>
                      </div>
                      <v-btn
                        class="in-btn"
                        icon
                        @click="$router.push({path: '/chat_room', query: {id: 123}})"
                      >
                        <v-icon :class="{ 'show-btns': hover }" :color="transparent">mdi-play</v-icon>
                      </v-btn>
                    </v-col>
                  </v-img>
                </v-card>
              </v-hover>
            </v-col>
          </template>
        </v-card>
        <!-- 工作流 -->
        <v-card>
          <v-app-bar dense color="grey">
            <v-toolbar-title>
              <v-icon color="orange">mdi-stack-overflow</v-icon>工作流
            </v-toolbar-title>
          </v-app-bar>
        </v-card>
        <!-- 汽车之家 -->
        <v-card>
          <v-app-bar dense color="green">
            <v-toolbar-title>
              <v-icon color="white">mdi-car-side</v-icon>汽车之家
            </v-toolbar-title>
          </v-app-bar>
          <v-col sm="4" md="3">
            <v-hover v-slot="{ hover }">
              <v-card :elevation="hover ? 10 : 2" id="item">
                <v-img src="@/assets/car.jpeg" height="12em">
                  <v-col>
                    <p id="room-title">机车新闻</p>
                    <div id="room-desc">
                      <p>资讯广场</p>
                      <p>领略全球最前沿的汽车科技...</p>
                    </div>
                    <v-btn class="in-btn" icon @click="$router.push({path: '/cars'})">
                      <v-icon :class="{ 'show-btns': hover }" :color="transparent">mdi-play</v-icon>
                    </v-btn>
                  </v-col>
                </v-img>
              </v-card>
            </v-hover>
          </v-col>
        </v-card>
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
.v-banner {
  margin-bottom: 1em;
}
.v-card:not([id="item"]) {
  margin: 2em 0;
}
.v-card[id="item"] {
  transition: opacity 0.4s ease-in-out;
}
.v-card[id="item"]:not(:hover) {
  opacity: 0.6;
}
#room-title {
  font: bolder;
  font-size: 1.5em;
  color: red;
}
#room-desc p {
  margin: 0;
  color: whitesmoke;
}
.in-btn {
  position: relative;
  left: 40%;
  top: 1em;
}
.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
.user {
  margin-top: 1.2em !important;
  min-width: 8em;
}
</style>
