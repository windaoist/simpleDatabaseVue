<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
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
const activeTab = ref('edit')
const passwdInfo = ref({
  username: '' as string,
  old_password: '' as string,
  new_password: '' as string,
  confirm_password: '' as string,
})
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
</style>
