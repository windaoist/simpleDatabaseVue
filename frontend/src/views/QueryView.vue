<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import request from '@/utils/request'
import * as translate from '@/stores/LanguageConverter'
import { getAttribute } from '@/stores/TableStructure'
import { ElMessage, ElMessageBox } from 'element-plus'

const queryForm = ref({
  table: '',
  filters: {},
  research_field: [],
})
const fields = ref([])
// const secondFieldKey = ref('')
// const formData = ref({
//   table: '',
//   filters: {},
//   research_field: [],
// })
const research_fields = ref()
const currentForm = ref()
// const editingState = reactive({});
// const editedData = ref([]);
const responseData = ref({
  data: {
    results: [],
    related_data: {
      相关学生: [],
      相关教职工: [],
      相关科研项目: [],
    },
  },
})
const activeName = ref()
// 新增：用于存储原始列顺序
// const columnOrder = ref([])
const primaryKey = ref()
async function onTableChange() {
  try {
    if (!queryForm.value.table) {
      ElMessage.error('请选择查询表名')
      return
    }
    // 获取表结构
    const attributes = await getAttribute(queryForm.value.table)
    fields.value = attributes
    responseData.value = {
      data: {
        results: [],
        related_data: {
          相关学生: [],
          相关教职工: [],
          相关科研项目: [],
        },
      },
    }
    // secondFieldKey.value = attributes[1] || ''
    console.log('表结构:', fields.value)
  } catch (error) {
    ElMessage.error('获取表格式失败，' + error.message)
  }
}
const onQuerySubmit = async () => {
  try {
    if (!queryForm.value.table) {
      ElMessage.error('请选择查询表名')
      return
    }
    console.log('research_field value:', queryForm.value.research_field)
    const payload = {
      table: queryForm.value.table,
      filters: queryForm.value.filters,
      research_field: queryForm.value.research_field
        .map((name) => {
          const match = research_fields.value.find((field) => field.research_field === name)
          return match ? match.id : null
        })
        .filter((id) => id !== null), // 过滤掉找不到的
    }
    const response = await request.post('query/', payload)

    responseData.value = response.data
    console.log(responseData.value.data)
    currentForm.value = queryForm.value.table // 保存当前查询表单数据
    // 获取除“序号”外的所有列名
    // const firstRow = responseData.value.data.results[0]
    // const keys = Object.keys(firstRow).filter((k) => k !== '序号')
    // columnOrder.value = keys
    // // 为每一行添加 __colOrder 字段
    const results = responseData.value.data.results
    if (results.length > 0) {
      // 取第一项的第一个键
      const firstItem = results[0]
      const firstKey = Object.keys(firstItem)[0]
      primaryKey.value = firstKey
      console.log('当前主键字段名:', firstKey)
      activeName.value = 'query-result' // 切换到查询结果标签
      console.log('查询结果:', responseData.value)
    }
  } catch (error) {
    console.error('查询失败:', error)
    ElMessage.error('查询失败：' + error.response?.data?.message)
  }
}
// 编辑状态
const editingId = ref(null)
const originalData = ref()
// 计算可编辑列（排除ID列），返回列名数组
const editableColumns = computed(() => {
  if (!responseData.value.data.results.length) return []
  // 优先用 columnOrder
  return fields.value.length
    ? Object.values(fields.value).map((key) => translate.translateToChinese(key))
    : Object.keys(responseData.value.data.results[0]).filter((k) => k !== '序号')
})

// 检查行是否在编辑状态
const isEditing = (index) => {
  return editingId.value === index
}

// 处理编辑操作
const handleEdit = (row, index) => {
  // 保存原始数据（深拷贝）
  originalData.value = JSON.parse(JSON.stringify(row))
  // console.log('123', originalData.value[row.序号]);
  editingId.value = index
}

