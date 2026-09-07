<template>
  <div class="category-list">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>科室浏览</span>
        </div>
      </template>
      
      <div class="category-list-container">
        <div
          v-for="category in categories"
          :key="category.id"
          class="category-row"
          @click="handleCategoryClick(category)"
        >
          <div class="category-thumb">
            <img v-if="category.iconUrl" :src="category.iconUrl" class="category-thumb-img" />
            <div v-else class="no-thumb">
              <el-icon><Picture /></el-icon>
            </div>
          </div>
          <div class="category-body">
            <h3 class="category-name">{{ category.name }}</h3>
            <p class="category-description">{{ category.description }}</p>
          </div>
          <div class="category-row-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <el-skeleton animated :rows="3" :loading="loading" />
      </div>

      <div v-if="!loading && categories.length === 0" class="empty-container">
        <el-empty description="暂无科室数据" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { categoryApi } from '@/api/category'
import type { CategoryVO } from '@/types/item'
import { Picture, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()
const categories = ref<CategoryVO[]>([])
const loading = ref(false)

const fetchCategories = async () => {
  try {
    loading.value = true
    const res = await categoryApi.list()
    categories.value = res || []
  } catch (error) {
    console.error('获取科室列表失败', error)
    ElMessage.error('获取科室列表失败')
  } finally {
    loading.value = false
  }
}

const handleCategoryClick = (category: CategoryVO) => {
  router.push({
    name: 'UserCategoryDetail',
    params: { id: category.id }
  })
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-list {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.box-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  background: white;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c5aa0;
}

.card-header span {
  display: flex;
  align-items: center;
}

.card-header span::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border-radius: 2px;
  margin-right: 10px;
  flex-shrink: 0;
}

.category-list-container {
  display: flex;
  flex-direction: column;
}

.category-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #e8eaed;
  cursor: pointer;
  transition: background 0.2s ease;
}

.category-row:hover {
  background: #f5f8ff;
}

.category-row:last-child {
  border-bottom: none;
}

.category-thumb {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.category-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-thumb {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #bbb;
  font-size: 28px;
}

.category-body {
  flex: 1;
  min-width: 0;
}

.category-name {
  margin: 0 0 6px 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #2c5aa0;
}

.category-description {
  margin: 0;
  font-size: 0.9rem;
  color: #5a6c7d;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category-row-arrow {
  flex-shrink: 0;
  color: #bbb;
  font-size: 16px;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.empty-container {
  padding: 60px 0;
}

@media (max-width: 768px) {
  .category-list {
    padding: 12px;
  }

  .category-row {
    padding: 12px;
    gap: 12px;
  }

  .category-thumb {
    width: 60px;
    height: 60px;
  }

  .category-name {
    font-size: 0.95rem;
  }

  .category-description {
    font-size: 0.8rem;
  }
}
</style> 