<script setup lang="ts">
import request from '@/utils/request'
import { ElMessage } from 'element-plus'
async function uploadFile(option) {
  const { file, onProgress } = option

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await request.post('/upload/', formData, {
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
      ElMessage.error(response.data.message || '上传失败，请稍后再试')
      return
    }
    ElMessage.info('上传成功！')
  } catch (error) {
    // console.error(error)
    // onError(error)
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
</script>
<template>
  <el-upload
    class="upload"
    drag
    action=""
    multiple
    :http-request="uploadFile"
    :before-upload="beforeUpload"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">拖动文件至此或 <em>点击上传</em></div>
    <template #tip>
      <div class="el-upload__tip">
        上传的文件名必须为“学生库.xlsx”，“教职工库.xlsx”或“科研项目库.xlsx”，且文件大小不超过 10MB。
      </div>
    </template>
  </el-upload>
</template>
<style scoped></style>
