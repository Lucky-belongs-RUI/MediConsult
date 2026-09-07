<script setup lang="ts">
import { computed } from 'vue'
import type { ChatMessage } from '@/types/chat'
import MarkdownIt from 'markdown-it'
import { UserFilled, Picture, View } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import RelevantCases from './RelevantCases.vue'
import { ElIcon, ElTag, ElImage } from 'element-plus'
import { fileRequest } from '@/api/file_request'

const md = new MarkdownIt({
  html: false,
  breaks: true,
  linkify: true
})

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)

const props = defineProps<{
  message: ChatMessage & {
    relevantCases?: Array<{
      id: number
      title: string
      description: string
      categoryName: string
      extraData?: Record<string, any>
    }>
  }
}>()

const messageClass = computed(() => {
  return {
    'message': true,
    'message-user': props.message.role === 'user',
    'message-assistant': props.message.role === 'assistant'
  }
})

const formattedTime = computed(() => {
  if (!props.message.messageTime) return ''
  
  const date = new Date(props.message.messageTime)
  return date.toLocaleString()
})

const renderedContent = computed(() => {
  if (!props.message.content || props.message.content.trim().length === 0) {
    return ''
  }
  return md.render(props.message.content)
})

const extraData = computed(() => {
  if (!props.message.extraData) return null
  try {
    return JSON.parse(props.message.extraData)
  } catch {
    return null
  }
})

const hasImage = computed(() => {
  return extraData.value?.bucket && extraData.value?.objectKey
})

const hasImageOld = computed(() => {
  return extraData.value?.hasImage === true
})

const imageUrl = computed(() => {
  if (!hasImage.value) return null
  const bucket = extraData.value.bucket
  const objectKey = extraData.value.objectKey
  return fileRequest.getFileUrl(bucket, objectKey)
})

const fileInfo = computed(() => {
  if (!extraData.value) return null
  return {
    fileName: extraData.value.fileName || '图片文件',
    fileSize: extraData.value.fileSize || 0,
    type: extraData.value.type || 'image'
  }
})

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<template>
  <div :class="messageClass">
    <div class="avatar-container">
      <div class="avatar" :class="message.role === 'user' ? 'avatar-user' : 'avatar-ai'">
        <img v-if="message.role === 'assistant'" src="@/assets/images/logo.png" alt="AI" class="avatar-img" />
        <img v-else-if="userInfo?.avatarUrl" :src="userInfo.avatarUrl" alt="用户" class="avatar-img" />
        <UserFilled v-else />
      </div>
    </div>
    <div class="message-wrapper">
      <div class="message-header">
        <div class="message-role">{{ message.role === 'user' ? '我' : 'AI助手' }}</div>
        <div v-if="message.role === 'assistant'" class="message-time">{{ formattedTime }}</div>
      </div>

      <div v-if="hasImage && message.role === 'user'" class="image-container">
        <div class="image-header">
          <ElTag type="primary" size="small" class="image-tag">
            <ElIcon><Picture /></ElIcon>
            <span>图片消息</span>
          </ElTag>
        </div>
        <div class="image-preview">
          <div class="image-wrapper">
            <ElImage
              :src="imageUrl || ''"
              fit="cover"
              class="message-image"
              :preview-src-list="imageUrl ? [imageUrl] : []"
              :initial-index="0"
              :preview-teleported="true"
              :z-index="3000"
              loading="lazy"
              preview-title="点击图片可全屏预览"
            >
              <template #error>
                <div class="image-error">
                  <ElIcon><Picture /></ElIcon>
                  <p>图片加载失败</p>
                </div>
              </template>
            </ElImage>
            <div class="preview-hint">
              <ElIcon class="preview-icon"><View /></ElIcon>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="hasImageOld && message.role === 'user'" class="image-indicator">
        <ElTag type="primary" size="small" class="image-tag">
          <ElIcon><Picture /></ElIcon>
          <span>包含图片</span>
        </ElTag>
        <div v-if="fileInfo" class="file-info">
          {{ fileInfo.fileName }} ({{ formatFileSize(fileInfo.fileSize) }})
        </div>
      </div>

      <div v-if="extraData?.type === 'image_analysis' && message.role === 'assistant'" class="analysis-indicator">
        <ElTag type="success" size="small" class="analysis-tag">
          <ElIcon><Picture /></ElIcon>
          <span>图片分析结果</span>
        </ElTag>
        <div v-if="extraData.analysis_model" class="model-info">
          模型：{{ extraData.analysis_model }}
        </div>
      </div>
      
      <div class="message-content">
        <div v-if="message.content && message.content.trim().length > 0" v-html="renderedContent"></div>
        <p v-else class="empty-content">{{ message.role === 'assistant' ? '等待AI响应...' : '空白消息' }}</p>

        <RelevantCases 
          v-if="message.role === 'assistant' && message.relevantCases && message.relevantCases.length > 0"
          :cases="message.relevantCases"
          :default-collapsed="true"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.message {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-user {
  flex-direction: row-reverse;
}

.avatar-container {
  flex-shrink: 0;
}

.avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 15px;
  color: #fff;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-user {
  background-color: #4f8de6;
  box-shadow: 0 2px 10px rgba(79, 141, 230, 0.25);
}

