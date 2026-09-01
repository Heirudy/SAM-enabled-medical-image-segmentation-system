<template>
  <div id="Header">
    <!-- 免费咨询 -->
    <div class="top-left-edition">
      <span style="color:#21b3b9;font-weight:bold;">
        <i class="el-icon-time" style="font-size:23px;"></i>工作时间：9:00-18:00
      </span>
    </div>
    <!-- CT图像处理字（可删除放图片） -->
    <div id="word">
      <h1>{{ msg }}</h1>
    </div>
    <!-- 导航栏 -->
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      id="menu"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="1">肺部CT</el-menu-item>
      <el-menu-item index="2">病理</el-menu-item>
      <el-menu-item index="3">眼底血管</el-menu-item>
      <el-menu-item index="4">
        <el-button type="primary" @click="logout">退出</el-button>
      </el-menu-item>
    </el-menu>
    <!-- 动态加载组件 -->
    <div v-if="activeIndex === '1'">
      <app-content />
    </div>
    <div v-if="activeIndex === '2'">
      <app-content2 />
    </div>
    <div v-if="activeIndex === '3'">
      <app-content3 />
    </div>
  </div>
</template>

<script>
import Content from "@/components/Content.vue";
import Content2 from "@/components/Content2.vue";
import Content3 from "@/components/Content3.vue";

export default {
  name: "Header",
  components: {
    "app-content": Content,
    "app-content2": Content2,
    "app-content3": Content3
  },
  data() {
    return {
      msg: "医学影像分割系统",
      activeIndex: "1"
    };
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
    },
    logout() {
      localStorage.removeItem("state");
      window.location.reload();
    }
  }
};
</script>

<style scoped>
#Header {
  padding: 20px 50px 0 50px; /* 减少内边距 */
  width: 90%;
  margin: 10px auto; /* 保持外边距 */
}

#word {
  margin-left: 0; /* 重置左边距 */
  margin-top: 20px; /* 调整顶部外边距 */
  margin-bottom: 30px; /* 调整底部外边距 */
  text-align: center; /* 居中对齐标题 */
  width: 100%; /* 确保标题容器宽度足够 */
}

h1 {
  color: #21b3b9;
  letter-spacing: 10px; /* 减少字间距 */
  font-size: 2em; /* 减少字体大小 */
  margin: 0; /* 重置默认外边距 */
}

.el-menu-demo {
  width: 100%; /* 确保导航栏宽度足够 */
  margin: 0 auto; /* 保持外边距 */
  padding: 0;
}

.top-left-edition {
  margin-bottom: 20px; /* 增加底部外边距 */
}

.top-left-edition span {
  font-size: 16px;
  color: #999999;
  line-height: 24px;
  margin-right: 40px;
}
</style>