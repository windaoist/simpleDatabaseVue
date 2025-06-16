<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import request from '@/utils/request'
import * as echarts from 'echarts'
import { ElMessage, ElMessageBox } from 'element-plus'
import AddForm from '@/components/AddForm.vue'
const profileInfo = ref({
  role: '' as 'student' | 'teacher' | 'Admin',
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
const backupList = ref({
  auto: [] as string[],
  manual: [] as string[],
})
const statistics = ref([])
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
  if (profileInfo.value.role === 'student') {
    info.push('学生')
    info.push(profileInfo.value.info['student_id'])
    info.push(profileInfo.value.info['name'])
    currentTable.value = 'student'
  } else if (profileInfo.value.role === 'teacher') {
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
async function fetchBackupList() {
  try {
    const response = await request.get('backup/list')
    backupList.value = response.data.data
  } catch (error) {
    ElMessage.error('获取备份文件失败：' + error.response?.data?.message)
  }
}
async function handleManualBackup() {
  try {
    const response = await request.get('backup/backup', {
      responseType: 'blob',
    })
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)

    const a = document.createElement('a')
    a.href = url

    // 尝试从响应头中提取文件名
    const contentDisposition = response.headers['content-disposition']
    let fileName = 'downloaded_file.sql'
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?([^"]+)"?/)
      if (match) {
        fileName = decodeURIComponent(match[1])
      }
    }

    a.download = fileName
    a.click()

    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
    fetchBackupList()
  } catch (error) {
    ElMessage.error('获取备份文件失败：' + error.response?.data?.message)
  }
}

async function restoreBackup(filename: string, source: string) {
  try {
    const response = await request.get('backup/restore_file', {
      params: {
        source: source,
        filename: filename,
      },
    })
    if (response.data.success) {
      ElMessage.success('备份恢复成功')
    } else {
      ElMessage.success('备份恢复失败，请稍后再试')
    }
  } catch (error) {
    ElMessage.error('获取备份文件失败：' + error.response?.data?.message)
  }
}
async function downloadBackup(filename: string, source: string) {
  try {
    const response = await request.get('backup/download_file', {
      responseType: 'blob',
      params: {
        source: source,
        filename: filename,
      },
    })
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)

    const a = document.createElement('a')
    a.href = url

    // 尝试从响应头中提取文件名
    const contentDisposition = response.headers['content-disposition']
    let fileName = 'downloaded_file.sql'
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?([^"]+)"?/)
      if (match) {
        fileName = decodeURIComponent(match[1])
      }
    }

    a.download = fileName
    a.click()

    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('获取备份文件失败：' + error.response?.data?.message)
  }
}
async function deleteBackup(filename: string, source: string) {
  try {
    await ElMessageBox.confirm('确定要删除这条数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    const response = await request.delete('backup/delete_file', {
      params: {
        source: source,
        filename: filename,
      },
    })
    if (response.data.success) {
      ElMessage.success('备份删除成功')
      fetchBackupList()
    } else {
      ElMessage.success('备份删除失败，请稍后再试')
    }
  } catch (error) {
    // 用户取消或其他异常
    if (error === 'cancel') {
      ElMessage.info('已取消删除')
    } else {
      ElMessage.error('删除失败：' + (error.response?.data?.message || error.message))
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
        <h3 v-if="profileInfo.role === 'student' || profileInfo.role === 'teacher'">
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
            v-if="profileInfo.role === 'student' || profileInfo.role === 'teacher'"
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
        v-if="profileInfo.role === 'student' || profileInfo.role === 'teacher'"
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

          <el-card>
            <div style="display: flex; gap: 20px">
              <el-button type="primary" style="width: 200px" @click="handleManualBackup"
                >手动备份</el-button
              >
              <el-upload
                class="upload"
                action=""
                style="width: 200px"
                :limit="1"
                :http-request="handleUpload"
                :before-upload="beforeUpload"
              >
                <el-button type="success" style="width: 200px" icon="Upload">上传备份</el-button>
              </el-upload>
            </div>
            <template #header>手动备份</template>
            <el-table :data="backupList.manual" border style="width: 100%">
              <el-table-column label="文件名" prop="filename">
                <template #default="scope">
                  {{ scope.row }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250">
                <template #default="scope">
                  <el-button size="small" @click="restoreBackup(scope.row, 'manual')"
                    >恢复</el-button
                  >
                  <el-button size="small" @click="downloadBackup(scope.row, 'manual')"
                    >下载</el-button
                  >
                  <el-button size="small" type="danger" @click="deleteBackup(scope.row, 'manual')"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </el-card>
          <el-card class="mb-4">
            <template #header>自动备份</template>
            <el-table :data="backupList.auto" border style="width: 100%">
              <el-table-column label="文件名" prop="filename">
                <template #default="scope">
                  {{ scope.row }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250">
                <template #default="scope">
                  <el-button size="small" @click="restoreBackup(scope.row, 'auto')">恢复</el-button>
                  <el-button size="small" @click="downloadBackup(scope.row, 'auto')"
                    >下载</el-button
                  >
                  <el-button size="small" type="danger" @click="deleteBackup(scope.row, 'auto')"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </el-card>

          <!-- </el-tab-pane>
            </el-tabs>
          </div> -->
          <el-button @click="fetchBackupList()">获取备份数据</el-button>
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
