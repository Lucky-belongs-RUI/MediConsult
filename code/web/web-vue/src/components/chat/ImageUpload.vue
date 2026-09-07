<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElUpload, ElButton, ElImage, ElMessage, ElIcon } from 'element-plus'
import { Picture, Delete, View, Upload } from '@element-plus/icons-vue'
import { fileRequest } from '@/api/file_request'
import type { UploadFile, UploadFiles, UploadProps } from 'element-plus'

interface FileUploadResponse {
  url: string
  bucket: string
  objectKey: string
}

const props = defineProps<{
  modelValue?: FileUploadResponse | null
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [file: FileUploadResponse | null]
}>()

const uploadRef = ref()
const fileList = ref<UploadFiles>([])
const uploadedFile = ref<FileUploadResponse | null>(null)
const previewVisible = ref(false)
const previewImageUrl = ref('')
const uploading = ref(false)

const hasFile = computed(() => uploadedFile.value !== null)

const beforeUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const isImage = rawFile.type.startsWith('image/')
  const isLt10M = rawFile.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }
  return true
}

const handleFileChange: UploadProps['onChange'] = async (uploadFile) => {
  if (uploadFile.raw && uploadFile.status === 'ready') {
    uploading.value = true
    
    try {
      const response = await fileRequest.upload<FileUploadResponse>('medical-images', uploadFile.raw as any)
      
      uploadedFile.value = response
      emit('update:modelValue', response)

      previewImageUrl.value = response.url
      
      ElMessage.success('图片上传成功')
      
    } catch (error: any) {
      console.error('图片上传失败:', error)
      ElMessage.error(error.message || '图片上传失败')

      uploadRef.value?.clearFiles()
      fileList.value = []
    } finally {
      uploading.value = false
    }
  }
}

const handleRemove: UploadProps['onRemove'] = async () => {
  if (uploadedFile.value) {
    try {
      await fileRequest.delete(uploadedFile.value.bucket, uploadedFile.value.objectKey)
    } catch (error) {
      console.error('删除文件失败:', error)
    }
  }
  
  uploadedFile.value = null
  emit('update:modelValue', null)
  previewImageUrl.value = ''
  fileList.value = []
}

const handlePreview = () => {
  if (previewImageUrl.value) {
    previewVisible.value = true
  }
}

const triggerUpload = () => {
  uploadRef.value?.clearFiles()
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]
    if (file && beforeUpload(file)) {
      uploading.value = true
      
      try {
        const response = await fileRequest.upload<FileUploadResponse>('medical-images', file as any)
        
        uploadedFile.value = response
        emit('update:modelValue', response)
        previewImageUrl.value = response.url

        fileList.value = [{
          name: file.name,
          status: 'success',
          uid: Date.now(),
          raw: file as any,
          url: response.url
        }]
        
        ElMessage.success('图片上传成功')
        
      } catch (error: any) {
        console.error('图片上传失败:', error)
        ElMessage.error(error.message || '图片上传失败')
      } finally {
        uploading.value = false
      }
    }
  }
  input.click()
}
</script>

<template>
  <div class="image-upload-container">
    <div class="upload-area">
      <ElUpload
        ref="uploadRef"
        v-model:file-list="fileList"
        :auto-upload="false"
        :show-file-list="false"
        :before-upload="beforeUpload"
        :on-change="handleFileChange"
        :disabled="disabled || uploading"
        drag
        class="upload-dragger"
      >
        <div v-if="!hasFile" class="upload-empty">
          <ElIcon class="upload-icon" :class="{ 'uploading': uploading }">
            <Picture />
          </ElIcon>
          <div class="upload-text">
            <p v-if="uploading">正在上传图片...</p>
            <template v-else>
              <p>点击或拖拽图片到此处上传</p>
              <p class="upload-tip">支持 JPG、PNG、GIF、BMP、TIFF 格式，大小不超过 10MB</p>
            </template>
          </div>
        </div>
        
        <div v-else class="upload-preview">
          <ElImage
            :src="previewImageUrl"
            fit="cover"
            class="preview-image"
            :preview-src-list="[previewImageUrl]"
            :initial-index="0"
            hide-on-click-modal
          />
          <div class="preview-overlay">
            <div class="preview-actions">
              <ElButton
                type="info"
                :icon="View"
                circle
                size="small"
                @click.stop="handlePreview"
              />
              <ElButton
                type="danger"
                :icon="Delete"
                circle
                size="small"
                @click.stop="() => handleRemove()"
              />
            </div>
          </div>
        </div>
      </ElUpload>

      <div class="upload-actions">
        <ElButton
          type="primary"
          :icon="Upload"
          @click="triggerUpload"
          :disabled="disabled || uploading"
          :loading="uploading"
          size="small"
        >
          {{ uploading ? '上传中...' : '选择图片' }}
        </ElButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.image-upload-container {
  padding: 16px;
  border: 1px solid #e1f0ff;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  box-shadow: 0 2px 8px rgba(44, 90, 160, 0.1);
}

.upload-area {
  width: 100%;
}

.upload-dragger {
  width: 100%;
}

.upload-dragger :deep(.el-upload-dragger) {
  width: 100%;
  height: 150px;
  border: 2px dashed #c0ccda;
  border-radius: 12px;
  background-color: #fafbfc;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.upload-dragger :deep(.el-upload-dragger:hover) {
  border-color: #2c5aa0;
  background-color: #f0f8ff;
}

.upload-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #5a6c7d;
}

.upload-icon {
  font-size: 48px;
  color: #c0ccda;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.upload-icon.uploading {
  color: #2c5aa0;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.upload-text {
  text-align: center;
}

.upload-text p {
  margin: 4px 0;
}

.upload-tip {
  font-size: 12px;
  color: #999;
}

.upload-preview {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  border-radius: 8px;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 8px;
}

.upload-preview:hover .preview-overlay {
  opacity: 1;
}

.preview-actions {
  display: flex;
  gap: 8px;
}

.upload-actions {
  margin-top: 12px;
  text-align: center;
}

@media (max-width: 768px) {
  .image-upload-container {
    padding: 12px;
  }
  
  .upload-dragger :deep(.el-upload-dragger) {
    height: 120px;
  }
  
  .upload-icon {
    font-size: 36px;
    margin-bottom: 12px;
  }
}
</style> 