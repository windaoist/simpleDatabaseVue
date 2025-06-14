<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { getPrimaryLabel, getTableSchema } from '@/utils/TableStructure'

const props = defineProps({
  currentTable: {
    type: String as () => 'student' | 'teacher' | 'project_submit' | 'project' | '',
    required: true,
  },
  researchFields: {
    type: Array as () => Array<{ id: string; research_field: string }>,
    required: true,
  },
  // 初始筛选数据（不包括成员）
  initialData: {
    type: Object as () => {
      filters: Record<string, any>
    } | null,
    default: null,
  },
})

const emit = defineEmits(['submit', 'update'])
const currentUser = ref(localStorage.getItem('current_user') || '')
const fields = ref([])
const primaryLabel = ref()
const tempInput = ref({
  member: '',
  teacher: '',
})
const memberList = ref({
  member: [] as Record<string, string>[],
  teacher: [] as Record<string, string>[],
})
const loading = ref({
  member: false,
  teacher: false,
})
const formData = ref({
  filters: {} as Record<string, any>,
})

// 计算属性判断是否为编辑模式
const isEditMode = computed(() => props.initialData !== null)

// 监听currentTable变化
watch(
  () => props.currentTable,
  (newVal) => {
    if (newVal) {
      onQuery(newVal)
    }
  },
  { immediate: true },
)
watch(
  () => props.initialData,
  (newVal) => {
    if (newVal) {
      initialize(props.currentTable)
    }
  },
  { deep: true, immediate: true },
)
function parseNameIdPairs(str: string): Record<string, string>[] {
  const result: Record<string, string>[] = []
  const regex = /([\u4e00-\u9fa5\w]+)\((\d+)\)/g
  let match
  while ((match = regex.exec(str)) !== null) {
    const name = match[1]
    const id = match[2]
    result.push({ [id]: name })
  }
  return result
}
function initialize(tableName) {
  // 如果有初始数据，则使用它填充表单
  if (props.initialData) {
    formData.value.filters = { ...props.initialData.filters }
    if (tableName == 'project') {
      memberList.value = {
        member: parseNameIdPairs(props.initialData.filters['member'] || ''),
        teacher: parseNameIdPairs(props.initialData.filters['teacher'] || ''),
      }
    }
  } else {
    // 否则初始化为空表单
    formData.value.filters = {}
    if (tableName == 'project') {
      memberList.value = {
        member: [] as Record<string, string>[],
        teacher: [] as Record<string, string>[],
      }
    }
  }

  primaryLabel.value = getPrimaryLabel(tableName) || ''
}
function onQuery(tableName: 'student' | 'teacher' | 'project_submit' | 'project') {
  try {
    const rawFields = getTableSchema(tableName)
    fields.value = rawFields.map((field) => {
      if (field.options && typeof field.options === 'object' && 'value' in field.options) {
        return { ...field, options: field.options.value }
      }
      return field
    })
    if (isEditMode.value) {
      initialize(tableName)
    }
  } catch (error) {
    ElMessage.error('获取表格式失败: ' + (error as Error).message)
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
        type: fieldName == 'member' ? 'student' : 'teacher',
        id: id,
      },
    })
    if (response.data.data['valid']) {
      if (memberList.value[fieldName].some((item) => id in item)) {
        ElMessage.warning(id + '已存在')
        return
      }
      const memberName =
        response.data.data[(fieldName == 'member' ? 'student' : 'teacher') + '_name']
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

function removeMember(fieldName: string, index: number) {
  memberList.value[fieldName].splice(index, 1)
}

function handleSubmit() {
  if (isEditMode.value) {
    // 编辑模式时触发 update 事件
    emit('update', {
      filters: formData.value.filters,
      memberList: memberList.value,
    })
  } else {
    // 创建模式时触发 submit 事件
    emit('submit', {
      filters: formData.value.filters,
      memberList: memberList.value,
    })
  }
}
</script>

<template>
  <div class="add-form" v-if="fields.length > 0">
    <el-form :model="formData" label-width="120px" ref="formRef">
      <div class="form-area">
        <el-form-item
          v-for="field in fields"
          :key="field.name"
          :label="field.label"
          style="flex: 1; min-width: 250px; margin-bottom: 20px"
        >
          <template v-if="field.name === 'leader'">
            <el-input
              v-if="field.name === 'leader'"
              :placeholder="currentUser"
              disabled
              style="width: 100%"
            />
          </template>
          <template v-else-if="field.name === 'member' || field.name === 'teacher'">
            <div class="input-row" style="width: 100%">
              <el-input
                v-model="tempInput[field.name]"
                :placeholder="
                  field.label === '成员' ? '输入学生的学号' : `输入${field.label}的工号`
                "
                @keyup.enter="validateAndAdd(field.name)"
                class="input-item"
                :disabled="isEditMode"
              />
              <el-button
                type="primary"
                @click="validateAndAdd(field.name)"
                :loading="loading[field.name]"
                :disabled="isEditMode"
              >
                添加
              </el-button>
            </div>

            <div class="tags-container">
              <el-tag
                v-for="(member, index) in memberList[field.name]"
                :key="index"
                type="info"
                :closable="!isEditMode"
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
            <el-select
              v-if="field.name === 'research_field'"
              v-model="formData.filters[field.name]"
              multiple
              placeholder="请选择研究领域"
              style="width: 100%"
            >
              <el-option
                v-for="item in researchFields"
                :key="item.id"
                :label="item.research_field"
                :value="item.research_field"
              />
            </el-select>

            <el-select
              v-else-if="field.name.includes('_status')"
              v-model="formData.filters[field.name]"
              placeholder="请选择状态"
              disabled
              style="width: 100%"
            >
            </el-select>

            <el-select
              v-else-if="field.name === 'gender'"
              v-model="formData.filters[field.name]"
              placeholder="请选择性别"
              style="width: 100%"
            >
              <el-option
                v-for="option in field.options"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>

            <el-input
              v-else-if="field.label === primaryLabel"
              v-model="formData.filters[field.name]"
              disabled
              type="textarea"
              :autosize="{ minRows: 1, maxRows: 4 }"
              style="width: 100%"
            />
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
          <el-button type="primary" @click="handleSubmit">
            {{ isEditMode ? '更新' : '提交' }}
          </el-button>
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<style scoped>
.input-row {
  display: flex;
  margin-bottom: 10px;
}

.input-item {
  flex: 1;
  margin-right: 10px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  margin-bottom: 5px;
}

.form-area {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px 30px;
  max-width: 1200px;
  margin: 20px 0px 0px 60px;
  padding: 0 15px;
  align-items: start;
}

.submit-btn {
  grid-column: 1 / -1;
  justify-self: center;
}

@media (max-width: 768px) {
  .form-area {
    grid-template-columns: 1fr;
  }
}

.el-form-item__label {
  padding-bottom: 8px !important;
  height: auto !important;
}
</style>
