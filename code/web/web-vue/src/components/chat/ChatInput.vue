<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElInput, ElButton, ElIcon, ElMessage, ElImage } from 'element-plus'
import { Promotion, Picture, FolderOpened, Loading, Delete, View } from '@element-plus/icons-vue'
import { fileRequest } from '@/api/file_request'

interface FileUploadResponse {
  url: string
  bucket: string
  objectKey: string
}

defineProps<{
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'send', message: string, imageInfo?: FileUploadResponse): void
}>()

const message = ref('')
const uploadedFile = ref<FileUploadResponse | null>(null)
const uploading = ref(false)

const getImagePreviewUrl = () => {
  if (!uploadedFile.value) return ''
  return fileRequest.getFileUrl(uploadedFile.value.bucket, uploadedFile.value.objectKey)
}

const sendMessage = () => {
  const messageText = message.value.trim()
  if (!messageText) {
    return
  }
  
  emit('send', messageText, uploadedFile.value || undefined)

  message.value = ''
  uploadedFile.value = null
}

const handleKeyDown = (e: Event) => {
  const keyEvent = e as KeyboardEvent
  if (keyEvent.key === 'Enter' && !keyEvent.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const beforeUpload = (file: File): boolean => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

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

const selectImage = () => {
  if (uploading.value) return
  
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.style.display = 'none'
  
  input.onchange = async (e) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]
    
    if (file && beforeUpload(file)) {
      await uploadImage(file)
    }

    document.body.removeChild(input)
  }

  document.body.appendChild(input)
  input.click()
}

const uploadImage = async (file: File) => {
  uploading.value = true

  try {
    ElMessage.info('正在上传图片...')

    const response = await fileRequest.upload<FileUploadResponse>('medical-images', file, true)
    
    uploadedFile.value = response
    ElMessage.success('图片上传成功!')
    
  } catch (error: any) {
    console.error('图片上传失败:', error)
    ElMessage.error(error.message || '图片上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

const removeImage = async () => {
  if (!uploadedFile.value) return

  try {
    await fileRequest.delete(uploadedFile.value.bucket, uploadedFile.value.objectKey)
  } catch (error) {
    console.error('删除文件失败:', error)
  }
  
  uploadedFile.value = null
  ElMessage.success('图片已移除')
}
</script>

<template>
  <div class="chat-input">
    <div class="input-container">
      <div class="main-input-area">
        <div class="text-input-area">
          <ElInput
            v-model="message"
            type="textarea"
            :rows="2"
            placeholder="输入消息，Enter发送，Shift+Enter换行..."
            resize="none"
            @keydown="handleKeyDown"
            :disabled="loading"
            class="message-textarea"
          />

          <div class="input-actions">
            <div class="action-buttons">
              <div v-if="uploadedFile" class="image-preview-mini">
                <ElImage
                  :src="getImagePreviewUrl()"
                  fit="cover"
                  class="mini-thumbnail"
                  :preview-src-list="[getImagePreviewUrl()]"
                  :initial-index="0"
                  :preview-teleported="true"
                  :z-index="3000"
                  loading="lazy"
                >
                  <template #error>
                    <div class="mini-error">
                      <ElIcon><Picture /></ElIcon>
                    </div>
                  </template>
                </ElImage>
                <div class="mini-overlay">
                  <ElButton
                    type="danger"
                    :icon="Delete"
                    size="small"
                    circle
                    @click="removeImage"
                    title="移除图片"
                    class="mini-remove-button"
                  />
                </div>
              </div>

              <ElButton
                :type="uploadedFile ? 'success' : 'default'"
                :icon="uploading ? Loading : Picture"
                circle
                size="small"
                @click="selectImage"
                :disabled="loading || uploading"
                :title="uploading ? '上传中...' : (uploadedFile ? '重新选择图片' : '选择图片')"
                class="image-button"
                :class="{ 'uploading': uploading }"
              />

              <ElButton 
                type="primary" 
                @click="sendMessage" 
                :loading="loading" 
                :disabled="!message.trim()"
                class="send-button"
                size="small"
              >
                <Promotion class="send-icon" />
                {{ uploadedFile ? '发送图片消息' : '发送' }}
              </ElButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  background: white;
  border-radius: 12px;
  border: 1px solid #d6e6ff;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(79, 141, 230, 0.12);
}

.input-container {
  padding: 12px 16px;
}

.main-input-area {
  width: 100%;
}

.image-preview-mini {
  position: relative;
  display: inline-block;
  margin-right: 8px;
}

.mini-thumbnail {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 2px solid #d6e6ff;
  cursor: pointer;
  transition: all 0.3s ease;
  object-fit: cover;
  box-shadow: 0 1px 4px rgba(79, 141, 230, 0.15);
}

.mini-thumbnail:hover {
  border-color: #4f8de6;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(79, 141, 230, 0.25);
}

.mini-overlay {
  position: absolute;
  top: -8px;
  right: -8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-preview-mini:hover .mini-overlay {
  opacity: 1;
}

.mini-remove-button {
  width: 18px;
  height: 18px;
  padding: 0;
  background: rgba(239, 68, 68, 0.9);
  border: 1px solid rgba(239, 68, 68, 1);
  color: white;
  font-size: 10px;
  transform: scale(0.8);
  transition: all 0.3s ease;
}

.mini-remove-button:hover {
  background: rgba(220, 38, 38, 1);
  border-color: rgba(220, 38, 38, 1);
  transform: scale(0.9);
}

.mini-error {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #f5f5f5;
  border: 2px dashed #ccc;
  border-radius: 6px;
  color: #999;
}

.mini-error .el-icon {
  font-size: 14px;
}

.text-input-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.message-textarea {
  margin-bottom: 12px;
  flex: 1;
}

.message-textarea :deep(.el-textarea__inner) {
  border: 1px solid #d6e6ff;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  box-shadow: none;
  transition: border-color 0.3s ease;
}

.message-textarea :deep(.el-textarea__inner:focus) {
  border-color: #4f8de6;
  box-shadow: 0 0 0 2px rgba(79, 141, 230, 0.15);
}

.input-actions {
  display: flex;
  justify-content: flex-end;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.image-button {
  transition: all 0.3s ease;
}

.image-button.uploading {
  color: #4f8de6;
  border-color: #4f8de6;
}

.image-button.uploading .el-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.send-button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  font-weight: 500;
}

.send-icon {
  font-size: 14px;
}

@media (max-width: 768px) {
  .input-container {
    padding: 12px;
  }
  
  .send-button {
    padding: 6px 12px;
    font-size: 14px;
  }
  
  .mini-thumbnail {
    width: 28px;
    height: 28px;
  }
  
  .mini-remove-button {
    width: 16px;
    height: 16px;
    font-size: 8px;
  }
  
  .mini-error {
    width: 28px;
    height: 28px;
  }
  
  .mini-error .el-icon {
    font-size: 12px;
  }
}
</style> 