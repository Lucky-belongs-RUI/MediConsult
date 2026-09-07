<script setup lang="ts">
import { ref, onMounted, nextTick, watch, onUnmounted } from 'vue'
import { ElMessage, ElButton, ElMessageBox } from 'element-plus'
import { Plus, ArrowLeft, Document, Promotion } from '@element-plus/icons-vue'
import type { ChatMessage, ChatSession } from '@/types/chat'
import { chatApi, llmApi } from '@/api/chat'
import { documentApi } from '@/api/document'
import { vectorIndexApi, knowledgeGraphApi } from '@/api/vector'
import ChatMessageComponent from '@/components/chat/ChatMessage.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import ModelSelector from '@/components/chat/ModelSelector.vue'

const props = defineProps<{
  sessionId?: number | null;
  showBackButton?: boolean;
}>();

const emits = defineEmits<{
  'back': [];
  'create-session': [];
  'clear-messages': [];
  'session-loaded': [session: ChatSession];
}>();

const session = ref<ChatSession | null>(null)
const messages = ref<ChatMessage[]>([])
const loading = ref(false)
const selectedModel = ref('qwen-turbo')
const messagesContainer = ref<HTMLElement | null>(null)

const enableRAG = ref(false)
const enableKnowledgeGraph = ref(false)
const ragStatus = ref({
  indexExists: false,
  loading: false
})
const knowledgeGraphStatus = ref({
  exists: false,
  loading: false
})

const documentLoading = ref(false)

const loadSession = async () => {
  if (!props.sessionId) return;

  try {
    session.value = await chatApi.getSession(props.sessionId)
    emits('session-loaded', session.value)
  } catch (error) {
    ElMessage.error('加载会话信息失败')
    console.error(error)
  }
}

const loadMessages = async () => {
  if (!props.sessionId) return;
  
  try {
    messages.value = await chatApi.getMessages({ sessionId: props.sessionId })
    await nextTick()
    scrollToBottom()
  } catch (error) {
    ElMessage.error('加载消息历史失败')
    console.error(error)
  }
}

