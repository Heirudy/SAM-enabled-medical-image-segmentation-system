<template>
  <div id="app" class="app-container" :class="{ 'login-background': state == 0 }">
    <div v-if="state == 0" class="login-container">
      <el-row>
        <el-col :span="24" class="login-col">
          <h1 class="login-title">{{ name }}</h1>
          <div class="grid-content bg-purple-dark">
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="账号">
                <el-input v-model="form.username" class="custom-input-width"></el-input>
              </el-form-item>
              <el-form-item label="密码">
                <el-input v-model="form.password" type="password" class="custom-input-width"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit" class="custom-button-width">登录</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-col>
      </el-row>
    </div>



    <div v-if="state == 1">
      <app-header></app-header>
      <app-footer></app-footer>
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  name: "医学影像分割系统",
  components: {
    "app-header": Header,
    "app-footer": Footer
  },
  data() {
    return {
      name: "医学影像分割系统",
      form: {
        username: '',
        password: ''
      },
      state: 0 // 0 表示登录页面，1 表示主页面
    };
  },
  methods: {
    onSubmit() {
      console.log(this.form);
      if (this.form.username === "admin" && this.form.password === "admin") {
        localStorage.setItem('state', 1);
        this.$message({
          message: '登录成功',
          type: 'success'
        });
        window.location.reload();
      } else {
        this.$message.error('账号密码错误');
      }
    },
    getStats() {
      this.state = localStorage.getItem('state') ? parseInt(localStorage.getItem('state')) : 0;
    }
  },
  created() {
    document.title = '医学影像分割系统';
  },
  mounted() {
    this.getStats();
  }
};
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 仅在登录页面应用背景样式 */
.login-background {
  background-image: url("@/OIP-C.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.login-container {
  width: 30%;
  background-color: rgba(255, 255, 255, 0.6);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  white-space: nowrap;
}

.el-form-item {
  margin-bottom: 15px;
}

.el-button {
  width: 100%;
}
</style>
