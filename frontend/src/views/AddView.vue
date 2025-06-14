<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import AddForm from '@/components/AddForm.vue'

const currentTable = ref('student' as 'student' | 'teacher' | 'project_submit' | 'project' | '')
const research_fields = ref([])
async function handleSubmit(formData: { filters: any; memberList: any }) {
  try {
    const payload = {
      table: currentTable.value == 'project_submit' ? 'project' : currentTable.value,
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
    if (Array.isArray(payload.data.research_field)) {
      payload.data.research_field = payload.data.research_field.join('、')
    }
    if (currentTable.value == 'project_submit') {
      payload.data['member'] = formData.memberList.member
        .flatMap((member) => Object.keys(member))
        .join('、')
      payload.data['teacher'] = formData.memberList.teacher
        .flatMap((member) => Object.keys(member))
        .join('、')
    }
    const response = await request.post('add-edit/add', payload)
    ElMessage.success('添加成功：' + response.data.message)
  } catch (error) {
    ElMessage.error('添加失败：' + error.response?.data?.message)
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
})
</script>
<template>
  <div>
    <div class="query-view">
      <h3>选择要添加项的表</h3>
      <el-select v-model="currentTable" placeholder="请选择添加表表名" style="width: 220px">
        <el-option label="学生表" value="student" />
        <el-option label="教职工表" value="teacher" />
        <el-option label="科研项目表" value="project_submit" />
      </el-select>
    </div>
    <AddForm
      :current-table="currentTable"
      :research-fields="research_fields"
      @submit="handleSubmit"
    />
  </div>
</template>
<style scoped>
.query-view {
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
/* 输入行样式 */
.input-row {
  display: flex;
  margin-bottom: 10px; /* 与下方标签保持间距 */
}

.input-item {
  flex: 1; /* 输入框占据剩余空间 */
  margin-right: 10px; /* 输入框和按钮间距 */
}
/* .add-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
} */
/* 标签容器样式 */
.tags-container {
  display: flex;
  flex-wrap: wrap; /* 允许标签换行 */
  gap: 8px; /* 标签间距 */
}

/* 单个标签样式 */
.tag-item {
  margin-bottom: 5px; /* 标签行间距 */
}
.form-area {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 双列布局 */
  gap: 20px 30px; /* 行间距20px，列间距30px */
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 15px;
  align-items: start; /* 内容顶部对齐 */
}
.submit-btn {
  grid-column: 1 / -1;
  justify-self: center;
}
/* .el-form-item {
  box-sizing: border-box;
} */

/* 单列项目 */
.el-form-item.full-width {
  grid-column: span 2;
}

/* 响应式：小屏幕单列显示 */
@media (max-width: 768px) {
  .form-area {
    grid-template-columns: 1fr;
  }
  .el-form-item.full-width {
    grid-column: span 1;
  }
}

/* 确保标签和输入区关系 */
.el-form-item__label {
  padding-bottom: 8px !important;
  height: auto !important;
}
</style>
