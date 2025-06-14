<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import request from '@/utils/request'
import * as translate from '@/utils/LanguageConverter'
import { getTableSchema, getPrimaryKey, getPrimaryLabel } from '@/utils/TableStructure'
import { ElMessage, ElMessageBox } from 'element-plus'
import AddForm from '@/components/AddForm.vue'
const queryForm = ref({
  table: '' as 'student' | 'teacher' | 'project' | 'project_submit' | '',
  filters: {} as Record<string, any>,
  // 移除了单独的 research_field，现在它包含在 filters 中
})

// 表结构字段
const fields = ref<
  Array<{
    name: string
    label: string
    type: string
    options?: Array<any>
    valueKey?: string
    labelKey?: string
  }>
>([])

const research_fields = ref<Array<{ id: string; research_field: string }>>([])
// const currentForm = ref('')
const responseData = ref({
  data: {
    results: [] as any[],
    related_data: {
      相关学生: [] as any[],
      相关教职工: [] as any[],
      相关科研项目: [] as any[],
    },
  },
})
const activeName = ref()
const primaryKey = ref()
const primaryLabel = ref()
const dialogVisible = ref(false)
const selectedRow = ref(null)

function openEditDialog(row) {
  selectedRow.value = { ...row } // 深拷贝，避免原表数据污染
  dialogVisible.value = true
}
// 当表名改变时获取表结构
function onTableChange() {
  try {
    if (!queryForm.value.table) {
      ElMessage.error('请选择查询表名')
      return
    }

    // 获取表结构
    const rawFields = getTableSchema(queryForm.value.table)
    // 如果 options 是 Ref，则取其 value，否则保持原样
    fields.value = rawFields.map((field) => {
      if (field.options && typeof field.options === 'object' && 'value' in field.options) {
        return { ...field, options: field.options.value }
      }
      return field
    })

    // 重置查询条件和结果
    queryForm.value.filters = {}
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

    // 获取主键
    primaryKey.value = getPrimaryKey(queryForm.value.table) || ''
    primaryLabel.value = getPrimaryLabel(queryForm.value.table) || ''
    console.log('表结构:', fields.value)
  } catch (error) {
    ElMessage.error('获取表格式失败: ' + (error as Error).message)
  }
}
const onQuerySubmit = async () => {
  try {
    if (!queryForm.value.table) {
      ElMessage.error('请选择查询表名')
      return
    }

    // 准备查询参数
    const payload = {
      table: queryForm.value.table,
      filters: {} as Record<string, any>,
      research_field: queryForm.value.filters.research_field
        ? queryForm.value.filters.research_field
            .map((name) => {
              const match = research_fields.value.find((field) => field.research_field === name)
              return match ? match.id : null
            })
            .filter((id) => id !== null)
        : null, // 过滤掉找不到的
    }

    // 处理过滤器参数 - 只包含有值的字段
    Object.keys(queryForm.value.filters).forEach((key) => {
      const value = queryForm.value.filters[key]
      if (value !== '' && value !== null && value !== undefined) {
        // 如果是数组且为空，则不添加
        if ((Array.isArray(value) && value.length === 0) || key == 'research_field') return

        payload.filters[key] = value
      }
    })

    const response = await request.post('query/', payload)
    responseData.value = response.data

    if (responseData.value.data.results.length > 0) {
      activeName.value = 'query-result' // 切换到查询结果标签
    }
  } catch (error) {
    console.error('查询失败:', error)
    ElMessage.error(
      '查询失败：' + ((error as any).response?.data?.message || (error as Error).message),
    )
  }
}

// 编辑状态
const editingId = ref(null)
const originalData = ref()
// 计算可编辑列（排除ID列），返回列名数组
const editableColumns = computed(() => {
  if (!responseData.value.data.results.length) return []
  return fields.value.length
    ? fields.value.map((item) => item.label)
    : Object.keys(responseData.value.data.results[0]).filter((k) => k !== '序号')
})

// // 检查行是否在编辑状态
// const isEditing = (index) => {
//   return editingId.value === index
// }

// // 处理编辑操作
// const handleEdit = (row, index) => {
//   // 保存原始数据（深拷贝）
//   originalData.value = JSON.parse(JSON.stringify(row))
//   // console.log('123', originalData.value[row.序号]);
//   editingId.value = index
// }

// // 处理重置操作
// const handleReset = (row) => {
//   // 恢复原始数据
//   Object.assign(row, originalData.value)
//   editingId.value = null
//   originalData.value = null
// }
// 处理提交操作
async function handleSubmit(formData: { filters: any; memberList: any }) {
  try {
    console.log('提交数据:', formData.filters)
    const payload = {
      table: queryForm.value.table,
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
    const primary = row[primaryLabel.value]
    const payload = {
      table: queryForm.value.table,
      key: primary,
    }
    const response = await request.post('add-edit/delete', payload)
    responseData.value.data.results = responseData.value.data.results.filter(
      (item) => item[primaryLabel.value] !== primary,
    )
    ElMessage.success((await response).data.message)
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
    <!-- 编辑弹窗 -->
    <el-dialog v-model="dialogVisible" title="编辑记录" width="50%">
      <div>
        <AddForm
          :current-table="queryForm.table"
          :research-fields="research_fields"
          :initial-data="{
            filters: Object.fromEntries(
              Object.entries(selectedRow)
                .filter(([k]) => k !== '序号')
                .map(([k, v]) => {
                  const translatedKey = translate.translateToEnglish(k)
                  if (translatedKey === 'research_field' && typeof v === 'string') {
                    return [translatedKey, v.split('、')]
                  }
                  return [translatedKey, v]
                }),
            ),
          }"
          @update="handleSubmit"
        />
      </div>
    </el-dialog>
    <div class="query-view">
      <el-form :inline="true" label-position="left" label-width="100px" :model="queryForm">
        <el-form-item label="查询表名">
          <el-select
            v-model="queryForm.table"
            @change="onTableChange"
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
            :key="field.name"
            :label="field.label"
            style="flex: 1; min-width: 250px; margin-bottom: 20px"
          >
            <!-- 研究领域字段 - 多选下拉 -->
            <el-select
              v-if="field.name === 'research_field'"
              v-model="queryForm.filters[field.name]"
              multiple
              collapse-tags
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
              v-model="queryForm.filters[field.name]"
              placeholder="请选择状态"
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

            <!-- 性别字段 - 下拉选择 -->
            <el-select
              v-else-if="field.name === 'gender'"
              v-model="queryForm.filters[field.name]"
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
              v-model="queryForm.filters[field.name]"
              :placeholder="`请输入${field.label}`"
              clearable
              style="width: 100%"
            />
          </el-form-item>
        </div>

        <el-form-item style="margin-top: 20px">
          <el-button type="primary" @click="onQuerySubmit" class="submit-btn">查询</el-button>
          <el-button
            type="success"
            @click="onDownload"
            :disabled="!responseData.data.results || responseData.data.results.length === 0"
            class="download-btn"
          >
            导出
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-tabs type="border-card" class="query-result" v-model="activeName" v-if="responseData.data">
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
              :prop="key"
              :min-width="key.length * 15 + 30"
            >
            </el-table-column>

            <!-- 固定操作列 -->
            <el-table-column label="操作" fixed="right" width="180">
              <template #default="{ row }">
                <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
                <el-button size="small" @click="handleDelete(row)">删除</el-button>
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
