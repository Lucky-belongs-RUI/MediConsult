<template>
  <div class="category-detail">
    <el-card v-if="category" class="main-card">
      <template #header>
        <div class="card-header">
          <span class="category-title">{{ category.name }}</span>
          <el-button @click="goBack" text>
            <el-icon class="mr-1"><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
      </template>
      
      <div class="category-header">
        <div class="category-icon-container">
          <img v-if="category.iconUrl" :src="category.iconUrl" class="category-icon" />
          <div v-else class="no-image-placeholder">
            <el-icon><Picture /></el-icon>
            <span>暂无封面</span>
          </div>
        </div>
        <div class="category-info">
          <p class="category-description">{{ category.description }}</p>
          <div class="category-meta-container">
            <p class="category-meta"><el-icon><Key /></el-icon> 科室ID：{{ category.id }}</p>
            <p class="category-meta"><el-icon><Calendar /></el-icon> 创建时间：{{ formatDate(category.createTime) }}</p>
            <p class="category-meta"><el-icon><Timer /></el-icon> 更新时间：{{ formatDate(category.updateTime) }}</p>
          </div>
        </div>
      </div>

      <el-divider>
        <span class="divider-content">病例列表</span>
      </el-divider>

      <el-row :gutter="16">
        <el-col v-for="item in items" 
                :key="item.id"
                :xs="24" :sm="12" :md="12" :lg="6" :xl="6"
                :class="{ 'mb-20': true }">
          <el-card shadow="hover" @click="handleItemClick(item)" class="item-card">
            <div class="item-img-container">
              <img v-if="item.coverUrl" :src="item.coverUrl" class="item-image" />
              <div v-else class="no-image-placeholder">
                <el-icon><Picture /></el-icon>
                <span>暂无封面</span>
              </div>
            </div>
            <h3 class="item-title">{{ item.title }}</h3>
            <div class="item-description">{{ item.description }}</div>
            <div class="item-tags">
              <el-tag 
                v-for="tag in getTagsArray(item.tags)" 
                :key="tag" 
                size="small" 
                effect="light"
                type="success" 
                class="tag" 
                round
              >
                {{ tag }}
              </el-tag>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <div v-if="loading" class="loading-container">
        <el-skeleton animated :rows="3" :loading="loading" />
      </div>

      <div v-if="!loading && items.length === 0" class="empty-container">
        <el-empty description="该科室下暂无病例" />
      </div>
    </el-card>

    <div v-if="!category && !loading" class="error-container">
      <el-result 
        icon="error" 
        title="未找到"
        sub-title="未找到该科室信息">
        <template #extra>
          <el-button type="primary" @click="goBack">返回</el-button>
        </template>
      </el-result>
    </div>

    <div v-if="loading && !category" class="loading-container">
      <el-skeleton animated :rows="3" :loading="loading" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { categoryApi } from '@/api/category'
import { itemApi } from '@/api/item'
import type { CategoryVO, ItemVO } from '@/types/item'
import { Picture, ArrowLeft, Calendar, Timer, Key } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const category = ref<CategoryVO | null>(null)
const items = ref<ItemVO[]>([])
const loading = ref(false)

const fetchCategoryDetail = async (id: number) => {
  if (!id) {
    ElMessage.error('科室ID无效')
    return
  }

  try {
    loading.value = true
    const res = await categoryApi.getById(id)
    category.value = res || null
  } catch (error) {
    console.error('获取科室详情失败', error)
    ElMessage.error('获取科室详情失败')
    category.value = null
  } finally {
    loading.value = false
  }
}

const fetchCategoryItems = async (id: number) => {
  if (!id) return

  try {
    loading.value = true
    const res = await itemApi.listByCategoryId(id)
    items.value = res || []
  } catch (error) {
    console.error('获取病例列表失败', error)
    ElMessage.error('获取病例列表失败')
  } finally {
    loading.value = false
  }
}

watchEffect(() => {
  const categoryId = Number(route.params.id)
  if (categoryId) {
    fetchCategoryDetail(categoryId)
    fetchCategoryItems(categoryId)
  }
})

const handleItemClick = (item: ItemVO) => {
  router.push({
    name: 'UserItemDetail',
    params: { id: item.id }
  })
}

const goBack = () => {
  router.back()
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
}

