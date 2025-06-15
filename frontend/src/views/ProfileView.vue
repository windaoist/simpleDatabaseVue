<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import request from '@/utils/request'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import AddForm from '@/components/AddForm.vue'
const profileInfo = ref({
  role: '' as 'Student' | 'Teacher' | 'Admin',
  info: {} as Record<string, string>,
  research_fields: [] as string[],
})
const research_fields = ref()
const BasicInfo = ref()
const currentTable = ref()
const activeTab = ref('')
const passwdInfo = ref({
  username: '' as string,
  old_password: '' as string,
  new_password: '' as string,
  confirm_password: '' as string,
})

const statistics = ref([]) // 原为 undefined，改为 []
async function getProfile() {
  try {
    const response = await request.get('auth/profile')
    if (response.data.success) {
      profileInfo.value = response.data.data
      BasicInfo.value = getBasicInfo()
    } else {
      ElMessage.error('获取账户信息错误：' + response.data?.message)
    }
  } catch (error) {
    ElMessage.error('获取账户信息错误：' + error.response?.data?.message)
  }
}
function getBasicInfo() {
  const info = []
  if (profileInfo.value.role === 'Student') {
    info.push('学生')
    info.push(profileInfo.value.info['student_id'])
    info.push(profileInfo.value.info['name'])
    currentTable.value = 'student'
  } else if (profileInfo.value.role === 'Teacher') {
    info.push('教职工')
    info.push(profileInfo.value.info['teacher_id'])
    info.push(profileInfo.value.info['name'])
    currentTable.value = 'teacher'
  } else {
    info.push('管理员')
  }
  return info
}
async function handleSubmit(formData: { filters: any; memberList: any }) {
  try {
    const payload = {
      table: currentTable.value,
      data: {
        ...formData.filters,
        research_field: formData.filters.research_field
          ? formData.filters.research_field
              .map((name) => {
                const match = research_fields.value.find((field) => field.research_field === name)
                return match ? match.id : null
              })
              .filter((id) => id !== null)
          : null,
      },
    }
    const response = await request.post('add-edit/edit', payload)
    ElMessage.success('编辑成功：' + response.data.message)
  } catch (error) {
    ElMessage.error('编辑失败：' + error.response?.data?.message)
  }
}
async function handleDownload() {
  try {
    const response = await request.get('backup/backup', { responseType: 'blob' })

    ElMessage.success('备份成功，正在下载...')

    // 获取响应头中的 content-disposition
    const disposition = response.headers['content-disposition']
    let filename = 'backup.sql' // 默认文件名

    if (disposition && disposition.includes('filename=')) {
      const match = disposition.match(/filename="?(.+?)"?$/)
      if (match && match[1]) {
        filename = decodeURIComponent(match[1])
      }
    }

    const blob = response.data
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()

    // 释放 URL 对象
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('备份失败:' + error.response?.data?.message)
  }
}
async function handleUpload(option) {
  const { file, onProgress } = option

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await request.post('backup/restore', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress({ percent })
        }
      },
    })
    if (response.data) {
      ElMessage.success(response.data.message || '上传成功')
      return
    }
    ElMessage.info('上传成功！')
  } catch (error) {
    ElMessage.error('上传失败：' + error.response?.data?.message || '请稍后再试')
  }
}
const beforeUpload = (file) => {
  const isLt2M = file.size / 1024 / 1024 / 1024 < 1
  if (!isLt2M) {
    ElMessage.error('上传文件大小不能超过 10MB!')
  }
  return isLt2M
}
async function submitPassword() {
  try {
    if (passwdInfo.value.new_password !== passwdInfo.value.confirm_password) {
      ElMessage.error('密码不匹配')
      return
    }
    const payload = {
      username: localStorage.getItem('current_user'),
      old_password: passwdInfo.value.old_password,
      new_password: passwdInfo.value.new_password,
    }
    const response = await request.post('auth/change-password', payload)
    ElMessage.success(response.data.message)
  } catch (error) {
    ElMessage.error('修改密码失败：' + error.response?.data?.message)
  }
}
function resetPasswordForm() {
  passwdInfo.value = {
    username: '' as string,
    old_password: '' as string,
    new_password: '' as string,
    confirm_password: '' as string,
  }
}
async function getStatistics() {
  try {
    const response = await request.get('query/statistics')
    statistics.value = response.data.data.results
    await nextTick()
    renderChart(statistics.value)
  } catch (error) {
    ElMessage.error('获取统计信息失败：' + error.response?.data?.message)
  }
}
let chartInstance: echarts.ECharts | null = null

function renderChart(data: any[]) {
  const chartDom = document.getElementById('barChart')
  if (!chartDom || chartDom.clientWidth === 0 || chartDom.clientHeight === 0) return

  if (chartInstance) {
    chartInstance.dispose()
  }
  chartInstance = echarts.init(chartDom)

  const categories = data.map((item) => item.专业)
  const applyPass = data.map((item) => Number(item.申报通过数))
  const approvePass = data.map((item) => Number(item.审批通过数))
  const acceptPass = data.map((item) => Number(item.验收通过数))

  const option = {
    title: {
      text: '各专业通过数统计',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    legend: {
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'value',
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        interval: 0,
      },
    },
    series: [
      {
        name: '申报通过数',
        type: 'bar',
        data: applyPass,
        color: '#5470C6',
      },
      {
        name: '审批通过数',
        type: 'bar',
        data: approvePass,
        color: '#91CC75',
      },
      {
        name: '验收通过数',
        type: 'bar',
        data: acceptPass,
        color: '#FAC858',
      },
    ],
  }

  chartInstance.setOption(option)
  // 只绑定一次 resize
  window.onresize = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }
}

