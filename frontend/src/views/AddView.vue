<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'
import { getPrimaryKey, getTableSchema } from '@/stores/TableStructure'
const currentTable = ref('student' as 'student' | 'teacher' | 'project_submit' | '')
const fields = ref([])
const primaryKey = ref()

const tempInput = ref({
  members: '',
  instructors: '',
}) // 加载状态
const memberList = ref({
  members: [] as Record<string, string>[],
  instructors: [] as Record<string, string>[],
})
const loading = ref({
  members: false,
  instructors: false,
})
const formData = ref({
  table: '' as 'student' | 'teacher' | 'project_submit' | '',
  filters: {} as Record<string, any>,
})
const research_fields = ref([])
async function onQuery() {
  if (!currentTable.value) {
    ElMessage.error('请选择查询表名')
    return
  }
  try {
    // 获取表结构
    const rawFields = getTableSchema(currentTable.value)
    // 如果 options 是 Ref，则取其 value，否则保持原样
    fields.value = rawFields.map((field) => {
      if (field.options && typeof field.options === 'object' && 'value' in field.options) {
        return { ...field, options: field.options.value }
      }
      return field
    })
    // 重置查询条件和结果
    formData.value.filters = {}
    formData.value.table = currentTable.value
    memberList.value = {
      members: [] as Record<string, string>[],
      instructors: [] as Record<string, string>[],
    }
    // 获取主键
    primaryKey.value = getPrimaryKey(formData.value.table) || ''
    // if (currentTable.value === 'project_submit') {
    //   formData.value.filters.head = localStorage.getItem('current_user')
    // }
    console.log('表结构:', fields.value)
  } catch (error) {
    ElMessage.error('获取表格式失败: ' + (error as Error).message)
  }
}
async function handleSubmit() {
  try {
    const payload = {
      table: currentTable.value == 'project_submit' ? 'project' : currentTable.value,
      data: {
        ...formData.value.filters,
        research_field: formData.value.filters.research_field
          ? formData.value.filters.research_field
              .map((name) => {
                const match = research_fields.value.find((field) => field.research_field === name)
                return match ? match.id : null
              })
              .filter((id) => id !== null)
          : null, // 过滤掉找不到的
      },
    }
    if (Array.isArray(payload.data.research_field)) {
      payload.data.research_field = payload.data.research_field.join('、')
    }
    if (currentTable.value == 'project_submit') {
      payload.data['member_ids'] = memberList.value.members
        .flatMap((member) => Object.keys(member))
        .join('、')
      payload.data['teacher_ids'] = memberList.value.instructors
        .flatMap((member) => Object.keys(member))
        .join('、')
    }
    const response = await request.post('add-edit/add', payload)
    ElMessage.success('添加成功：' + response.data.message)
  } catch (error) {
    ElMessage.error('添加失败：' + error.response?.data?.message)
  }
}
async function validateAndAdd(fieldName: string) {
  if (!tempInput.value[fieldName]) {
    ElMessage.error('不能添加空值')
    return
  }
  try {
    const id = tempInput.value[fieldName].trim()
    loading.value[fieldName] = true
    const response = await request.get('add-edit/validate_id', {
      params: {
        type: fieldName == 'members' ? 'student' : 'teacher',
        id: id,
      },
    })
    if (response.data.data['valid']) {
      if (memberList.value[fieldName].some((item) => id in item)) {
        ElMessage.warning(id + '已存在')
        return
      }
      const memberName =
        response.data.data[(fieldName == 'members' ? 'student' : 'teacher') + '_name']
      memberList.value[fieldName].push({ [id]: memberName })
    } else {
      ElMessage.error('不存在此学生／教职工')
    }
  } catch (error) {
    ElMessage.error('添加成员／指导教师失败：' + error.response?.data?.message)
  } finally {
    loading.value[fieldName] = false
  }
}
async function removeMember(fieldName, index) {
  memberList.value[fieldName].splice(index, 1)
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
  onQuery() // 默认查询专家表
})
</script>
<template>
  <div>
    <div class="query-view">
      <h3>选择要添加项的表</h3>
      <el-select
        v-model="currentTable"
        @change="onQuery()"
        placeholder="请选择添加表表名"
        style="width: 220px"
      >
        <el-option label="学生表" value="student" />
        <el-option label="教职工表" value="teacher" />
        <el-option label="科研项目表" value="project_submit" />
      </el-select>
      <!-- <el-button type="primary" @click="onQuery" style="margin-left: 10px;">
  查询
</el-button> -->
    </div>
    <div class="add-form" v-if="fields.length > 0">
      <el-form :model="formData" label-width="120px" ref="formRef">
        <div class="form-area">
          <el-form-item
            v-for="field in fields"
            :key="field.name"
            :label="field.label"
            style="flex: 1; min-width: 250px; margin-bottom: 20px"
          >
            <template v-if="field.name === 'head'">
              <el-input
                v-if="field.name === 'head'"
                v-model="formData.filters[field.name]"
                placeholder="负责人"
                disabled
                style="width: 100%"
              />
            </template>
            <template v-else-if="field.name === 'members' || field.name === 'instructors'">
              <!-- 输入行：输入框 + 按钮 (同一行) -->
              <div class="input-row" style="width: 100%">
                <el-input
                  v-model="tempInput[field.name]"
                  :placeholder="
                    field.label === '成员' ? '输入学生的学号' : `输入${field.label}的工号`
                  "
                  @keyup.enter="validateAndAdd(field.name)"
                  class="input-item"
                />
                <el-button
                  type="primary"
                  @click="validateAndAdd(field.name)"
                  :loading="loading[field.name]"
                >
                  添加
                </el-button>
              </div>

              <!-- 标签展示区 (单独一行) -->
              <div class="tags-container">
                <el-tag
                  v-for="(member, index) in memberList[field.name]"
                  :key="index"
                  type="info"
                  closable
                  @close="removeMember(field.name, index)"
                  class="tag-item"
                >
                  <div v-for="[key, value] in Object.entries(member)" :key="key">
                    {{ key }}：{{ value }}
                  </div>
                </el-tag>
              </div>
            </template>
            <template v-else>
              <!-- 研究领域字段 - 多选下拉 -->
              <el-select
                v-if="field.name === 'research_field'"
                v-model="formData.filters[field.name]"
                multiple
                placeholder="请选择研究领域"
                style="width: 100%"
              >
                <el-option
                  v-for="item in research_fields"
                  :key="item.id"
                  :label="item.research_field"
                  :value="item.research_field"
                />
              </el-select>

              <!-- 状态字段 - 下拉选择 -->
              <el-select
                v-else-if="field.name.includes('_status')"
                v-model="formData.filters[field.name]"
                placeholder="请选择状态"
                clearable
                @close="removeMember"
                style="width: 100%"
              >
                <el-option
                  v-for="option in field.options"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>

              <!-- 性别字段 - 下拉选择 -->
              <el-select
                v-else-if="field.name === 'gender'"
                v-model="formData.filters[field.name]"
                placeholder="请选择性别"
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="option in field.options"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>

              <!-- 其他字段 - 文本输入 -->
              <el-input
                v-else
                v-model="formData.filters[field.name]"
                :placeholder="`请输入${field.label}`"
                clearable
                type="textarea"
                :autosize="{ minRows: 1, maxRows: 4 }"
                style="width: 100%"
              />
            </template>
          </el-form-item>
          <el-form-item label=" " class="submit-btn">
            <el-button type="primary" @click="handleSubmit">提交</el-button>
          </el-form-item>
        </div>
      </el-form>
    </div>
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
