<script setup lang="ts">
import { inject, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { DocumentAdd, Upload, Search, User } from '@element-plus/icons-vue'
const navItems = [
  { name: '添加数据', path: '/add', icon: DocumentAdd },
  { name: '上传数据', path: '/upload', icon: Upload },
  { name: '查询数据', path: '/query', icon: Search },
  { name: '我的账户', path: '/profile', icon: User },
]
const isLoggedIn = inject('isLoggedIn')

const visibleNavItems = computed(() => {
  return isLoggedIn ? navItems : navItems.slice(0, navItems.length - 1)
})
</script>

<template>
  <div class="card-items">
    <ElRow :gutter="30" justify="center">
      <ElCol
        :xs="24"
        :sm="12"
        :md="12"
        :lg="12"
        v-for="item in visibleNavItems"
        :key="item.path"
        class="grid-item"
      >
        <ElCard class="operation-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon">
              <div class="icon-wrapper">
                <component :is="item.icon" class="card-el-icon" />
              </div>
            </div>
            <h2>{{ item.name }}</h2>
            <p class="card-desc">点击进入{{ item.name }}页面</p>
            <RouterLink :to="item.path">
              <ElButton type="primary" class="card-button" round>进入操作</ElButton>
            </RouterLink>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>

<style scoped>
/* 新增网格容器样式 */
.grid-item {
  padding-bottom: 30px; /* 垂直间距 */
}
.card-el-icon {
  width: 40px;
  height: 40px;
  color: white;
}
.operation-card {
  border-radius: 12px;
  border: none;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  height: 100%;
  width: 100%;
}

.operation-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}

.card-content {
  padding: 25px 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.card-icon {
  margin-bottom: 20px;
}

.icon-wrapper {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #409eff, #64b5ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.icon-text {
  font-size: 28px;
  font-weight: bold;
  color: white;
}

.operation-card h2 {
  font-size: 1.5rem;
  color: #303133;
  margin-bottom: 12px;
}

.card-desc {
  color: #606266;
  font-size: 1rem;
  margin-bottom: 25px;
  flex-grow: 1;
}

.card-button {
  padding: 10px 28px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
  transition: all 0.3s;
}

.card-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(64, 158, 255, 0.4);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .grid-item {
    padding-bottom: 20px; /* 小屏幕垂直间距 */
  }
}
</style>
