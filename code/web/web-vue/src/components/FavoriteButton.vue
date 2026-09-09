<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { favoriteApi } from '@/api/favorite'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  itemId: {
    type: Number,
    required: true
  },
  initialIsFavorite: {
    type: Boolean,
    default: false
  },
  text: {
    type: Boolean,
    default: false
  },
  size: {
    type: String as () => '' | 'default' | 'small' | 'large',
    default: 'default'
  }
})

const userStore = useUserStore()
const userId = userStore.userInfo?.id
const emit = defineEmits(['update:isFavorite', 'favorite', 'unfavorite'])

const isFavorite = ref(props.initialIsFavorite)
const loading = ref(false)

const toggleFavorite = async () => {
  if (loading.value) return

  loading.value = true
  try {
    if (isFavorite.value) {
      await favoriteApi.remove(props.itemId, userId)
      isFavorite.value = false
      emit('unfavorite')
    } else {
      await favoriteApi.add({ itemId: props.itemId,userId: userId} )
      isFavorite.value = true
      emit('favorite')
    }
    emit('update:isFavorite', isFavorite.value)
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
    console.error('收藏操作失败', error)
  } finally {
    loading.value = false
  }
}

const loadFavoriteStatus = async () => {
  try {
    const status = await favoriteApi.status(props.itemId,userId?userId:0)
    isFavorite.value = status
    emit('update:isFavorite', isFavorite.value)
  } catch (error) {
    console.error('获取收藏状态失败', error)
  }
}

onMounted(() => {
  if (props.initialIsFavorite === false) {
    loadFavoriteStatus()
  }
})
</script>

<template>
  <div class="favorite-button">
    <el-button
      :type="isFavorite ? 'warning' : 'default'"
      :size="size"
      :loading="loading"
      :text="text"
      @click="toggleFavorite"
    >
      <el-icon v-if="isFavorite"><StarFilled /></el-icon>
      <el-icon v-else><Star /></el-icon>
      <span class="favorite-text">{{ isFavorite ? '已收藏' : '收藏' }}</span>
    </el-button>
  </div>
</template>

<style scoped>
.favorite-button {
  display: inline-flex;
  align-items: center;
}

.favorite-text {
  margin-left: 4px;
}
</style> 