const getTagsArray = (tags: string | string[] | undefined | null): string[] => {
  if (!tags) return []

  if (Array.isArray(tags)) return tags.filter(Boolean)

  return tags.split(',').map(tag => tag.trim()).filter(Boolean)
}
</script>

<style scoped>
.category-detail {
  max-width: 1400px;
  margin: 0 auto;
  padding: 15px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.el-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  overflow: hidden;
  transition: all 0.3s ease;
}

.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.12);
}

.category-header {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-bottom: 20px;
}

.category-icon-container {
  width: 120px;
  height: 120px;
  margin-right: 24px;
  flex-shrink: 0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(22, 160, 133, 0.2);
  border: 3px solid #16a085;
}

.category-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 13px;
  transition: transform 0.3s ease;
}

.category-icon:hover {
  transform: scale(1.08);
}

.category-info {
  flex: 1;
  text-align: center;
}

.category-title {
  font-size: 2rem;
  font-weight: 600;
  color: #2c5aa0;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.category-title::before {
  content: '';
  width: 4px;
  height: 40px;
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.category-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #5a6c7d;
  padding: 20px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-radius: 12px;
  border-left: 4px solid #16a085;
  border: 1px solid #e1f0ff;
}

.category-meta-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-meta {
  color: #5a6c7d;
  font-size: 1rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.category-meta .el-icon {
  margin-right: 8px;
  color: #16a085;
  font-size: 1.2rem;
}

.divider-content {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c5aa0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.divider-content::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.mb-20 {
  margin-bottom: 25px;
}

.mr-1 {
  margin-right: 4px;
}

.item-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  overflow: hidden;
}

.item-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 45px rgba(44, 90, 160, 0.15);
}

.item-img-container {
  overflow: hidden;
  border-radius: 0;
  flex: none;
}

.item-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.item-card:hover .item-image {
  transform: scale(1.08);
}

.el-card__body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.item-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #2c5aa0;
}

.item-description {
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #5a6c7d;
  margin-top: 8px;
  margin-bottom: 8px;
  line-height: 1.4;
}

.item-tags {
  display: flex;
  flex-wrap: wrap;
  margin-top: auto;
  padding-top: 12px;
}

.tag {
  margin-right: 8px;
  margin-bottom: 8px;
  border-radius: 15px;
  font-weight: 500;
}

.tag.el-tag--success {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #16a085;
  border-color: #16a085;
}

.tag.el-tag--warning {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #f39c12;
  border-color: #f39c12;
}

.tag.el-tag--danger {
  background: linear-gradient(135deg, #fde8e8 0%, #fad2d2 100%);
  color: #e53e3e;
  border-color: #e53e3e;
}

.tag.el-tag--info {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #16a085;
  border-color: #16a085;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.empty-container {
  padding: 60px 0;
  text-align: center;
}

.empty-container .el-empty {
  color: #5a6c7d;
}

.error-container {
  padding: 60px 0;
  text-align: center;
  color: #e53e3e;
}

.no-image-placeholder {
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #999999;
  border-radius: 0;
  font-size: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.no-image-placeholder .el-icon {
  font-size: 2.5rem;
  margin-bottom: 8px;
  color: #999999;
}

:deep(.el-card__header) {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-bottom: 2px solid #e1f0ff;
  padding: 20px 25px;
}

:deep(.el-divider__text) {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  padding: 0 20px;
}

:deep(.el-divider) {
  border-top: 2px solid #e1f0ff;
}

:deep(.el-col) {
  margin-bottom: 20px;
}

@media (min-width: 768px) {
  .category-detail {
    padding: 20px;
  }

  .category-header {
    flex-direction: row;
    text-align: left;
  }
  
  .category-icon-container {
    width: 140px;
    height: 140px;
    margin-bottom: 0;
  }
  
  .category-info {
    text-align: left;
  }
  
  .category-title {
    justify-content: flex-start;
  }
  
  .category-meta {
    justify-content: flex-start;
  }
  
  .item-image {
    height: 220px;
  }
  
  .category-meta-container {
    flex-direction: row;
    gap: 30px;
  }
}

@media (min-width: 992px) {
  .category-icon-container {
    width: 160px;
    height: 160px;
  }
  
  .category-title {
    font-size: 2.2rem;
  }
}
</style> 