<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
import * as translate from '@/stores/LanguageConverter'
import { ElMessage } from 'element-plus'
import { getAttribute } from '@/stores/TableStructure'
const currentTable = ref('student')
const fields = ref([])
const formData = ref({
  table: '',
  filters: {},
  research_field: [],
})
const research_fields = ref([])
const secondFieldKey = ref('')
async function onQuery() {
  try {
    if (!currentTable.value) {
      ElMessage.error('请选择查询表名')
      return
    }
    // 获取表结构
    const attributes = await getAttribute(currentTable.value)
    fields.value = attributes
    secondFieldKey.value = attributes[1] || ''
    console.log('表结构:', fields.value)
  } catch (error) {
    ElMessage.error('获取表格式失败，' + error.message)
  }
}
async function handleSubmit() {
  const processedData = { ...formData.value }
  // 处理第二个字段：如果匹配 industries，替换为 id
  const secondFieldValue = formData.value[secondFieldKey.value]
  const matchedIndustry = research_fields.value.find(
    (industry) => industry.industry_name === secondFieldValue,
  )

  if (matchedIndustry) {
    processedData[secondFieldKey.value] = matchedIndustry.id
  }
  const payload = {
    table: currentTable.value,
    data: {},
  }
  Object.keys(processedData).forEach((key) => {
    const newKey = translate.translateToEnglish(key)
    payload.data[newKey] = processedData[key]
  })
  console.log('提交数据:', payload)
  try {
    const response = await request.post('add-edit/add', payload, {
      headers: {
        Accept: '*/*',
        'Content-Type': 'application/json',
      },
    })
    if (response.data.success) {
      ElMessage.success(response.data.message)
      // 清空表单数据
      fields.value = []
      formData.value = {
        table: '',
        filters: {},
        research_field: [],
      }
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('提交数据失败:', error)
    ElMessage.error('提交数据失败，' + error.message)
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
        <el-option label="科研项目表" value="project" />
      </el-select>
      <!-- <el-button type="primary" @click="onQuery" style="margin-left: 10px;">
  查询
</el-button> -->
    </div>
    <div class="add-form" v-if="fields.length > 0">
      <el-form :model="formData" label-width="120px" ref="formRef">
        <div class="form-grid">
          <el-form-item
            v-for="field in fields"
            :key="field"
            :label="translate.translateToChinese(field)"
          >
            <!-- 第二项为下拉框 -->
            <!-- <el-select
              v-if="index === 1"
              v-model="formData[field]"
              placeholder="请选择"
              style="width: 100%"
            >
              <el-option
                v-for="industry in industries"
                :key="industry.id"
                :label="industry.industry_name"
                :value="industry.industry_name"
              ></el-option>
            </el-select> -->

            <!-- 其他项为文本域 -->
            <el-select
              v-if="field === 'research_field'"
              v-model="formData.research_field"
              multiple
              collapse-tags
              placeholder="请选择研究领域"
              style="width: 100%"
            >
              <el-option
                v-for="field in research_fields"
                :key="field.id"
                :label="field.research_field"
                :value="field.research_field"
              />
            </el-select>
            <el-input
              v-else
              type="textarea"
              :autosize="true"
              style="width: 100%"
              v-model="formData[field]"
            />
          </el-form-item>

          <el-form-item>
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

.form-grid {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: 10px auto;
  padding: 0 10px;
  gap: 10px; /* 添加间距 */
}

.el-form-item {
  flex: 1 1 calc(50% - 16px);
  box-sizing: border-box;
  width: 100%;
}
</style>
