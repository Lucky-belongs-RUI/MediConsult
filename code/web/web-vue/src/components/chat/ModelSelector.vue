<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElSelect, ElOption } from 'element-plus'
import type { ChatModel } from '@/types/chat'
import { llmApi } from '@/api/chat'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const localModelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const models = ref<ChatModel[]>([])
const loading = ref(false)

const loadModels = async () => {
  try {
    loading.value = true
    models.value = await llmApi.getModels()
  } catch (error) {
    console.error('加载模型列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadModels()
})
</script>

<template>
  <div class="model-selector">
    <ElSelect 
      v-model="localModelValue" 
      placeholder="选择模型" 
      :loading="loading"
      size="small"
      style="width: 180px"
    >
      <ElOption
        v-for="model in models"
        :key="model.key"
        :label="model.name"
        :value="model.key"
      />
    </ElSelect>
  </div>
</template>

<style scoped>
.model-selector {
  margin-bottom: 8px;
  min-width: 180px;
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-select-dropdown__item) {
  padding-right: 20px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 