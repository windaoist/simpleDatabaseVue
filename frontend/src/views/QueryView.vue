<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import request from '@/utils/request'
// import * as translate from '@/stores/LanguageConverter.ts'
import { ElMessage, ElMessageBox } from 'element-plus'

const queryForm = ref({
  keyword1: '',
  keyword2: '',
  table: '',
})
const industries = ref()
const currentForm = ref()
// const editingState = reactive({});
// const editedData = ref([]);
const responseData = ref({
  data: {
    results: [],
    related_data: {
      related_experts: [],
      related_projects: [],
      related_funds: [],
    },
  },
})
const activeName = ref()
// 新增：用于存储原始列顺序
const columnOrder = ref([])

const onQuerySubmit = async () => {
  try {
    if (!queryForm.value.table) {
      ElMessage.error('请选择查询表名')
      return
    }
    const response = await request.get('query/', {
      params: {
        keyword1: queryForm.value.keyword1,
        keyword2: queryForm.value.keyword2,
        table: queryForm.value.table,
      },
    })
    responseData.value = response.data
    currentForm.value = queryForm.value.table // 保存当前查询表单数据
    // 新增：为每一行添加原始列顺序
    if (responseData.value.data && responseData.value.data.results.length > 0) {
      // 获取除“序号”外的所有列名
      const firstRow = responseData.value.data.results[0]
      const keys = Object.keys(firstRow).filter((k) => k !== '序号')
      columnOrder.value = keys
      // 为每一行添加 __colOrder 字段
      responseData.value.data.results.forEach((row) => {
        row.__colOrder = [...keys]
      })
      activeName.value = 'query-result' // 切换到查询结果标签
    }
    console.log('查询结果:', responseData.value)
  } catch (error) {
    console.error('查询失败:', error)
    ElMessage.error('查询失败：' + error.message)
  }
}
// 编辑状态
const editingId = ref(null)
const originalData = ref({})
// 计算可编辑列（排除ID列），返回列名数组
const editableColumns = computed(() => {
  if (!responseData.value.data.results.length) return []
  // 优先用 columnOrder
  return columnOrder.value.length
    ? columnOrder.value
    : Object.keys(responseData.value.data.results[0]).filter(
        (k) => k !== '序号' && k !== '__colOrder',
      )
})

// 检查行是否在编辑状态
const isEditing = (row) => {
  return editingId.value === row.序号
}

// 处理编辑操作
const handleEdit = (row) => {
  // 保存原始数据（深拷贝）
  originalData.value[row.序号] = JSON.parse(JSON.stringify(row))
  // console.log('123', originalData.value[row.序号]);
  editingId.value = row.序号
}

