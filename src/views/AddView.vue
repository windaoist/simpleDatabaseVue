<script setup>
import { ref,onMounted } from 'vue'
import request from '@/utils/request';
import * as translate from '@/stores/LanguageConverter.ts';
import { ElMessage } from 'element-plus';
const currentTable= ref('Expert')
const fields = ref([]);
const formData = ref({});
const industries=ref([]);
const secondFieldKey = ref('');
async function onQuery() {
  try{
  const response = await request.get('query/',{params:{
    table: currentTable.value
  }});
  if (response.data.success) {
    fields.value = Object.keys(response.data.data.results[0]).filter(key => key !== '序号');
      // 记录第二个字段 key
    if (fields.value.length >= 2) {
      secondFieldKey.value = fields.value[1];
    }
    fields.value.forEach((key) => {
      formData[key] = ''
    })
    console.log('获取表格式成功', fields.value);
  }}catch(error) {
    ElMessage.error('获取表格式失败');
  }
}
async function handleSubmit() {
  
  const processedData = { ...formData.value };
  // 处理第二个字段：如果匹配 industries，替换为 id
  const secondFieldValue = formData.value[secondFieldKey.value];
  const matchedIndustry = industries.value.find(
    industry => industry.industry_name === secondFieldValue
  );

  if (matchedIndustry) {
    processedData[secondFieldKey.value] = matchedIndustry.id;
  }
  const payload= {
    "table": currentTable.value,
    "data": {}
  };
  Object.keys(processedData).forEach(key => {
        const newKey = translate.translateToEnglish(key);
        payload.data[newKey] = processedData[key];
  });
  console.log('提交数据:', payload);
  try{
  const response = await request.post('add-edit/add',payload, {           headers: {
                'Accept': '*/*',
                'Content-Type': 'application/json'
            }
    });
    if (response.data.success) {
    ElMessage.success(response.data.message);
    // 清空表单数据
    fields.value=[];
    formData.value = {};
  } else {
    ElMessage.error(response.data.message);
  }
  } catch (error) {
    console.error('提交数据失败:', error);
    ElMessage.error('提交数据失败，' + error.message);
}
}
async function fetchIndustries() {
  try {
    const response = await request.get('add-edit/industries');
    industries.value = response.data.data.industries;
    console.log('行业列表:', industries.value);
  } catch (error) {
    console.error('获取行业列表失败:', error);
  }
}
onMounted(() => {
  // 初始化行业列表
  fetchIndustries();
  onQuery(); // 默认查询专家表
});
</script>
<template>
<div>
<div class="query-view">
  <h3>选择要添加项的表</h3>
<el-select v-model="currentTable" @change="onQuery()" placeholder="请选择添加表表名" style="width: 220px;">
  <el-option label="专家表" value="Expert"></el-option>
  <el-option label="项目表" value="Project"></el-option>
  <el-option label="基金表" value="Fund"></el-option>
</el-select>
<!-- <el-button type="primary" @click="onQuery" style="margin-left: 10px;">
  查询
</el-button> -->
</div>
<div class="add-form" v-if="fields.length > 0">
  <el-form :model="formData" label-width="120px" ref="formRef">
    <div class="form-grid">
<el-form-item
  v-for="(field, index) in fields"
  :key="field"
  :label="field"
>
  <!-- 第二项为下拉框 -->
  <el-select
    v-if="index === 1"
    v-model="formData[field]"
    placeholder="请选择"
    style="width: 100%"
  >
        <el-option v-for="industry in industries" :key="industry.id" :label="industry.industry_name" :value="industry.industry_name"></el-option>
  </el-select>

  <!-- 其他项为文本域 -->
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
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 16px; /* 间距可根据需要调整 */
  margin-top:20px;
}

.form-grid .el-form-item {
  flex: 1 1 calc(50% - 16px); /* 每项宽度为 50% 减去间距 */
  box-sizing: border-box;
}
</style>