// 处理重置操作
const handleReset = (row) => {
  // 恢复原始数据
  Object.assign(row, originalData.value)
  editingId.value = null
  originalData.value = null
}
// 处理提交操作
const handleSubmit = async (row) => {
  try {
    console.log('提交数据:', row)
    const primary = row[primaryKey.value]
    const payload = {
      table: currentForm.value,
      old_key: primary,
      data: {
        ...Object.fromEntries(
          Object.entries(row)
            .filter(([k]) => k !== '序号')
            .map(([k, v]) => [translate.translateToEnglish(k), v]),
        ),
      },
    }
    const response = await request.post('add-edit/edit', payload)
    ElMessage.success('提交成功：' + response.data.message)
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败:' + error.response?.data?.message)
  }
  // 清除编辑状态
  editingId.value = null
  // 移除备份数据
  originalData.value = null
}
async function handleDelete(row) {
  try {
    // 弹窗确认
    await ElMessageBox.confirm('确定要删除这条数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
      .then(() => {
        // 用户点击了确定
        console.log('用户确认删除')
      })
      .catch(() => {
        // 用户点击了取消
        console.log('用户取消删除')
        throw '取消' // 抛出异常以跳过后续操作
      })
    const primary = row[primaryKey.value]
    const payload = {
      table: currentForm.value,
      key: primary,
    }
    const response = request.post('add-edit/delete', payload)
    ElMessage.success('删除成功：' + (await response).data.message)
    // const colOrder = row.__colOrder
    // const keys = {}
    // if (colOrder && colOrder.length >= 2) {
    //   const [firstKey, secondKey] = colOrder.slice(0, 2)
    //   keys[0] = row[firstKey]
    //   keys[1] = row[secondKey]

    // 构造 payload
  } catch (error) {
    ElMessage.error('删除失败：' + error.response?.data?.message)
  }
}
async function onDownload() {
  try {
    const response = await request.get('export/excel', {
      params: {
        // keyword1: queryForm.value.keyword1,
        // keyword2: queryForm.value.keyword2,
        table: queryForm.value.table,
      },
    })
    if (response.data.success) {
      const url = response.data.download_url
      console.log('下载链接:', url)
      const link = document.createElement('a')
      link.href = url
      link.target = '_blank' // 可选
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  } catch (error) {
    ElMessage.error('导出失败:' + error.message)
  }
}
// const editingRow = ref()
// const editingContent = ref('')
// const contentDialogVisible = ref(false)
// function openContentDialog(row) {
//   editingRow.value = row
//   editingContent.value = row['教职工内容'] || ''
//   contentDialogVisible.value = true
// }

// function handleDialogSave() {
//   if (editingRow.value) {
//     editingRow.value['教职工内容'] = editingContent.value
//   }
//   contentDialogVisible.value = false
// }

// function handleDialogClose() {
//   contentDialogVisible.value = false
// }

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
// 行样式（编辑状态背景色）
// const getRowClassName = ({ row }) => {
//   return isEditing(row) ? 'editing-row' : '';
// };
</script>
<template>
  <div>
    <div class="query-view">
      <el-form :inline="true" label-position="left" label-width="80px" :model="queryForm">
        <el-form-item label="查询表名">
          <el-select
            v-model="queryForm.table"
            @change="onTableChange()"
            placeholder="请选择查询表名"
            style="width: 220px"
          >
            <el-option label="学生表" value="student" />
            <el-option label="教职工表" value="teacher" />
            <el-option label="科研项目表" value="project" />
          </el-select>
        </el-form-item>
        <div class="query-form-items">
          <el-form-item
            v-for="field in fields"
            :key="field"
            :label="translate.translateToChinese(field)"
            style="flex: 1; min-width: 200px"
          >
            <!-- 特殊处理“研究领域”为下拉框 -->
            <el-select
              v-if="field === 'research_field'"
              v-model="queryForm.research_field"
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

            <!-- 默认使用文本域 -->
            <el-input
              v-else
              type="textarea"
              :autosize="{ minRows: 1, maxRows: 6 }"
              v-model="queryForm.filters[field]"
              style="width: 80%"
            />
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary" @click="onQuerySubmit" class="submit-btn">查询</el-button>
          <el-button
            type="success"
            @click="onDownload"
            :disabled="!responseData.data"
            class="download-btn"
            >导出</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <!-- <div>
   <p>{{responseData}}</p>
</div> -->
    <!-- <el-dialog
      v-model="contentDialogVisible"
      title="编辑教职工内容"
      width="60%"
      :before-close="handleDialogClose"
    >
      <el-input
        type="textarea"
        v-model="editingContent"
        :rows="10"
        placeholder="请输入教职工内容"
        style="width: 100%"
      />
      <template #footer>
        <el-button @click="handleDialogClose">取消</el-button>
        <el-button type="primary" @click="handleDialogSave">保存</el-button>
      </template>
    </el-dialog> -->
    <el-tabs class="query-result" v-model="activeName" v-if="responseData.data">
      <el-tab-pane label="查询结果" name="query-result">
        <div class="section" v-if="responseData.data.results.length > 0">
          <el-table :data="responseData.data.results" :max-height="500" style="width: 100%">
            <!-- 固定第一列 (ID) -->
            <el-table-column type="index" :min-width="50" fixed="left"> </el-table-column>

            <!-- 动态数据列 -->
            <el-table-column
              v-for="key in editableColumns"
              :key="key"
              :label="key"
              :min-width="key.length * 15 + 30"
            >
              <template #default="{ row, $index }">
                <template v-if="isEditing($index)">
                  <el-input
                    v-model="row[key]"
                    type="textarea"
                    :autosize="true"
                    style="width: 100%"
                  />
                </template>
                <template v-else>
                  {{ row[key] }}
                </template>
              </template>
            </el-table-column>

            <!-- 固定操作列 -->
            <el-table-column label="操作" fixed="right" width="180">
              <template #default="{ row, $index }">
                <div v-if="isEditing($index)">
                  <el-button size="small" @click="handleReset(row)">重置</el-button>
                  <el-button size="small" type="primary" @click="handleSubmit(row)">提交</el-button>
                </div>
                <div v-else>
                  <el-button size="small" @click="handleEdit(row, $index)" :disabled="!!editingId">
                    编辑
                  </el-button>
                  <el-button size="small" @click="handleDelete(row)" :disabled="!!editingId">
                    删除
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无查询结果</div>
      </el-tab-pane>
      <!-- 相关数据展示 -->
      <el-tab-pane label="相关学生" name="related-students">
        <!-- 相关学生 -->
        <div class="section" v-if="responseData.data.related_data.相关学生.length > 0">
          <el-table :data="responseData.data.related_data.相关学生" border :max-height="500">
            <!-- 固定第一列 (ID) -->
            <el-table-column type="index" :min-width="50" fixed="left"> </el-table-column>
            <el-table-column
              v-for="key in Object.keys(responseData.data.related_data.相关学生[0] || {}).filter(
                (k) => k !== '序号',
              )"
              :key="key"
              :prop="key"
              :label="key"
            >
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无相关学生</div>
      </el-tab-pane>
      <!-- 相关教职工 -->
      <el-tab-pane label="相关教职工" name="related-teachers">
        <div class="section" v-if="responseData.data.related_data.相关教职工.length > 0">
          <el-table :data="responseData.data.related_data.相关教职工" border :max-height="500">
            <!-- 固定第一列 (ID) -->
            <el-table-column type="index" :min-width="50" fixed="left"> </el-table-column>
            <el-table-column
              v-for="key in Object.keys(responseData.data.related_data.相关教职工[0] || {}).filter(
                (k) => k !== '序号',
              )"
              :key="key"
              :prop="key"
              :label="key"
            >
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无相关教职工</div>
      </el-tab-pane>
      <!-- 相关教职工 -->
      <el-tab-pane label="相关科研项目" name="related-projects">
        <div class="section" v-if="responseData.data.related_data.相关科研项目.length > 0">
          <el-table :data="responseData.data.related_data.相关科研项目" border :max-height="500">
            <!-- 固定第一列 (ID) -->
            <el-table-column type="index" :min-width="50" fixed="left"> </el-table-column>
            <el-table-column
              v-for="key in Object.keys(
                responseData.data.related_data.相关科研项目[0] || {},
              ).filter((k) => k !== '序号')"
              :key="key"
              :prop="key"
              :label="key"
            >
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无相关科研项目</div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<style scoped>
.query-view {
  padding: 20px;
  margin: auto;
  height: fit-content;
  width: fit-content;
  min-width: 600px;
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.query-form-items {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: 10px auto;
  padding: 0 10px;
  gap: 10px; /* 添加间距 */
}
.el-form-item {
  margin-bottom: 18px;
}

.el-form-item label {
  font-weight: 600;
  color: #606266;
}

.el-input,
.el-select {
  transition: all 0.3s ease;
  width: 220px;
}

.el-input:hover,
.el-select:hover {
  box-shadow: 0 0 5px rgba(64, 158, 255, 0.3);
}

.submit-btn {
  width: 120px;
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(64, 158, 255, 0.3);
}
.query-result {
  color: black;
  /* max-height: 60vh; 限制最大高度 */
  overflow: auto; /* 添加垂直滚动 */
  height: 100%;
  flex: 1;
  margin-top: 20px;
  padding: 10px 10px 0px 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.102);
}
@media (max-width: 768px) {
  .query-view {
    height: fit-content;
    overflow-y: auto;
  }
}
/* 编辑行背景色
:deep(.el-table .editing-row) {
  --el-table-tr-bg-color: #f0f9eb;
} */
</style>
