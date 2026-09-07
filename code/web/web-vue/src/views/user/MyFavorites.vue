<template>
  <div class="my-favorites">
    <div class="favorites-header">
      <h3>我的病例收藏</h3>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="favorites.length === 0" class="empty-container">
      <el-empty description="暂无病例收藏" />
    </div>
    
    <div v-else class="favorites-list">
      <div 
        v-for="favorite in favorites" 
        :key="favorite.id" 
        class="favorite-item"
        :class="{ 'has-cover': favorite.item?.coverUrl }"
      >
        <div class="favorite-content">
          <div class="favorite-cover" @click="navigateToDetail(favorite.itemId)">
            <el-image 
              v-if="favorite.item?.coverUrl" 
              :src="favorite.item.coverUrl" 
              fit="cover"
              class="item-cover"
            />
            <div v-else class="no-image">
              <el-icon><Picture /></el-icon>
            </div>
            <div class="cover-overlay">
              <el-icon class="view-icon"><View /></el-icon>
              <span>查看详情</span>
            </div>
          </div>
          
          <div class="favorite-info">
            <h3 class="item-title">
              <router-link :to="`/item/${favorite.itemId}`">{{ favorite.item?.title }}</router-link>
            </h3>
            
            <p 
              v-if="favorite.item?.description" 
              class="item-description"
              @click="navigateToDetail(favorite.itemId)"
            >
              {{ truncateDescription(favorite.item.description) }}
            </p>
            
            <div class="item-meta">
              <div class="meta-left">
                <el-tag v-if="favorite.item?.category" size="small" type="info">{{ favorite.item.category.name }}</el-tag>
                <span class="favorite-time">收藏于: {{ formatTime(favorite.createTime) }}</span>
              </div>
              
              <div class="meta-right">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="navigateToDetail(favorite.itemId)"
                >
                  <el-icon><View /></el-icon> 查看详情
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="handleRemoveFavorite(favorite.itemId)"
                >
                  <el-icon><Delete /></el-icon> 取消病例收藏
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed,  onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { favoriteApi } from '@/api/favorite'
import type { FavoriteVO } from '@/types/favorite'
import { Picture, View, Delete } from '@element-plus/icons-vue'
import { formatDate } from '@/utils/date'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const favorites = ref<FavoriteVO[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const userStore = useUserStore()
const userId = computed(() => userStore.userInfo?.id)
const fetchFavorites = async () => {
  loading.value = true
  try {
    const res = await favoriteApi.page(userId.value?userId.value:0,currentPage.value, pageSize.value)
    favorites.value = res.records
    total.value = res.total
  } catch (error) {
    console.error('获取病例收藏列表失败', error)
    ElMessage.error('获取病例收藏列表失败')
  } finally {
    loading.value = false
  }
}

const navigateToDetail = (itemId: number) => {
  router.push(`/user/item/${itemId}`)
}

const handleRemoveFavorite = (itemId: number) => {
  ElMessageBox.confirm('确定要取消病例收藏吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await favoriteApi.remove(itemId)
      ElMessage.success('取消病例收藏成功')
      fetchFavorites()
    } catch (error) {
      console.error('取消病例收藏失败', error)
      ElMessage.error('取消病例收藏失败')
    }
  }).catch(() => {})
}

const formatTime = (dateStr: string) => {
  return formatDate(new Date(dateStr), 'YYYY-MM-DD HH:mm')
}

const truncateDescription = (text: string, maxLength: number = 100) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchFavorites()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  fetchFavorites()
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.my-favorites {
  width: 100%;
  padding: 0;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
}

.favorites-header {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  padding: 20px 25px;
  border-bottom: 2px solid #e1f0ff;
}

.favorites-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c5aa0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.favorites-header h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.loading-container, 
.empty-container {
  display: flex;
  justify-content: center;
  padding: 60px 0;
  background: #fff;
  border-radius: 0 0 16px 16px;
}

