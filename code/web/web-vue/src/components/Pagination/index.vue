<template>
  <div class="pagination-container">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :layout="'total, sizes, prev, pager, next, jumper'"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  current: {
    type: Number,
    default: 1
  },
  size: {
    type: Number,
    default: 10
  },
  total: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:current', 'update:size', 'change'])

const currentPage = computed({
  get: () => props.current,
  set: (val: number) => emit('update:current', val)
})

const pageSize = computed({
  get: () => props.size,
  set: (val: number) => emit('update:size', val)
})

const handleCurrentChange = (val: number) => {
  emit('change')
}

const handleSizeChange = (val: number) => {
  emit('change')
}
</script>

<style lang="scss" scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 