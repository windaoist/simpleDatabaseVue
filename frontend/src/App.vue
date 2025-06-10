<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const navItems = [
  { name: '添加数据', path: '/add' },
  { name: '上传数据', path: '/upload' },
  { name: '查询数据', path: '/query' },
]
onMounted(() => {
  console.log(window.devicePixelRatio)
})
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo-container">
            <img alt="Vue logo" class="logo" src="@/assets/logo.svg" />
            <h1 class="app-title">数据库操作平台</h1>
          </div>

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
