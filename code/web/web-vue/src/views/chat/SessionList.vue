<script setup lang="ts">
import { ref,computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElButton, ElPopconfirm, ElInput } from 'element-plus'
import { Plus, Delete, Edit } from '@element-plus/icons-vue'
import { chatApi } from '@/api/chat'
import type { ChatSession } from '@/types/chat'

const props = defineProps<{
  currentSessionId?: number | null;
  loading?: boolean;
}>();

const emits = defineEmits<{
  'select-session': [sessionId: number];
  'create-session': [];
  'delete-session': [session: ChatSession];
  'sessions-loaded': [sessions: ChatSession[]];
}>();

const sessions = ref<ChatSession[]>([])
const localLoading = ref(false)

const isLoading = () => props.loading !== undefined ? props.loading : localLoading.value;

const editingSessionId = ref<number | null>(null)
const editingSessionName = ref('')
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
const userId = computed(() => userStore.userInfo?.id)
const loadSessions = async () => {
  try {
    localLoading.value = true
    sessions.value = await chatApi.getUserSessions(userId.value?userId.value:0)
    emits('sessions-loaded', sessions.value)
  } catch (error) {
    ElMessage.error('加载会话列表失败')
    console.error(error)
  } finally {
    localLoading.value = false
  }
}

const createSession = () => {
  emits('create-session')
}

const selectSession = (session: ChatSession) => {
  emits('select-session', session.id)
}

const deleteSession = (session: ChatSession) => {
  emits('delete-session', session)

  setTimeout(() => {
    loadSessions()
  }, 300)
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString()
}

const startRenameSession = (session: ChatSession, event: Event) => {
  event.stopPropagation()
  editingSessionId.value = session.id
  editingSessionName.value = session.sessionName
}

const cancelRenameSession = () => {
  editingSessionId.value = null
  editingSessionName.value = ''
}

const saveRenameSession = async (session: ChatSession) => {
  if (!editingSessionName.value.trim()) {
    ElMessage.warning('会话名称不能为空')
    return
  }

  try {
    await chatApi.updateSession({
      id: session.id,
      sessionName: editingSessionName.value.trim()
    })

    const index = sessions.value.findIndex(s => s.id === session.id)
    if (index !== -1) {
      sessions.value[index].sessionName = editingSessionName.value.trim()
    }

    cancelRenameSession()
    ElMessage.success('重命名成功')

    await loadSessions()

    document.dispatchEvent(new CustomEvent('refresh-session-detail', { detail: session.id }))
  } catch (error) {
    ElMessage.error('重命名失败')
    console.error(error)
  }
}

const handleRenameKeydown = (session: ChatSession, event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    saveRenameSession(session)
  } else if (event.key === 'Escape') {
    cancelRenameSession()
  }
}

const handleRefreshSessionList = () => {
  loadSessions()
}


onMounted(() => {
  loadSessions()
  document.addEventListener('refresh-session-list', handleRefreshSessionList)
})

onUnmounted(() => {
  document.removeEventListener('refresh-session-list', handleRefreshSessionList)
})
</script>