// 处理重置操作
const handleReset = (row) => {
  // 恢复原始数据
  Object.assign(row, originalData.value[row.序号])
  editingId.value = null
}
// 处理提交操作
const handleSubmit = async (row) => {
  try {
    console.log('提交数据:', row)
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败:' + error.message)
  }
  // 清除编辑状态
  editingId.value = null
  // 移除备份数据
  delete originalData.value[row.序号]
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

    const colOrder = row.__colOrder
    const keys = {}
    if (colOrder && colOrder.length >= 2) {
      const [firstKey, secondKey] = colOrder.slice(0, 2)
      keys[0] = row[firstKey]
      keys[1] = row[secondKey]

      // 构造 payload
      const payload = {
        table: currentForm.value,
        key1: keys[0],
        key2: keys[1],
      }
      console.log(row)
      // 发送 POST 请求
      const response = await request.post('/add-edit/delete', payload)

      if (response.data && response.data.success) {
        ElMessage.success('删除成功')
        responseData.value.data.results = responseData.value.data.results.filter(
          (item) => item[firstKey] !== keys[0] || item[secondKey] !== keys[1],
        )
      } else {
        ElMessage.error(response.data?.message || '删除失败')
      }
    } else {
      throw new Error('数据错误')
    }
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
  }
}
async function onDownload() {
  try {
    const response = await request.get('export/excel', {
      params: {
        keyword1: queryForm.value.keyword1,
        keyword2: queryForm.value.keyword2,
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
const editingRow = ref()
const editingContent = ref('')
const contentDialogVisible = ref(false)
function openContentDialog(row) {
  editingRow.value = row
  editingContent.value = row['项目内容'] || ''
  contentDialogVisible.value = true
}

function handleDialogSave() {
  if (editingRow.value) {
    editingRow.value['项目内容'] = editingContent.value
  }
  contentDialogVisible.value = false
}

function handleDialogClose() {
  contentDialogVisible.value = false
}

async function fetchIndustries() {
  try {
    const response = await request.get('add-edit/industries')
    industries.value = response.data.data.industries
    console.log('行业列表:', industries.value)
  } catch (error) {
    console.error('获取行业列表失败:', error)
  }
}
onMounted(() => {
  // 初始化行业列表
  fetchIndustries()
})
// 行样式（编辑状态背景色）
// const getRowClassName = ({ row }) => {
//   return isEditing(row) ? 'editing-row' : '';
// };
</script>
<template>
  <div>
    <div class="query-view">
      <el-form :inline="true" :model="queryForm">
        <div class="query-form-items">
          <el-form-item label="关键字1">
            <el-input v-model="queryForm.keyword1" placeholder="主要关键字"></el-input>
          </el-form-item>
          <el-form-item label="关键字2">
            <!-- <el-input v-model="queryForm.keyword2" placeholder="次要关键字"></el-input> -->
            <el-select
              v-model="queryForm.keyword2"
              clearable
              placeholder="次要关键字"
              style="width: 220px"
            >
              <el-option
                v-for="industry in industries"
                :key="industry.id"
                :label="industry.industry_name"
                :value="industry.industry_name"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="查询表名">
            <el-select v-model="queryForm.table" placeholder="请选择查询表名" style="width: 220px">
              <el-option label="专家表" value="Expert"></el-option>
              <el-option label="项目表" value="Project"></el-option>
              <el-option label="基金表" value="Fund"></el-option>
            </el-select>
          </el-form-item>
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
        </div>
      </el-form>
    </div>
    <!-- <div>
   <p>{{responseData}}</p>
</div> -->
    <el-dialog
      v-model="contentDialogVisible"
      title="编辑项目内容"
      width="60%"
      :before-close="handleDialogClose"
    >
      <el-input
        type="textarea"
        v-model="editingContent"
        :rows="10"
        placeholder="请输入项目内容"
        style="width: 100%"
      />
      <template #footer>
        <el-button @click="handleDialogClose">取消</el-button>
        <el-button type="primary" @click="handleDialogSave">保存</el-button>
      </template>
    </el-dialog>
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
              :prop="key"
              :label="key"
              :min-width="key.length * 15 + 30"
            >
              <template #default="{ row }">
                <template v-if="isEditing(row)">
                  <!-- 如果是项目内容字段，使用弹窗 -->
                  <template v-if="key === '项目内容'">
                    <el-button @click="openContentDialog(row)" size="small">编辑内容</el-button>
                  </template>
                  <template v-else>
                    <el-input
                      v-model="row[key]"
                      type="textarea"
                      :autosize="true"
                      style="width: 100%"
                    />
                  </template>
                </template>
                <template v-else>
                  {{ row[key] }}
                </template>
              </template>
            </el-table-column>

            <!-- 固定操作列 -->
            <el-table-column label="操作" fixed="right" width="180">
              <template #default="{ row }">
                <div v-if="isEditing(row)">
                  <el-button size="small" @click="handleReset(row)">重置</el-button>
                  <el-button size="small" type="primary" @click="handleSubmit(row)">提交</el-button>
                </div>
                <div v-else>
                  <el-button size="small" @click="handleEdit(row)" :disabled="!!editingId">
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
      <el-tab-pane label="相关专家" name="related-experts">
        <!-- 相关专家 -->
        <div class="section" v-if="responseData.data.related_data.related_experts.length > 0">
          <el-table :data="responseData.data.related_data.related_experts" border :max-height="500">
            <el-table-column
              v-for="(value, key) in responseData.data.related_data.related_experts[0]"
              :key="key"
              :prop="key"
              :label="key"
            >
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无相关专家</div>
      </el-tab-pane>
      <!-- 相关项目 -->
      <el-tab-pane label="相关项目" name="related-projects">
        <div class="section" v-if="responseData.data.related_data.related_projects.length > 0">
          <el-table
            :data="responseData.data.related_data.related_projects"
            border
            :max-height="500"
          >
            <el-table-column
              v-for="(value, key) in responseData.data.related_data.related_projects[0]"
              :key="key"
              :prop="key"
              :label="key"
            >
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无相关项目</div>
      </el-tab-pane>
      <!-- 相关基金 -->
      <el-tab-pane label="相关基金" name="related-funds">
        <div class="section" v-if="responseData.data.related_data.related_funds.length > 0">
          <el-table :data="responseData.data.related_data.related_funds" border :max-height="500">
            <el-table-column
              v-for="(value, key) in responseData.data.related_data.related_funds[0]"
              :key="key"
              :prop="key"
              :label="key"
            >
            </el-table-column>
          </el-table>
        </div>
        <div v-else>无相关基金</div>
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
@media (max-width: 768px) {
  .query-view {
    height: fit-content;
    overflow-y: auto;
  }
}
.query-form-items {
  display: flex;
  justify-content: center;
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
  max-height: 60vh; /* 限制最大高度 */
  overflow: auto; /* 添加垂直滚动 */
  flex: 1;
  margin-top: 20px;
  padding: 10px 10px 0px 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.102);
}
/* 编辑行背景色
:deep(.el-table .editing-row) {
  --el-table-tr-bg-color: #f0f9eb;
} */
</style>
