<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { chatApi } from '@/api/chat'
import type { ChatSession as ChatSessionType } from '@/types/chat'
import type { ConsultInfo } from '@/types/chat'
import SessionList from './SessionList.vue'
import ChatSession from './ChatSession.vue'
import ConsultInfoDialog from '@/components/chat/ConsultInfoDialog.vue'
import { categoryApi } from '@/api/category'
import type { CategoryVO } from '@/types/item'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
const userId = computed(() => userStore.userInfo?.id)
const router = useRouter()
const route = useRoute()

const currentSessionId = ref<number | null>(null)
const currentSession = ref<ChatSessionType | null>(null)
const loading = ref(false)

const showSessionList = ref(window.innerWidth > 768)

const isMobileDevice = ref(window.innerWidth <= 768)

const containerStyle = computed(() => {
  return {
    'chat-container': true,
    'show-sessions': showSessionList.value
  }
})

// 新建问诊弹窗
const showConsultDialog = ref(false)
const categories = ref<CategoryVO[]>([])
/** 当前会话的问诊基础信息 */
const activeConsultInfo = ref<ConsultInfo | null>(null)
/** 各会话对应的问诊基础信息（会话切换时恢复） */
const consultInfoMap = new Map<number, ConsultInfo>()

const loadCategories = async () => {
  try {
    categories.value = await categoryApi.list()
  } catch (error) {
    console.error('获取科室列表失败', error)
  }
}

const handleSelectSession = async (sessionId: number) => {
  if (!sessionId || Number.isNaN(Number(sessionId))) {
    return
  }
  currentSessionId.value = sessionId

  router.replace(`/user/chat?sessionId=${sessionId}`)

  // 优先使用会话内缓存；刷新后缓存丢失时从后端会话记录恢复问诊基础信息
  activeConsultInfo.value = consultInfoMap.get(sessionId) || null
  if (!activeConsultInfo.value) {
    try {
      const session = await chatApi.getSession(sessionId)
      if (session?.extraData) {
        const parsed = JSON.parse(session.extraData)
        activeConsultInfo.value = parsed
        consultInfoMap.set(sessionId, parsed)
      }
    } catch (error) {
      console.error('恢复问诊基础信息失败:', error)
    }
  }

  if (isMobileDevice.value) {
    showSessionList.value = false
  }
}

const handleSessionLoaded = (session: ChatSessionType) => {
  currentSession.value = session
}

const handleCreateSession = async () => {
  if (loading.value) return

  // 先填写问诊基础信息
  showConsultDialog.value = true
}

const onConsultDialogConfirm = async (info: ConsultInfo) => {
  showConsultDialog.value = false

  try {
    loading.value = true

    const timestamp = new Date().toLocaleString('zh-CN', {
      month: 'numeric',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric'
    })
    const sessionName = info.consultName || `新的问诊 (${timestamp})`

    const newSession = await chatApi.createSession({
      userId: userId.value ? userId.value : 0,
      sessionName: sessionName,
      extraData: JSON.stringify(info)
    })

    consultInfoMap.set(newSession.id, { ...info })
    activeConsultInfo.value = { ...info }

    handleSelectSession(newSession.id)

    document.dispatchEvent(new CustomEvent('refresh-session-list'))
  } catch (error) {
    ElMessage.error('创建新问诊失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const onConsultDialogCancel = () => {
  showConsultDialog.value = false
}

const handleDeleteSession = async (session: ChatSessionType) => {
  try {
    loading.value = true
    await chatApi.deleteSession(session.id)
    ElMessage.success('删除成功')

    consultInfoMap.delete(session.id)
    if (activeConsultInfo.value) {
      // 删除的是当前会话时清除基础信息
      if (currentSessionId.value === session.id) {
        activeConsultInfo.value = null
      }
    }

    if (currentSessionId.value === session.id) {
      currentSessionId.value = null
      currentSession.value = null

      await fetchAndSelectNewSession()
    }
  } catch (error) {
    ElMessage.error('删除问诊失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchAndSelectNewSession = async () => {
  try {
    const sessions = await chatApi.getUserSessions(userId.value ? userId.value : 0)

    if (sessions.length > 0) {
      handleSelectSession(sessions[0].id)
    } else {
      router.replace('/user/chat')
    }
  } catch (error) {
    console.error('获取问诊列表失败:', error)
  }
}

const handleBack = () => {
  showSessionList.value = true
}

const toggleSessionList = () => {
  showSessionList.value = !showSessionList.value
}

const handleSessionsLoaded = (sessions: ChatSessionType[]) => {
  if (!currentSessionId.value && sessions.length > 0) {
    handleSelectSession(sessions[0].id)
  }
}

const handleClearMessages = async () => {
  document.dispatchEvent(new CustomEvent('refresh-session-list'))
}

const handleResize = () => {
  isMobileDevice.value = window.innerWidth <= 768
  if (window.innerWidth > 768) {
    showSessionList.value = true
  }
}

onMounted(() => {
  const sessionIdParam = route.query.sessionId

  if (sessionIdParam) {
    const sessionId = Number(sessionIdParam)
    if (!Number.isNaN(sessionId)) {
      handleSelectSession(sessionId)
    }
  }

  loadCategories()

  window.addEventListener('resize', handleResize)

  document.addEventListener('refresh-session-list', () => {
    console.log('收到刷新问诊列表事件')
  })
})
</script>

<template>
  <div :class="containerStyle">
    <SessionList
      v-show="showSessionList"
      :current-session-id="currentSessionId"
      :loading="loading"
      @select-session="handleSelectSession"
      @create-session="handleCreateSession"
      @delete-session="handleDeleteSession"
      @sessions-loaded="handleSessionsLoaded"
    />

    <ChatSession
      :session-id="currentSessionId"
      :show-back-button="isMobileDevice"
      :consult-info="activeConsultInfo"
      :categories="categories"
      @back="handleBack"
      @create-session="handleCreateSession"
      @clear-messages="handleClearMessages"
      @session-loaded="handleSessionLoaded"
    >
      <template #toggle-button>
        <button @click="toggleSessionList" class="toggle-btn">
          {{ showSessionList ? '隐藏会话' : '显示会话' }}
        </button>
      </template>
    </ChatSession>

    <ConsultInfoDialog
      :visible="showConsultDialog"
      :categories="categories"
      @update:visible="showConsultDialog = $event"
      @confirm="onConsultDialogConfirm"
      @cancel="onConsultDialogCancel"
    />
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 72px);
  overflow: hidden;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  width: 100%;
  margin: 0;
  border: none;
}

.toggle-btn {
  display: none;
  padding: 8px 16px;
  background: linear-gradient(135deg, #4f8de6 0%, #6fb2ff 100%);
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  color: white;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(79, 141, 230, 0.25);
}

.toggle-btn:hover {
  background: linear-gradient(135deg, #3a6fdc 0%, #5d9dff 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(79, 141, 230, 0.3);
}

@media (max-width: 768px) {
  .chat-container.show-sessions .chat-session {
    display: none;
  }
  
  .chat-container:not(.show-sessions) .session-list {
    display: none;
  }

  .toggle-btn {
    display: block;
  }
  
  .chat-container {
    margin: 0;
    border-radius: 0;
  }
}
</style>
