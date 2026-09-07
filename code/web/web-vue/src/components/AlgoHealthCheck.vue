<template>
  <div class="algo-health-check">
    <el-tooltip
      effect="dark"
      :content="tooltipContent"
      placement="bottom"
    >
      <el-button
        :class="[
          'status-button',
          health.status === 'ok' ? 'status-normal' : 'status-error'
        ]"
        size="small"
        plain
        @click="checkHealth"
      >
        <template #icon>
          <el-icon class="status-icon" :class="{ 'is-spinning': checking }">
            <Monitor v-if="health.status === 'ok'" />
            <Warning v-else />
          </el-icon>
        </template>

        <el-tag
          v-if="health.status"
          size="small"
          :class="health.status === 'ok' ? 'tag-normal' : 'tag-error'"
          class="status-tag"
          effect="plain"
        >
          <template #icon>
            <el-icon><CircleCheck v-if="health.status === 'ok'" /><CircleClose v-else /></el-icon>
          </template>
          {{ health.status === 'ok' ? '正常' : '异常' }}
        </el-tag>
      </el-button>
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Monitor, Warning, CircleCheck, CircleClose } from '@element-plus/icons-vue'
import { checkAlgoHealth } from '@/api/algo_health'
import type { HealthResponse } from '@/api/algo_health'

const health = ref<HealthResponse>({
  status: '',
  service: '',
  version: ''
})

const checking = ref(false)

const tooltipContent = computed(() => {
  if (!health.value.status) return '正在检查服务状态...'
  return health.value.status === 'ok' 
    ? `服务正常运行中 (${health.value.version})`
    : '服务异常，点击重试'
})

const checkHealth = async () => {
  checking.value = true
  try {
    const data = await checkAlgoHealth()
    health.value = data
  } catch (error) {
    console.error('检查算法服务状态失败:', error)
    health.value.status = 'error'
  } finally {
    checking.value = false
  }
}

onMounted(() => {
  checkHealth()
})
</script>

<style scoped>
.algo-health-check {
  display: inline-block;
  padding-right: 30px;
}

.status-button {
  padding: 8px 12px;
  transition: all 0.3s ease;
  border: none;
  
}

.status-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.status-normal {
  background: linear-gradient(145deg, #f0f9eb 0%, #e1f3d8 100%);
  color: #67c23a;

}

.status-normal:hover {
  background: linear-gradient(145deg, #e1f3d8 0%, #d0ecb8 100%);
}

.status-error {
  background: linear-gradient(145deg, #fef0f0 0%, #fde2e2 100%);
  color: #f56c6c;
}

.status-error:hover {
  background: linear-gradient(145deg, #fde2e2 0%, #fbd0d0 100%);
}

.service-name {
  font-weight: 500;
  margin: 0 4px;
}

.status-icon {
  font-size: 16px;
  transition: all 0.3s ease;
  opacity: 0.8;
    padding-left: 10px;
}

.status-icon.is-spinning {
  animation: spin 1s linear infinite;
}

.status-tag {
  margin-left: 8px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: none;
}

.tag-normal {
  background-color: rgba(103, 194, 58, 0.1);
  color: #67c23a;
}

.tag-error {
  background-color: rgba(245, 108, 108, 0.1);
  color: #f56c6c;
}

:deep(.el-button) {
  display: flex;
  align-items: center;
  gap: 4px;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 