.favorites-list {
  background: #fff;
  padding: 0 0 20px 0;
  border-radius: 0 0 16px 16px;
}

.favorite-item {
  margin-bottom: 0;
  transition: all 0.3s ease;
  background: #fff;
  padding: 20px 25px;
  border-bottom: 1px solid #e1f0ff;
  position: relative;
}

.favorite-item:hover {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  transform: translateX(4px);
}

.favorite-item:last-child {
  border-bottom: none;
}

.favorite-content {
  display: flex;
  gap: 20px;
}

.favorite-cover {
  position: relative;
  width: 140px;
  height: 100px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(22, 160, 133, 0.15);
  transition: all 0.3s ease;
}

.favorite-cover:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 25px rgba(22, 160, 133, 0.25);
}

.item-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.favorite-cover:hover .item-cover {
  transform: scale(1.08);
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(44, 90, 160, 0.8) 0%, rgba(22, 160, 133, 0.8) 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  backdrop-filter: blur(2px);
}

.favorite-cover:hover .cover-overlay {
  opacity: 1;
}

.view-icon {
  font-size: 1.5rem;
  margin-bottom: 5px;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #16a085;
}

.no-image .el-icon {
  font-size: 2.5rem;
}

.favorite-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-title {
  margin: 0 0 12px;
  font-size: 1.1rem;
  font-weight: 600;
}

.item-title a {
  color: #2c5aa0;
  text-decoration: none;
  transition: color 0.3s ease;
}

.item-title a:hover {
  color: #16a085;
}

.item-description {
  margin: 0 0 15px;
  font-size: 0.9rem;
  color: #5a6c7d;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  cursor: pointer;
  transition: color 0.3s ease;
  line-height: 1.5;
}

.item-description:hover {
  color: #2c5aa0;
}

.item-meta {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.meta-left .el-tag {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #16a085;
  border: 1px solid #16a085;
  border-radius: 15px;
  font-weight: 500;
}

.meta-right {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.meta-right .el-button {
  border-radius: 20px;
  padding: 6px 15px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.meta-right .el-button--primary {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border: none;
}

.meta-right .el-button--primary:hover {
  background: linear-gradient(135deg, #138d75 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(22, 160, 133, 0.3);
}

.meta-right .el-button--danger {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  border: none;
}

.meta-right .el-button--danger:hover {
  background: linear-gradient(135deg, #c53030 0%, #9c2626 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(229, 62, 62, 0.3);
}

.favorite-time {
  font-size: 0.8rem;
  color: #5a6c7d;
  font-weight: 400;
}

.pagination-container {
  margin-top: 25px;
  padding: 0 25px;
  display: flex;
  justify-content: center;
}

.pagination-container :deep(.el-pagination__total),
.pagination-container :deep(.el-pagination__sizes),
.pagination-container :deep(.el-pagination__jump) {
  color: #5a6c7d;
}

.pagination-container :deep(.el-pager li) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  margin: 0 2px;
  border: 1px solid #e1f0ff;
}

.pagination-container :deep(.el-pager li:hover),
.pagination-container :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  color: white;
  border-color: #16a085;
}

.pagination-container :deep(.btn-prev),
.pagination-container :deep(.btn-next) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  border: 1px solid #e1f0ff;
}

.pagination-container :deep(.btn-prev:hover),
.pagination-container :deep(.btn-next:hover) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  color: white;
}

:deep(.el-button) {
  display: flex;
  align-items: center;
  gap: 6px;
}

@media (max-width: 768px) {
  .favorites-header {
    padding: 15px 20px;
  }
  
  .favorite-item {
    padding: 15px 20px;
  }
  
  .favorite-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .favorite-cover {
    width: 100%;
    height: 120px;
  }
  
  .item-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .meta-right {
    width: 100%;
    justify-content: flex-start;
  }
  
  .pagination-container {
    padding: 0 15px;
  }
}
</style> 