.avatar-ai {
  background-color: #3a6fdc;
  box-shadow: 0 2px 10px rgba(58, 111, 220, 0.25);
}

.message-wrapper {
  padding: 12px 16px;
  border-radius: 16px;
  box-sizing: border-box;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
}

.message-user .message-wrapper {
  max-width: 80%;
  margin-left: auto;
  background-color: #edf4ff;
  border: 1px solid #a5c0ff;
  border-top-right-radius: 4px;
}

.message-assistant .message-wrapper {
  max-width: 80%;
  background-color: #fff;
  border: 1px solid #f0f0f0;
  border-top-left-radius: 4px;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 12px;
}

.message-user .message-header {
  justify-content: flex-start;
}

.message-role {
  font-weight: bold;
  color: #1f3b60;
}

.message-time {
  color: #999;
  font-size: 11px;
}

.message-content {
  word-break: break-word;
  overflow-wrap: break-word;
  line-height: 1.5;
  max-width: 100%;
  font-size: 14px;
  color: #1f3b60;
}

.message-content :deep(pre) {
  background-color: #f7f9fb;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  white-space: pre-wrap;
  max-width: 100%;
  margin: 8px 0;
  border: 1px solid #e8eaed;
}

.message-content :deep(code) {
  background-color: #f0f2f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  word-break: break-all;
  font-size: 13px;
  color: #476582;
}

.message-content :deep(blockquote) {
  border-left: 4px solid #dfe2e5;
  padding: 0 12px;
  margin: 12px 0;
  color: #666;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 0 4px 4px 0;
}

.image-container {
  margin-bottom: 12px;
  border: 1px solid #e1f0ff;
  border-radius: 12px;
  overflow: hidden;
  background: #fafbfc;
}

.image-header {
  padding: 8px 12px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  border-bottom: 1px solid #e1f0ff;
}

.image-preview {
  padding: 12px;
  display: flex;
  justify-content: center;
}

.image-wrapper {
  position: relative;
  display: inline-block;
}

.message-image {
  max-width: 300px;
  max-height: 200px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(44, 90, 160, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.message-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 16px rgba(44, 90, 160, 0.2);
}

.preview-hint {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

.image-wrapper:hover .preview-hint {
  opacity: 1;
}

.preview-icon {
  font-size: 14px;
}

.message-image:hover::before {
  content: "点击查看大图";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 10;
  pointer-events: none;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 120px;
  background: #f5f5f5;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  color: #999;
}

.image-error p {
  margin: 8px 0 0 0;
  font-size: 12px;
}

.image-indicator,
.analysis-indicator {
  margin-bottom: 8px;
  padding: 8px;
  background: rgba(44, 90, 160, 0.05);
  border-radius: 8px;
  border: 1px solid #e1f0ff;
}

.image-tag,
.analysis-tag {
  margin-bottom: 4px;
}

.image-tag :deep(.el-icon) {
  margin-right: 4px;
}

.analysis-tag :deep(.el-icon) {
  margin-right: 4px;
}

.file-info,
.model-info {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
}

.message-content :deep(img) {
  max-width: 100%;
  border-radius: 4px;
  margin: 8px 0;
}

.message-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  border-radius: 4px;
  overflow: hidden;
}

.message-content :deep(th), .message-content :deep(td) {
  border: 1px solid #e8eaed;
  padding: 8px;
  text-align: left;
}

.message-content :deep(th) {
  background-color: #f7f9fb;
}

.message-content :deep(tr:nth-child(2n)) {
  background-color: #f9fafb;
}

.message-content :deep(ul), .message-content :deep(ol) {
  padding-left: 20px;
  margin: 10px 0;
}

.message-content :deep(li) {
  margin-bottom: 5px;
}

.empty-content {
  color: #999;
  font-style: italic;
  margin: 0;
}

@media (max-width: 768px) {
  .message-image {
    max-width: 220px;
    max-height: 140px;
  }

  .image-preview {
    padding: 8px;
  }

  .image-header {
    padding: 6px 10px;
  }

  .image-error {
    width: 150px;
    height: 100px;
  }

  .preview-hint {
    width: 20px;
    height: 20px;
    top: 6px;
    right: 6px;
    opacity: 0.8;
  }

  .preview-icon {
    font-size: 12px;
  }
}

:global(.el-image-viewer__mask) {
  background-color: rgba(0, 0, 0, 0.8) !important;
}

:global(.el-image-viewer__canvas) {
  background-color: transparent !important;
}

:global(.el-image-viewer__btn) {
  background-color: rgba(255, 255, 255, 0.8) !important;
  color: #333 !important;
  border-radius: 6px !important;
  transition: all 0.3s ease !important;
}

:global(.el-image-viewer__btn:hover) {
  background-color: rgba(255, 255, 255, 0.9) !important;
  transform: scale(1.1) !important;
}

:global(.el-image-viewer__close) {
  top: 40px !important;
  right: 40px !important;
  font-size: 24px !important;
}

:global(.el-image-viewer__actions) {
  background-color: rgba(0, 0, 0, 0.5) !important;
  border-radius: 8px !important;
  padding: 8px 16px !important;
}
</style> 