// 监听 activeTab 和 statistics，切换到 statistics 且有数据时自动渲染图表
watch([activeTab, statistics], async ([tab, stats]) => {
  if (tab === 'statistics' && stats && stats.length) {
    await nextTick()
    renderChart(stats)
  }
})

async function fetchFields() {
  try {
    const response = await request.get('query/research_fields')
    research_fields.value = response.data.data.research_fields
    console.log('行业列表:', research_fields.value)
  } catch (error) {
    console.error('获取行业列表失败:', error)
  }
}
onMounted(() => {
  // 初始化行业列表
  fetchFields()
  getProfile()
})
</script>

<template>
  <div>
    <div v-if="profileInfo.role">
      <div class="basic">
        <h3 v-if="profileInfo.role === 'Student' || profileInfo.role === 'Teacher'">
          欢迎，{{ BasicInfo[0] }}{{ BasicInfo[1] }}{{ BasicInfo[2] }}
        </h3>
        <h3 v-else>欢迎，{{ BasicInfo[0] }}</h3>
      </div>
    </div>

    <div class="profile" v-if="profileInfo.role">
      <!-- 按钮组切换 -->
      <div style="margin-bottom: 20px">
        <el-button-group>
          <el-button
            :type="activeTab === 'edit' ? 'primary' : 'default'"
            @click="activeTab = 'edit'"
            size="large"
            round
            v-if="profileInfo.role === 'Student' || profileInfo.role === 'Teacher'"
          >
            编辑信息
          </el-button>
          <el-button
            size="large"
            round
            :type="activeTab === 'statistics' ? 'primary' : 'default'"
            @click="activeTab = 'statistics'"
            v-if="profileInfo.role === 'Admin'"
          >
            统计信息
          </el-button>
          <el-button
            size="large"
            round
            :type="activeTab === 'backup' ? 'primary' : 'default'"
            @click="activeTab = 'backup'"
            v-if="profileInfo.role === 'Admin'"
          >
            备份恢复
          </el-button>
          <el-button
            size="large"
            round
            :type="activeTab === 'password' ? 'primary' : 'default'"
            @click="activeTab = 'password'"
          >
            修改密码
          </el-button>
        </el-button-group>
      </div>

      <!-- 内容区域 -->
      <div
        v-show="activeTab === 'edit'"
        v-if="profileInfo.role === 'Student' || profileInfo.role === 'Teacher'"
      >
        <AddForm
          :current-table="currentTable"
          :research-fields="research_fields"
          :initial-data="{
            filters: {
              ...profileInfo.info,
              research_field: profileInfo.research_fields,
            },
          }"
          @update="handleSubmit"
        />
      </div>
      <div v-if="activeTab === 'statistics'">
        <el-tabs type="border-card">
          <el-tab-pane label="table">
            <el-table :data="statistics" style="width: 100%">
              <el-table-column prop="专业" label="专业" />
              <el-table-column prop="申报通过数" label="申报通过数" />
              <el-table-column prop="审批通过数" label="审批通过数" />
              <el-table-column prop="验收通过数" label="验收通过数" />
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="chart">
            <el-card v-if="statistics && statistics.length" style="margin-top: 20px">
              <div id="barChart" style="width: 100%; height: 500px"></div>
            </el-card>
          </el-tab-pane>
        </el-tabs>
        <el-button @click="getStatistics">获取统计数据 </el-button>
      </div>
      <div v-if="activeTab === 'backup'">
        <el-card class="operation-card">
          <template #header>
            <span>数据管理</span>
          </template>

          <div class="data-button">
            <!-- 备份按钮 -->
            <el-button
              size="large"
              style="width: 400px"
              type="primary"
              icon="Download"
              @click="handleDownload"
            >
              数据备份
            </el-button>

            <!-- 恢复按钮 -->
            <el-upload
              class="upload"
              drag
              style="width: 100%"
              action=""
              :http-request="handleUpload"
              :before-upload="beforeUpload"
            >
              <el-button type="success" icon="Upload">数据恢复</el-button>
            </el-upload>
          </div>
        </el-card>
      </div>
      <div v-if="activeTab === 'password'">
        <el-form label-width="100px" :model="passwdInfo" ref="passwdFormRef" status-icon>
          <el-form-item label="旧密码" prop="old_password">
            <el-input v-model="passwdInfo.old_password" type="password" show-password />
          </el-form-item>

          <el-form-item label="新密码" prop="new_password">
            <el-input v-model="passwdInfo.new_password" type="password" show-password />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirm_password">
            <el-input v-model="passwdInfo.confirm_password" type="password" show-password />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitPassword">提交</el-button>
            <el-button @click="resetPasswordForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.basic {
  padding: 20px;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  height: fit-content;
  width: fit-content;
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  color: black;
}
.el-button-group {
  display: flex;
  justify-content: center;
  margin-top: 2%;
  gap: 10px;
}
.data-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
</style>
