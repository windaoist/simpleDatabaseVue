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
const isLoggedIn = ref(!!localStorage.getItem('jwt_token'))
async function handleLogin() {
  if (account.value.username === '' || account.value.password === '' || account.value.role === '') {
    ElMessage.error('用户名，密码或类别不能为空')
    return
  }
  try {
    const response = await request.post('/auth/login', account.value)
    localStorage.setItem('jwt_token', response.data.data.token)
    // LoggedIn.value = true
  } catch (error) {
    console.error('登录失败', error.message)
    ElMessage.error('登录失败：' + error.response?.data?.message || '请稍后再试')
    return
  }
  loginDialogVisible.value = false
  isLoggedIn.value = true
  console.log('登录成功', account.value)
  ElMessage.success('登录成功')
}
async function handleLogout() {
  try {
    // await request.post('/auth/logout')
    localStorage.removeItem('jwt_token')
    isLoggedIn.value = false
    // LoggedIn.value = false
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
    <el-container style="height: 100vh">
      <el-aside width="200px">
        <div class="sidebar-content">
          <div class="logo-container">
            <img alt="Vue logo" class="logo" src="@/assets/logo.svg" />
            <h1 class="app-title">数据库操作平台</h1>
          </div>
          <div class="auth-button">
            <el-button
              type="primary"
              v-if="!isLoggedIn"
              class="icon-wrapper"
              @click="loginDialogVisible = true"
            >
              登录
            </el-button>
            <el-button type="danger" v-else class="icon-wrapper" @click="handleLogout">
              注销
            </el-button>
          </div>
          <ElMenu
            mode="vertical"
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
      </el-aside>

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
  height: fit-content;
  flex-direction: column;
  background-color: #f5f7fa;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
}

.el-aside {
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  width: 220px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  height: 100%;
  padding: 20px 15px;
  box-sizing: border-box;
  overflow-y: auto;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
}

.logo {
  width: 60px;
  height: 60px;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: rotate(10deg) scale(1.1);
}

.app-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #34495e;
  text-align: center;
  white-space: nowrap;
}

.auth-button {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.icon-wrapper {
  width: 80%;
  font-size: 14px;
}

.app-menu {
  flex-grow: 1;
  width: 100%;
  border-right: none;
}

.app-menu .el-menu-item {
  font-size: 1rem;
  font-weight: 500;
  margin: 5px 8px;
  border-radius: 6px;
  transition: background-color 0.25s ease;
  padding-left: 20px !important;
}
.el-menu-item a {
  color: inherit;
  text-decoration: none;
}
.app-menu .el-menu-item:hover {
  background-color: #f0f8ff !important;
}

.app-menu .el-menu-item.is-active {
  background-color: #ecf5ff !important;
  border-left: 4px solid #409eff;
  font-weight: bold;
  color: #409eff !important;
}

.el-main {
  overflow-y: auto;
  flex: 1;
  max-width: 2000px;
  margin-top: 30px;
  margin-left: 220px;
  margin-bottom: 30px;
  padding: 0 20px;
}

/* .router-view {
  max-width: 2000px;
  width: 100%;
  margin: 0 auto 30px;
  padding: 0 20px;
} */

@media (max-width: 768px) {
  .common-layout {
    height: 100%;
  }

  .el-aside {
    width: 100%;
    height: auto;
    position: relative;
  }

  .el-main {
    margin-left: 0;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .app-menu {
    width: 100%;
  }

  .icon-wrapper {
    width: 60px;
    height: 60px;
  }
}
</style>