<template>
  <div class="sessions-panel session-list">
    <div class="sessions-header">
              <h2>我的医疗问诊</h2>
      <ElButton 
        type="primary" 
        :icon="Plus" 
        @click="createSession"
        :loading="isLoading()"
        class="create-btn"
      >
                  新建问诊
      </ElButton>
    </div>
    
    <div class="sessions-list">
      <div v-if="isLoading()" class="loading">
        <div class="loading-spinner"></div>
        加载中...
      </div>
      <div v-else-if="!sessions.length" class="empty">
        <div class="empty-icon">
          <svg class="medical-empty-icon" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
            <circle cx="25" cy="30" r="8" fill="none" stroke="currentColor" stroke-width="3" opacity="0.6"/>
            <path d="M33 30 Q45 30 45 45 Q45 55 35 60" fill="none" stroke="currentColor" stroke-width="3" opacity="0.6"/>
            <circle cx="35" cy="60" r="5" fill="currentColor" opacity="0.8"/>

            <path d="M17 30 Q10 25 10 15 Q10 10 15 10 Q20 10 20 15" fill="none" stroke="currentColor" stroke-width="2.5" opacity="0.7"/>
            <path d="M33 30 Q40 25 40 15 Q40 10 45 10 Q50 10 50 15" fill="none" stroke="currentColor" stroke-width="2.5" opacity="0.7"/>

            <rect x="55" y="20" width="18" height="24" fill="currentColor" opacity="0.2" rx="2"/>
            <rect x="57" y="22" width="14" height="20" fill="white" opacity="0.9" rx="1"/>

            <line x1="59" y1="26" x2="69" y2="26" stroke="currentColor" stroke-width="1" opacity="0.4"/>
            <line x1="59" y1="29" x2="69" y2="29" stroke="currentColor" stroke-width="1" opacity="0.4"/>
            <line x1="59" y1="32" x2="67" y2="32" stroke="currentColor" stroke-width="1" opacity="0.4"/>
            <line x1="59" y1="35" x2="69" y2="35" stroke="currentColor" stroke-width="1" opacity="0.4"/>
            <line x1="59" y1="38" x2="65" y2="38" stroke="currentColor" stroke-width="1" opacity="0.4"/>

            <circle cx="15" cy="60" r="6" fill="currentColor" opacity="0.3"/>
            <rect x="13" y="55" width="4" height="10" fill="white" rx="1"/>
            <rect x="10" y="58" width="10" height="4" fill="white" rx="1"/>

            <path d="M5 70 L10 70 L12 65 L14 75 L16 60 L18 80 L20 70 L25 70"
                  stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.4"/>
          </svg>
        </div>
        <p>暂无医疗咨询记录</p>
        <p class="empty-subtitle">点击"新建问诊"开始您的智能医疗咨询</p>
      </div>
      <div 
        v-else
        v-for="session in sessions" 
        :key="session.id" 
        class="session-item"
        :class="{ 'active': currentSessionId === session.id }"
        @click="selectSession(session)"
      >
        <div class="session-info">
          <div v-if="editingSessionId === session.id" class="session-name-editing" @click.stop>
            <ElInput 
              v-model="editingSessionName" 
              size="small" 
              @keydown.enter="saveRenameSession(session)"
              @keydown.esc="cancelRenameSession()"
              @blur="saveRenameSession(session)"
              ref="sessionNameInput"
              placeholder="输入会话名称"
              autofocus
            />
          </div>
          <div v-else class="session-name">{{ session.sessionName }}</div>
          <div class="session-time">{{ formatDate(session.updateTime) }}</div>
          <div class="session-preview" v-if="session.latestMessage">
            {{ session.latestMessage }}
          </div>
        </div>
        <div class="session-actions" @click.stop>
          <ElButton 
            type="primary" 
            :icon="Edit" 
            circle 
            size="small"
            @click="(e) => startRenameSession(session, e)"
            style="margin-right: 8px;"
            class="action-btn edit-btn"
          />
          <ElPopconfirm
            title="确定删除此会话吗？"
            @confirm="deleteSession(session)"
            confirm-button-text="确定"
            cancel-button-text="取消"
            placement="top"
          >
            <template #reference>
              <ElButton 
                type="danger" 
                :icon="Delete" 
                circle 
                size="small"
                class="action-btn delete-btn"
              />
            </template>
          </ElPopconfirm>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sessions-panel {
  width: 300px;
  min-width: 300px;
  border-right: 1px solid #dce7fb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #fff;
  height: 100vh;
}

.sessions-header {
  padding: 14px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dce7fb;
  background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
}

.sessions-header h2 {
  margin: 0;
  font-size: 18px;
  color: #1f3b60;
  font-weight: 600;
}

.create-btn {
  font-weight: 600;
  border: none;
  background: linear-gradient(135deg, #4f8de6 0%, #6fb2ff 100%);
  color: #fff;
  border-radius: 24px;
  box-shadow: 0 6px 18px rgba(79, 141, 230, 0.25);
}

.create-btn:hover {
  background: linear-gradient(135deg, #3a6fdc 0%, #5d9dff 100%);
  transform: translateY(-1px);
}

.sessions-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  border: 1px solid #dce7fb;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #fff;
}

.session-item:hover {
  background-color: #f5faff;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(79, 141, 230, 0.12);
}

.session-item.active {
  background-color: #edf4ff;
  border-color: #a5c0ff;
  box-shadow: 0 4px 16px rgba(79, 141, 230, 0.18);
}

.session-info {
  flex: 1;
  overflow: hidden;
}

.session-name {
  font-weight: bold;
  margin-bottom: 4px;
  color: #1f3b60;
  font-size: 15px;
}

.session-time {
  font-size: 12px;
  color: #8c8c8c;
  margin-bottom: 6px;
}

.session-preview {
  font-size: 13px;
  color: #595959;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.session-actions {
  margin-left: 10px;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.session-item:hover .session-actions {
  opacity: 1;
}

.action-btn {
  transition: transform 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.1);
}

.loading, .empty {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px 20px;
  color: #5a6c7d;
  gap: 15px;
  height: 100%;
}

.empty p {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #3a6fdc;
}

.empty-subtitle {
  font-size: 14px !important;
  color: #8c8c8c !important;
  font-weight: 400 !important;
  line-height: 1.4;
}

.empty-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e7f1ff 0%, #d6e7ff 100%);
  border-radius: 50%;
  border: 3px solid #4f8de6;
  box-shadow: 0 6px 20px rgba(79, 141, 230, 0.2);
  position: relative;
  overflow: hidden;
}

.empty-icon::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transform: rotate(45deg);
  animation: shimmerIcon 4s infinite;
}

@keyframes shimmerIcon {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
  100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
}

.medical-empty-icon {
  width: 50px;
  height: 50px;
  color: #4f8de6;
  filter: drop-shadow(0 2px 4px rgba(79, 141, 230, 0.3));
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 48px;
  color: #d9d9d9;
  margin-bottom: 12px;
}

.session-name-editing {
  margin-bottom: 8px;
  width: 100%;
}

.session-name-editing :deep(.el-input__inner) {
  height: 32px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #91d5ff;
  background-color: #fff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  transition: all 0.3s;
}

@media (max-width: 768px) {
  .sessions-panel {
    width: 100%;
  }
  
.sessions-header {
    padding: 16px;
  }
}
</style> 
