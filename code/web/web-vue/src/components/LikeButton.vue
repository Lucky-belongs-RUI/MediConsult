<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { likeApi } from '@/api/like'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const userId = userStore.userInfo?.id
const props = defineProps({
  itemId: {
    type: Number,
    required: true
  },
  initialIsLiked: {
    type: Boolean,
    default: false
  },
  initialLikeCount: {
    type: Number,
    default: 0
  },
  showCount: {
    type: Boolean,
    default: true
  },
  size: {
    type: String as () => '' | 'default' | 'small' | 'large',
    default: 'default'
  }
})

const emit = defineEmits(['update:isLiked', 'update:likeCount', 'like', 'unlike'])

const isLiked = ref(props.initialIsLiked)
const likeCount = ref(props.initialLikeCount)
const loading = ref(false)

const toggleLike = async () => {
  if (loading.value) return

  loading.value = true
  try {
    if (isLiked.value) {
      await likeApi.unlike(props.itemId, userId)
      isLiked.value = false
      likeCount.value = Math.max(0, likeCount.value - 1)
      emit('unlike')
    } else {
      await likeApi.like({ itemId: props.itemId,userId:userId })
      isLiked.value = true
      likeCount.value += 1
      emit('like')
    }
    emit('update:isLiked', isLiked.value)
    emit('update:likeCount', likeCount.value)
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
    console.error('点赞操作失败', error)
  } finally {
    loading.value = false
  }
}

const loadLikeStatus = async () => {
  try {
    const status = await likeApi.status(props.itemId,userId?userId:0)
    isLiked.value = status
    emit('update:isLiked', isLiked.value)
  } catch (error) {
    console.error('获取点赞状态失败', error)
  }
}

const loadLikeCount = async () => {
  try {
    const count = await likeApi.count(props.itemId)
    likeCount.value = count
    emit('update:likeCount', likeCount.value)
  } catch (error) {
    console.error('获取点赞数失败', error)
  }
}

onMounted(() => {
  if (props.initialIsLiked === false) {
    loadLikeStatus()
  }
  if (props.initialLikeCount === 0) {
    loadLikeCount()
  }
})
</script>

<template>
  <div class="like-button">
    <el-button
      :type="isLiked ? 'danger' : 'default'"
      :icon="isLiked ? 'el-icon-star-on' : 'el-icon-star-off'"
      :size="size"
      :loading="loading"
      @click="toggleLike"
    >
      <el-icon v-if="isLiked"><StarFilled /></el-icon>
      <el-icon v-else><Star /></el-icon>
      <span v-if="showCount" class="like-count">{{ likeCount }}</span>
    </el-button>
  </div>
</template>

<style scoped>
.like-button {
  display: inline-flex;
  align-items: center;
}

.like-count {
  margin-left: 4px;
}
</style> 