const handleSendMessage = async (content: string, imageInfo?: { url: string, bucket: string, objectKey: string }) => {
  if (loading.value || !content.trim() || !props.sessionId) return
  
  let extraData = ''
  if (imageInfo) {
    extraData = JSON.stringify({
      bucket: imageInfo.bucket,
      objectKey: imageInfo.objectKey
    })
  }

  const userMessage: ChatMessage = {
    sessionId: props.sessionId,
    role: 'user',
    content,
    model: selectedModel.value,
    extraData: extraData
  }
  
  messages.value = [...messages.value, userMessage]
  await nextTick()
  scrollToBottom()
  
  const tempMessageIndex = messages.value.length - 1
  
  try {
    loading.value = true
    
    const aiResponse = await chatApi.sendMessage({
      sessionId: props.sessionId,
      content,
      model: selectedModel.value,
      extraData: extraData
    })
    
    const tempMessage: ChatMessage = {
      id: aiResponse.id,
      sessionId: props.sessionId,
      role: 'assistant',
      content: '正在思考...',
      model: selectedModel.value,
      messageTime: aiResponse.messageTime
    }
    
    messages.value = [...messages.value, tempMessage]
    await nextTick()
    scrollToBottom()
    
    try {
      await handleNormalResponse(tempMessage, imageInfo)
      
      document.dispatchEvent(new CustomEvent('refresh-session-list'))
    } catch (responseError) {
      console.error('获取AI响应失败:', responseError)
      const updatedMessage = { ...tempMessage }
      updatedMessage.content = '抱歉，AI响应生成失败，请重试。'
      
      const index = messages.value.findIndex(msg => msg.id === tempMessage.id)
      if (index !== -1) {
        messages.value[index] = updatedMessage
        messages.value = [...messages.value]
      }
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送消息失败')
    messages.value.splice(tempMessageIndex)
    messages.value = [...messages.value]
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}



const handleNormalResponse = async (tempMessage: ChatMessage, imageInfo?: { url: string, bucket: string, objectKey: string }) => {
  try {
    const historyMessages = messages.value.slice(0, messages.value.length - 1)
    
    const ragResponse = await llmApi.chat(
      selectedModel.value,
      historyMessages,
      enableRAG.value,
      enableKnowledgeGraph.value,
      imageInfo
    )
    
    if (enableRAG.value && ragResponse.rewritten_query) {
      console.log('🔍 查询重构:', {
        原始查询: historyMessages[historyMessages.length - 1]?.content,
        重构查询: ragResponse.rewritten_query
      })
    }
    
    const updatedMessage = { ...tempMessage }
    updatedMessage.content = ragResponse.response
    
    if (ragResponse.relevant_cases && ragResponse.relevant_cases.length > 0) {
      (updatedMessage as any).relevantCases = ragResponse.relevant_cases
    }
    
    if (ragResponse.relevant_knowledge && ragResponse.relevant_knowledge.length > 0) {
      (updatedMessage as any).relevantKnowledge = ragResponse.relevant_knowledge
    }
    
    tempMessage.content = ragResponse.response
    if (ragResponse.relevant_cases && ragResponse.relevant_cases.length > 0) {
      (tempMessage as any).relevantCases = ragResponse.relevant_cases
    }
    if (ragResponse.relevant_knowledge && ragResponse.relevant_knowledge.length > 0) {
      (tempMessage as any).relevantKnowledge = ragResponse.relevant_knowledge
    }
    
    const index = messages.value.findIndex(msg => msg.id === tempMessage.id)
    if (index !== -1) {
      messages.value[index] = updatedMessage
      messages.value = [...messages.value]
      
      nextTick(() => {
        scrollToBottom()
      })
    }
    
    await updateAiMessageInDatabase(tempMessage.id!, ragResponse.response)
  } catch (error) {
    console.error('获取LLM响应失败:', error)
    
    const updatedMessage = { ...tempMessage }
    updatedMessage.content = '抱歉，发生了错误，请重试。'
    
    tempMessage.content = updatedMessage.content
    
    const index = messages.value.findIndex(msg => msg.id === tempMessage.id)
    if (index !== -1) {
      messages.value[index] = updatedMessage
      messages.value = [...messages.value]
    }
    
    throw error
  }
}

const updateAiMessageInDatabase = async (messageId: number, content: string) => {
  try {
    if (!messageId) {
      console.error('更新AI消息到数据库失败: 消息ID未定义')
      return
    }
    await chatApi.updateMessageContent(messageId, content)
  } catch (error) {
    console.error('更新AI消息到数据库失败:', error)
  }
}

const goBack = () => {
  emits('back')
}

const createNewSession = () => {
  emits('create-session')
}

const clearMessages = async () => {
  if (!props.sessionId) return
  
  try {
    await ElMessageBox.confirm('确定要清空所有问诊记录吗？此操作不可恢复', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await chatApi.clearSessionMessages(props.sessionId)
    messages.value = []
    ElMessage.success('问诊记录已清空')
    
    emits('clear-messages')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空问诊记录失败')
      console.error(error)
    }
  } finally {
    loading.value = false
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

watch(() => props.sessionId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    await loadSession();
    await loadMessages();
  }
}, { immediate: true });

const handleRefreshSessionDetail = (event: CustomEvent) => {
  const refreshSessionId = event.detail
  if (refreshSessionId === props.sessionId) {
    loadSession()
  }
}

const generateChatDocument = async () => {
  if (!props.sessionId || messages.value.length === 0) {
    ElMessage.warning('当前会话没有对话记录，无法生成文档')
    return
  }
  
  try {
    documentLoading.value = true
    ElMessage.info('正在分析问诊记录并生成文档，请稍候...')
    
    const result = await documentApi.generateChatDocument(props.sessionId)
    
    window.open(result.downloadUrl, '_blank')
    
    ElMessage.success('问诊文档生成成功！正在下载...')
    
    if (result.summary) {
      console.log('📋 问诊总结:', result.summary)
    }
    
  } catch (error) {
    console.error('生成问诊文档失败', error)
    ElMessage.error('生成问诊文档失败，请稍后重试')
  } finally {
    documentLoading.value = false
  }
}

const checkRAGStatus = async () => {
  try {
    ragStatus.value.loading = true
    const status = await vectorIndexApi.getStatus()
    ragStatus.value.indexExists = status.exists
  } catch (error) {
    console.error('检查RAG状态失败:', error)
    ragStatus.value.indexExists = false
  } finally {
    ragStatus.value.loading = false
  }
}

const checkKnowledgeGraphStatus = async () => {
  try {
    knowledgeGraphStatus.value.loading = true
    const status = await knowledgeGraphApi.getStatus()
    knowledgeGraphStatus.value.exists = status.exists
  } catch (error) {
    console.error('检查知识图谱状态失败:', error)
    knowledgeGraphStatus.value.exists = false
  } finally {
    knowledgeGraphStatus.value.loading = false
  }
}

onMounted(async () => {
  if (props.sessionId) {
    await loadSession();
    await loadMessages();
  }
  
  await checkRAGStatus()

  await checkKnowledgeGraphStatus()

  document.addEventListener('refresh-session-detail', handleRefreshSessionDetail as EventListener)
})

onUnmounted(() => {
  document.removeEventListener('refresh-session-detail', handleRefreshSessionDetail as EventListener)
})
</script>

<template>
  <div class="chat-panel chat-session">
    <div class="chat-header">
      <ElButton v-if="showBackButton" link @click="goBack" :icon="ArrowLeft">返回</ElButton>

      <slot name="toggle-button"></slot>
      
      <h2 v-if="session">{{ session.sessionName }}</h2>
      <div v-else class="no-session-title">请选择或创建一个会话</div>
      
      <div class="chat-actions" v-if="sessionId">
        <ElButton type="info" @click="generateChatDocument" :icon="Document" size="small" :loading="documentLoading">
          生成问诊文档
        </ElButton>
        <ElButton type="danger" @click="clearMessages" plain size="small" :loading="loading">清空记录</ElButton>
        <ElButton type="primary" @click="createNewSession" :icon="Plus" circle />
      </div>
    </div>
    
    <div class="model-options" v-if="sessionId">
      <ModelSelector v-model="selectedModel" />

      <div class="rag-controls">
        <div class="rag-switch">
          <ElTooltip
            content="智能诊断功能会基于相关病例为您提供更精准的医疗建议"
            placement="top"
          >
            <ElSwitch
              v-model="enableRAG"
              :disabled="!ragStatus.indexExists || ragStatus.loading"
              active-text="病例检索"
              size="small"
            />
          </ElTooltip>
        </div>

        <div class="rag-switch">
          <ElTooltip
            content="知识图谱功能会基于医学知识库为您提供更专业的医疗建议"
            placement="top"
          >
            <ElSwitch
              v-model="enableKnowledgeGraph"
              :disabled="!knowledgeGraphStatus.exists || knowledgeGraphStatus.loading"
              active-text="知识图谱"
              size="small"
            />
          </ElTooltip>
        </div>
      </div>
    </div>
    
    <div class="messages-container" ref="messagesContainer" v-if="sessionId">
      <template v-if="messages.length">
        <ChatMessageComponent 
          v-for="(message, index) in messages" 
          :key="index" 
          :message="message" 
        />
      </template>
      <div v-else class="empty-message">
        <div class="empty-chat-icon">
          <svg class="medical-chat-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <!-- 医疗聊天气泡 -->
            <circle cx="35" cy="40" r="25" fill="#4f8de6" opacity="0.1"/>
            <circle cx="35" cy="40" r="20" fill="#4f8de6" opacity="0.2"/>
            <circle cx="35" cy="40" r="15" fill="#4f8de6" opacity="0.4"/>
            
            <!-- 聊天气泡主体 -->
            <path d="M20 30 Q20 20 30 20 L50 20 Q60 20 60 30 L60 40 Q60 50 50 50 L35 50 L25 55 L30 50 Q20 50 20 40 Z" 
                  fill="currentColor" opacity="0.8"/>
            
            <!-- 医疗十字 -->
            <rect x="32" y="28" width="6" height="14" fill="white" rx="1"/>
            <rect x="28" y="32" width="14" height="6" fill="white" rx="1"/>
            
            <!-- 第二个气泡 -->
            <circle cx="65" cy="55" r="18" fill="#3a6fdc" opacity="0.3"/>
            <path d="M50 50 Q50 45 55 45 L70 45 Q75 45 75 50 L75 55 Q75 60 70 60 L60 60 L55 63 L58 60 Q50 60 50 55 Z" 
                  fill="#3a6fdc" opacity="0.6"/>
            
            <!-- 心跳线 -->
            <path d="M85 25 L88 25 L90 20 L92 30 L94 15 L96 35 L98 25 L100 25" 
                  stroke="currentColor" stroke-width="2" fill="none" opacity="0.5"/>
          </svg>
        </div>
        <p>开始新的医疗咨询吧！</p>
      </div>
    </div>
    
    <div class="no-session" v-else>
      <div class="welcome-icon">
        <svg class="medical-welcome-icon" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
          <!-- 医院建筑轮廓 -->
          <rect x="30" y="60" width="60" height="50" fill="currentColor" opacity="0.1" rx="4"/>
          
          <!-- 主建筑 -->
          <rect x="35" y="65" width="50" height="40" fill="currentColor" opacity="0.3" rx="2"/>
          
          <!-- 医疗十字标志 -->
          <circle cx="60" cy="45" r="20" fill="currentColor" opacity="0.2"/>
          <circle cx="60" cy="45" r="15" fill="currentColor" opacity="0.4"/>
          <rect x="56" y="35" width="8" height="20" fill="white" rx="2"/>
          <rect x="50" y="41" width="20" height="8" fill="white" rx="2"/>
          
          <!-- 建筑窗户 -->
          <rect x="42" y="72" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          <rect x="52" y="72" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          <rect x="62" y="72" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          <rect x="72" y="72" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          
          <rect x="42" y="82" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          <rect x="52" y="82" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          <rect x="62" y="82" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          <rect x="72" y="82" width="6" height="6" fill="white" opacity="0.8" rx="1"/>
          
          <!-- 入口门 -->
          <rect x="56" y="90" width="8" height="15" fill="white" opacity="0.9" rx="1"/>
          
          <!-- 医疗符号装饰 -->
          <circle cx="15" cy="25" r="4" fill="currentColor" opacity="0.3"/>
          <path d="M13 25 L17 25 M15 23 L15 27" stroke="white" stroke-width="1.5"/>
          
          <circle cx="105" cy="85" r="4" fill="currentColor" opacity="0.3"/>
          <path d="M103 85 L107 85 M105 83 L105 87" stroke="white" stroke-width="1.5"/>
          
          <!-- 脉搏波形 -->
          <path d="M10 100 L15 100 L18 95 L22 105 L25 90 L28 110 L32 100 L35 100" 
                stroke="currentColor" stroke-width="2" fill="none" opacity="0.4"/>
        </svg>
      </div>
      <h3>智慧医疗助手</h3>
      <p>请在左侧选择一个会话或创建新会话开始咨询</p>
      <div class="welcome-features">
        <div class="feature-item">
          <span class="feature-icon">🤖</span>
          <span>AI智能诊断</span>
        </div>
        <div class="feature-item">
          <span class="feature-icon">📊</span>
          <span>病例数据分析</span>
        </div>
        <div class="feature-item">
          <span class="feature-icon">⚡</span>
          <span>24小时在线</span>
        </div>
      </div>
      <ElButton type="primary" @click="createNewSession" class="welcome-btn">
        <Promotion />
        创建新会话
      </ElButton>
    </div>
    
    <div class="input-container" v-if="sessionId">
              <ChatInput 
          @send="handleSendMessage" 
          :loading="loading" 
        />
    </div>
  </div>
</template>

<style scoped>
.chat-panel {
  flex-grow: 1;
  flex-shrink: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #ffffff;
  height: 100%;
  min-width: 0;
}

.chat-header {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e1f0ff;
  gap: 12px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.chat-header h2 {
  margin: 0;
  flex-grow: 1;
  font-size: 1.3rem;
  color: #3a6fdc;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-header h2::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #4f8de6 0%, #3a6fdc 100%);
  border-radius: 2px;
}

.no-session-title {
  color: #5a6c7d;
  font-size: 1.1rem;
}

.model-options {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 6px 20px;
  border-bottom: 1px solid #e1f0ff;
  gap: 16px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.model-options .model-selector {
  flex: 1;
  min-width: 200px;
  max-width: 300px;
}

.model-options :deep(.el-select .el-input__wrapper) {
  border-radius: 10px;
  border: 2px solid #e1f0ff;
  background: #ffffff;
  transition: all 0.3s ease;
}

.model-options :deep(.el-select .el-input__wrapper:hover) {
  border-color: #4f8de6;
}

.model-options :deep(.el-select .el-input__wrapper.is-focus) {
  border-color: #3a6fdc;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.rag-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.rag-switch {
  display: flex;
  align-items: center;
}

.rag-switch :deep(.el-switch__core) {
  background-color: #e1f0ff;
  border-color: #e1f0ff;
}

.rag-switch :deep(.el-switch.is-checked .el-switch__core) {
  background: linear-gradient(135deg, #4f8de6 0%, #3a6fdc 100%);
  border-color: #4f8de6;
}

.rag-status {
  display: flex;
  align-items: center;
}

.rag-status :deep(.el-tag) {
  border-radius: 15px;
  font-weight: 500;
}

.rag-status :deep(.el-tag--success) {
  background: linear-gradient(135deg, #e7f1ff 0%, #d6e7ff 100%);
  color: #4f8de6;
  border-color: #4f8de6;
}

.rag-status :deep(.el-tag--warning) {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #f39c12;
  border-color: #f39c12;
}

.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  word-break: break-word;
  overflow-wrap: break-word;
  scroll-behavior: smooth;
  background-image:
    radial-gradient(circle at 25% 25%, rgba(79, 141, 230, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 75% 75%, rgba(44, 90, 160, 0.03) 0%, transparent 50%);
}

.empty-message {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #5a6c7d;
  gap: 15px;
}

.empty-chat-icon, 
.welcome-icon {
  color: #4f8de6;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #e7f1ff 0%, #d6e7ff 100%);
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #4f8de6;
  box-shadow: 0 8px 24px rgba(79, 141, 230, 0.2);
  position: relative;
  overflow: hidden;
}

.empty-chat-icon::before,
.welcome-icon::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: rotate(45deg);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
  100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
}

.medical-chat-icon, 
.medical-welcome-icon {
  width: 70px;
  height: 70px;
  color: #4f8de6;
  filter: drop-shadow(0 2px 4px rgba(79, 141, 230, 0.3));
}

.start-tips {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  border: 1px solid #e1f0ff;
  backdrop-filter: blur(10px);
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #5a6c7d;
  padding: 4px 0;
}

.welcome-features {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  margin: 20px 0;
  width: 100%;
  max-width: 300px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  border: 1px solid #e1f0ff;
  font-size: 14px;
  color: #5a6c7d;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.feature-item:hover {
  background: rgba(79, 141, 230, 0.1);
  border-color: #4f8de6;
  transform: translateY(-1px);
}

.feature-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.no-session h3 {
  margin: 10px 0;
  color: #3a6fdc;
  font-size: 1.4rem;
  font-weight: 600;
}

.no-session {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #5a6c7d;
  gap: 20px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  text-align: center;
  padding: 40px;
}

.no-session p {
  font-size: 1.1rem;
  color: #5a6c7d;
  margin: 0;
}

.welcome-btn {
  padding: 12px 30px;
  font-weight: 500;
  background: linear-gradient(135deg, #4f8de6 0%, #3a6fdc 100%);
  border: none;
  border-radius: 25px;
  color: white;
  transition: all 0.3s ease;
}

.welcome-btn:hover {
  background: linear-gradient(135deg, #2f5ecf 0%, #2a4fbf 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(79, 141, 230, 0.3);
}

.input-container {
  padding: 14px 20px;
  border-top: 1px solid #e1f0ff;
  background: #ffffff;
  box-shadow: 0 -2px 12px rgba(44, 90, 160, 0.06);
}

.chat-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-actions :deep(.el-button) {
  border-radius: 20px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.chat-actions :deep(.el-button--primary) {
  background: linear-gradient(135deg, #4f8de6 0%, #3a6fdc 100%);
  border: none;
}

.chat-actions :deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #2f5ecf 0%, #2a4fbf 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(79, 141, 230, 0.3);
}

.chat-actions :deep(.el-button--danger) {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  border: none;
}

.chat-actions :deep(.el-button--danger:hover) {
  background: linear-gradient(135deg, #c53030 0%, #9c2626 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(229, 62, 62, 0.3);
}

@media (max-width: 768px) {
  .chat-header {
    padding: 20px;
  }
  
  .messages-container {
    padding: 20px;
  }
  
  .input-container {
    padding: 15px 20px;
  }
  
  .model-options {
    padding: 6px 20px;
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
    justify-content: flex-start;
  }
  
  .model-options .rag-controls {
    justify-content: flex-end;
    width: 100%;
  }
  
  .rag-controls {
    flex-direction: row;
    align-items: center;
    gap: 12px;
  }
  
  .no-session {
    padding: 30px 20px;
  }
  
  .empty-chat-icon, 
  .welcome-icon {
    font-size: 3rem;
    width: 70px;
    height: 70px;
  }
}
</style>