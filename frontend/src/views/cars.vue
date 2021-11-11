<template>
  <v-app>
    <v-app-bar app hide-on-scroll>
      <v-toolbar dark color="teal">
        <v-col offset-md="2" offset-sm="0" md="1">
          <v-toolbar-title>Search</v-toolbar-title>
        </v-col>
        <v-col md="6" sm="8" align-self="auto">
          <v-text-field
            v-model="search"
            :loading="loading"
            label="What are you want to search?"
            flat
          ></v-text-field>
        </v-col>
        <v-col md="2">
          <span>约 {{ count }} 条信息</span>
        </v-col>
      </v-toolbar>
    </v-app-bar>
    <v-main>
      <v-col md="10" offset-lg="1" lg="10" id="news" ref="news">
        <v-card>
          <v-tabs v-model="index" background-color="primary" dark>
            <v-tab v-for="tab in tabs" :key="tab.title">{{ tab.title }}</v-tab>
          </v-tabs>
          <v-tabs-items v-model="index">
            <v-tab-item v-for="tab in tabs" :key="tab.title" class="card">
              <v-col offset-md="1" md="10">
                <v-card
                  v-for="item in source"
                  :key="item._id"
                  :href="item._source.detail_url"
                  class="sub_card"
                >
                  <v-card-title class="text-h5">
                    <span
                      v-if="item.highlight && item.highlight.title"
                      v-html="item.highlight.title[0]"
                    ></span>
                    <span v-else v-html="item._source.title "></span>
                  </v-card-title>
                  <v-card-text class="pb-0 clearfix">
                    <img id="autoimg" :src="item._source.img_url" />
                    <v-chip small>{{ item._source.tag }}</v-chip>
                    <p
                      class="summary"
                      v-if="item.highlight && item.highlight.summary"
                      v-html="item.highlight.summary[0]"
                    ></p>
                    <p class="summary" v-else v-html="item._source.summary"></p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-tab-item>
          </v-tabs-items>

          <!-- 分页 -->
          <div class="pageation">
            <v-pagination v-model="page" :length="Math.ceil(count/size)" :total-visible="7"></v-pagination>
          </div>
        </v-card>
      </v-col>
    </v-main>
  </v-app>
</template>
<script>
import { esNewsSearch } from "@/api";

export default {
  data() {
    return {
      // 标签页
      index: 0,
      tabs: [
        { title: "全部", content: "" },
        { title: "最新", content: "news" },
        { title: "推荐", content: "advice" },
        { title: "驾驶", content: "drive" },
        { title: "用车", content: "use" },
        { title: "文化", content: "culture" },
        { title: "旅行", content: "travels" },
        { title: "科技", content: "tech" },
        { title: "图柠", content: "tuning" },
        { title: "新能源", content: "ev" }
      ],

      // 定时器
      timer: null,

      // loading
      loading: false,

      // 搜索条件
      search: "",

      // 新闻列表
      source: [],

      // 分页
      page: 1,
      size: 10,
      count: 0
    };
  },
  methods: {
    queryState(content, tag) {
      // 加载中
      this.loading = true;
      esNewsSearch(content, tag, this.page, this.size).then(res => {
        // 加载完成
        this.loading = false;
        this.count = res.data.hits.total.value;

        let data = res.data.hits.hits;

        // 结果不为空就渲染到页面
        if (data.length > 0) {
          this.source = data;
        }
      });
    },

    debounce(content, tag, func, wait) {
      // 防抖
      if (this.timer !== null) {
        clearTimeout(this.timer);
      }
      this.timer = setTimeout(() => {
        func(content, tag);
      }, wait);
    }
  },

  watch: {
    search(val) {
      if (val) {
        this.page = 1;
        this.debounce(val, this.tabs[this.index].content, this.queryState, 500);
      }
    },
    index(val) {
      // 切换标签时，page重置
      this.page = 1;
      this.debounce(this.search, this.tabs[val].content, this.queryState, 200);
    },
    page() {
      this.queryState(this.search, this.tabs[this.index].content);
    }
  },

  mounted() {
    this.queryState(this.search, this.tabs[this.index].content);
  }
};
</script>
<style scoped>
.card {
  height: 60em;
  overflow: auto;
}
.sub_card {
  margin: 2em 0;
}
.v-text-field {
  margin-top: 1em !important;
}
.summary {
  padding: 1em 0;
}
#autoimg {
  float: left;
  margin-right: 1em;
  margin-bottom: 1em;
}
.clearfix:after {
  content: "";
  display: block;
  clear: both;
}
.pageation {
  text-align: center;
  background-color: lightgray;
}
</style>