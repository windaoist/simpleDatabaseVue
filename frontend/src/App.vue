<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const navItems = [
  { name: '添加数据', path: '/add' },
  { name: '上传数据', path: '/upload' },
  { name: '查询数据', path: '/query' },
]
const roles = [
  { name: '管理员', value: 'Admin' },
  { name: '老师', value: 'Teacher' },
  { name: '学生', value: 'Student' },
]
const loginDialogVisible = ref(false)
const account = ref({
  username: '',
  password: '',
  role: '',
})
const LoggedIn = ref(false)
async function handleLogin() {
  if (account.value.username === '' || account.value.password === '' || account.value.role === '') {
    ElMessage.error('用户名，密码或类别不能为空')
    return
  }
  // 模拟登录成功
  try {
    const response = await request.post('/auth/login', account.value)
    localStorage.setItem('jwt_token', response.data.token)
    LoggedIn.value = true
  } catch (error) {
    console.error('登录失败', error.message)
    ElMessage.error('登录失败：' + error.response?.data?.message || '请稍后再试')
    return
  }
  loginDialogVisible.value = false
  console.log('登录成功', account.value)
  ElMessage.success('登录成功')
}
async function handleLogout() {
  try {
    // await request.post('/auth/logout')
    localStorage.removeItem('jwt_token')
    LoggedIn.value = false
    ElMessage.success('注销成功')
  } catch (error) {
    console.error('注销失败', error.message)
    ElMessage.error('注销失败：' + error.response?.data?.message || '请稍后再试')
  }
}
onMounted(() => {
  console.log(window.devicePixelRatio)
})
</script>

<template>
  <div class="common-layout">
    <!-- 登录对话框 -->
    <el-dialog
      v-model="loginDialogVisible"
      title="用户登录"
      width="450px"
      class="login-dialog"
      :close-on-click-modal="false"
      :show-close="false"
    >
      <template #header>
        <div class="dialog-header">
          <h2 style="color: black">欢迎登录</h2>
        </div>
      </template>
      <div class="login-form">
        <el-input v-model="account.username" placeholder="请输入用户名" class="login-input">
          <template #prepend> 用户名 </template></el-input
        >
        <el-input
          v-model="account.password"
          type="password"
          show-password
          placeholder="请输入密码"
          class="login-input"
        >
          <template #prepend> 密码 </template></el-input
        >
        <el-select v-model="account.role" placeholder="请选择用户类别" class="login-input">
          <el-option
            v-for="role in roles"
            :key="role.value"
            :label="role.name"
            :value="role.value"
          ></el-option>
        </el-select>
      </div>
      <div class="login-actions">
        <el-button type="info" @click="loginDialogVisible = false" class="login-btn">
          取消
        </el-button>
        <el-button class="login-btn" type="primary" @click="handleLogin">登录</el-button>
      </div>
    </el-dialog>
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo-container">
            <img alt="Vue logo" class="logo" src="@/assets/logo.svg" />
            <h1 class="app-title">数据库操作平台</h1>
          </div>
          <el-button
            type="primary"
            v-if="!LoggedIn"
            style="margin-left: 5%"
            class="icon-wrapper"
            @click="loginDialogVisible = true"
          >
            登录
          </el-button>
          <el-button
            type="danger"
            v-else
            style="margin-left: 5%"
            class="icon-wrapper"
            @click="handleLogout"
          >
            注销
          </el-button>
          <ElMenu
            mode="horizontal"
            class="app-menu"
            :default-active="$route.path"
            background-color="#ffffff"
            text-color="#2c3e50"
            active-text-color="#409EFF"
          >
            <ElMenuItem index="/">
              <RouterLink to="/">首页</RouterLink>
            </ElMenuItem>
            <ElMenuItem v-for="item in navItems" :key="item.path" :index="item.path">
              <RouterLink :to="item.path">{{ item.name }}</RouterLink>
            </ElMenuItem>
          </ElMenu>
        </div>
      </el-header>

      <el-main>
        <RouterView class="router-view" />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
body {
  background-color: #f5f7fa;
  color: #2c3e50;
  font-family: 'Arial', sans-serif;
}
a {
  text-decoration: none;
}
.login-dialog {
  display: flex;
  justify-content: center;
}
.login-form {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}
.login-input {
  width: 80%;
}
.login-actions {
  display: flex;
  justify-content: space-evenly;
  margin-top: 20px;
}
.login-btn {
  width: 20%;
}
.common-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
}

.el-header {
  background-color: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  height: fit-content;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 15px;
  /* flex-shrink: 0; 新增 */
}

.app-menu {
  border-bottom: none;
  flex: 1; /* 允许扩展 */
  min-width: 0; /* 防止溢出 */
  display: flex;
  justify-content: flex-end; /* 右对齐 */
}

.app-menu > .el-menu {
  width: 100%;
  justify-content: flex-end;
}
.logo {
  width: 50px;
  height: 50px;
  transition: transform 0.3s;
}

.logo:hover {
  transform: rotate(15deg);
}

.app-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.app-menu .el-menu-item {
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0 5px;
  border-radius: 4px;
  transition: all 0.3s;
}

.app-menu .el-menu-item:hover {
  background-color: #ecf5ff !important;
}

.app-menu .el-menu-item.is-active {
  background-color: #ecf5ff !important;
  border-bottom: 2px solid #409eff;
}

.el-main {
  overflow-y: auto;
  flex: 1;
  max-width: 2000px;
  margin: 30px auto;
  padding: 0 20px;
}

.router-view {
  max-width: 2000px;
  width: 100%;
  margin: 0 auto 30px;
  padding: 0 20px;
}

@media (max-width: 768px) {
  .common-layout {
    height: 100%;
  }
  .header-content {
    flex-direction: column;
    gap: 15px;
    position: sticky;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .app-menu {
    width: 100%;
    justify-content: center;
  }

  .icon-wrapper {
    width: 60px;
    height: 60px;
  }
}
</style>
