<template>
  <div class="main">
    <div class="hall">
      <div class="subhall" id="hall" @scroll="scroll(2)"></div>
      <v-chip
        class="tips"
        v-show="msg_tip_show"
        @click="scroll(1)"
        color="blue"
        text-color="white"
      >您有 {{ msg_count }} 条未读消息</v-chip>
    </div>
    <v-row>
      <v-col cols="4">
        <v-text-field v-model="input" placeholder="少说两句～" @keyup.enter="publish()" outlined dense></v-text-field>
      </v-col>
      <v-col cols="8">
        <v-btn @click="publish()" elevation="2" color="primary">发表</v-btn>
        <v-btn @click="connection()" elevation="2" color="error">{{ online ? "离开" : "重连" }}</v-btn>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      // 输入框
      input: "",

      // 未读消息数量
      msg_count: 0,
      msg_tip_show: false,

      // 在线状态
      online: false
    };
  },
  methods: {
    // 建立websocket连接
    getConnection() {
      let that = this;
      let socket = new WebSocket(
        `ws://${axios.defaults.baseURL.split("//")[1]}/chat/${
          this.$route.query.id
        }/`
      );

      // socket钩子函数，在我手成功时触发
      socket.onopen = function(event) {
        if (event.isTrusted) {
          that.online = true;

          let div = document.createElement("div");
          let p = document.createElement("p");

          p.setAttribute("style", "font-size:0.8em; color: grey; margin:1em;");
          p.innerHTML = "建立连接...成功";

          div.appendChild(p);
          document.getElementById("hall").appendChild(div);
        }
      };

      // socket钩子函数，在接收到服务端消息后出发
      socket.onmessage = event => {
        // 解析后端json字符串为对象
        let data = JSON.parse(event.data);
        let username = data.username;
        let time = data.time;
        let text = data.text;

        let header = document.createElement("p");
        header.setAttribute("style", "margin: 0;");

        let un = document.createElement("span");
        un.setAttribute("style", "color: blue; font-size:0.8em;");
        un.innerText = username;

        let t = document.createElement("span");
        t.setAttribute(
          "style",
          "font-size:0.6em; color: grey; margin-left: 1em;"
        );
        t.innerText = time;

        header.appendChild(un);
        header.appendChild(t);

        let body = document.createElement("p");
        body.setAttribute("style", "margin: 0;");
        body.innerText = text;

        let div = document.createElement("div");
        div.appendChild(header);
        div.appendChild(body);

        div.setAttribute(
          "style",
          "border-radius: 0.5em; background: whitesmoke; padding: 0.3em 0.5em 0.3em; margin: 0.5em;"
        );

        // 判断是否在底部
        var hall = document.getElementById("hall");

        if (hall.clientHeight + hall.scrollTop == hall.scrollHeight) {
          this.msg_tip_show = false;
        } else {
          this.msg_tip_show = true;
          this.msg_count += 1;
        }

        // 添加消息到窗口
        document.getElementById("hall").appendChild(div);

        // 滚动窗口
        this.scroll(0);
      };

      // socket钩子函数，断开连接时触发
      socket.onclose = event => {
        if (event.type == "close") {
          let div = document.createElement("div");
          let p = document.createElement("p");

          p.setAttribute("style", "font-size:0.8em; color: grey; margin:1em;");
          p.innerHTML = "连接已关闭...";

          div.appendChild(p);
          document.getElementById("hall").appendChild(div);

          // 客户端同步关闭
          this.disConnection();
        }
      };

      return socket;
    },
    // 发送消息到服务端
    publish() {
      if (this.input) {
        // 生成身份信息
        if (!this.$store.state.nickname) {
          this.$store.state.nickname =
            "游客 " + Math.round(Math.random() * 1000000);
        }

        let message = {
          username: this.$store.state.nickname,
          text: this.input
        };
        this.socket.send(JSON.stringify(message));
        this.input = "";
      } else {
        this.$message({
          message: "请输入要发表的内容...",
          type: "warning"
        });
      }
    },
    // 断开socket连接
    disConnection() {
      this.socket.close();
      this.online = false;
    },
    // 滚动滚动条展示最新消息。0:自动， 1:手动点击， 2:手动滚动
    scroll(type = 0) {
      var hall = document.getElementById("hall");
      if (type == 0) {
        // 根据是否在底部决定要不要自动滚动
        if (!this.msg_tip_show) {
          hall.scrollTop = hall.scrollHeight;
          this.msg_count = 0;
        }
      } else if (type == 1) {
        hall.scrollTop = hall.scrollHeight;
        this.msg_tip_show = false;
        this.msg_count = 0;
      } else {
        this.msg_tip_show = false;
        this.msg_count = 0;
      }
    },
    // 连接
    connection() {
      if (this.online) {
        this.disConnection();
      } else {
        this.socket = this.getConnection();
      }
    }
  },
  mounted() {
    this.socket = this.getConnection();
  },
  beforeDestroy() {
    this.disConnection();
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
  margin: 2em 0;
}
.subhall {
  height: 30em;
  margin: 0;
  border: 1px solid black;
  overflow-x: auto;
  overflow-y: scroll;
}
.v-btn {
  margin: 0 1em;
}
.tips {
  position: relative;
  top: -10%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
