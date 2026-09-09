<template>
  <div class="user-home">
    <div class="banner-section">
      <el-carousel 
        :interval="4000" 
        height="300px" 
        indicator-position="outside"
        :autoplay="true"
        trigger="click"
      >
        <el-carousel-item v-for="(banner, index) in banners" :key="index">
          <div class="banner-item" @click="handleBannerClick(banner)">
            <el-image 
              :src="banner.imageUrl" 
              fit="cover" 
              class="banner-image"
              :preview-src-list="banners.map(item => item.imageUrl)"
              :initial-index="index"
              loading="lazy"
            >
              <template #loading>
                <div class="image-loading">
                  <el-icon class="loading-icon"><Loading /></el-icon>
                </div>
              </template>
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <div class="placeholder-text">图片加载失败</div>
                </div>
              </template>
            </el-image>
            <div class="banner-title">{{ banner.title }}</div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="home-content">
      <div class="main-section">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">常见病例</h2>
            <router-link to="/user/items" class="more-link">
              更多
              <el-icon><ArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="item-grid">
            <div 
              v-for="item in recommendedItems" 
              :key="item.id" 
              class="item-card"
              @click="goToItemDetail(item.id)"
            >
              <div class="item-cover">
                <el-image 
                  :src="item.coverUrl || defaultCover" 
                  fit="cover" 
                  class="cover-image"
                  loading="lazy"
                >
                  <template #error>
                    <div class="image-placeholder">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
                <div class="item-stats">
                  <span class="stat">
                    <el-icon><View /></el-icon> {{ formatNumber(item.views || 0) }}
                  </span>
                  <span class="stat">
                    <el-icon><Star /></el-icon> {{ formatNumber(item.favorites || 0) }}
                  </span>
                </div>
              </div>
              <div class="item-info">
                <div class="item-title">{{ item.title }}</div>
                <div class="item-meta">
                  <span class="uploader">{{ item.userRealName || '未知医生' }}</span>
                </div>
              </div>
            </div>
          </div>

          <el-empty 
            v-if="recommendedItems.length === 0 && !loading" 
            description="暂无常见病例" 
          />
          <div v-if="loading" class="loading-container">
            <el-skeleton :rows="3" animated />
          </div>
        </div>

        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">典型病例</h2>
            <router-link to="/user/items?sort=popular" class="more-link">
              更多
              <el-icon><ArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="item-grid">
            <div 
              v-for="item in popularItems" 
              :key="item.id" 
              class="item-card"
              @click="goToItemDetail(item.id)"
            >
              <div class="item-cover">
                <el-image 
                  :src="item.coverUrl || defaultCover" 
                  fit="cover" 
                  class="cover-image"
                  loading="lazy"
                >
                  <template #error>
                    <div class="image-placeholder">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
                <div class="item-stats">
                  <span class="stat">
                    <el-icon><View /></el-icon> {{ formatNumber(item.views || 0) }}
                  </span>
                  <span class="stat">
                    <el-icon><Star /></el-icon> {{ formatNumber(item.favorites || 0) }}
                  </span>
                </div>
              </div>
              <div class="item-info">
                <div class="item-title">{{ item.title }}</div>
                <div class="item-meta">
                  <span class="uploader">{{ item.userRealName || '未知医生' }}</span>
                </div>
              </div>
            </div>
          </div>

          <el-empty 
            v-if="popularItems.length === 0 && !loading" 
            description="暂无典型病例" 
          />
          <div v-if="loading" class="loading-container">
            <el-skeleton :rows="3" animated />
          </div>
        </div>
      </div>

      <div class="sidebar-section">
        <div class="user-card">
          <div class="user-profile">
            <el-avatar :size="50" :src="userInfo?.avatarUrl || defaultAvatar">
              {{ userInfo?.username?.substring(0, 1) }}
            </el-avatar>
            <div class="user-details">
              <div class="username">{{ userInfo?.realName || userInfo?.username || '游客' }}</div>
              <div class="user-role">{{ userInfo?.role === 1 ? '管理员' : '患者' }}</div>
            </div>
          </div>
          <div class="user-stats">
            <div class="stat-item">
              <div class="stat-value">{{ userStats.favorites || 0 }}</div>
              <div class="stat-label">病例收藏</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ userStats.history || 0 }}</div>
              <div class="stat-label">查看历史</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ userStats.purchases || 0 }}</div>
              <div class="stat-label">咨询病例</div>
            </div>
          </div>
        </div>

        <div class="sidebar-card">
          <div class="card-header">
            <h3>热门科室</h3>
            <router-link to="/user/categories" class="more-link">
              更多
              <el-icon><ArrowRight /></el-icon>
            </router-link>
          </div>
          <div class="category-list">
            <div 
              v-for="category in popularCategories" 
              :key="category.id" 
              class="category-item"
              @click="goToCategoryDetail(category.id)"
            >
              <div class="category-icon">
                <el-image 
                  v-if="category.iconUrl" 
                  :src="category.iconUrl" 
                  fit="cover"
                  loading="lazy"
                />
                <el-icon v-else><Grid /></el-icon>
              </div>
              <div class="category-name">{{ category.name }}</div>
            </div>
          </div>
          <el-empty 
            v-if="popularCategories.length === 0 && !loading" 
            description="暂无科室" 
            :image-size="60"
          />
        </div>

        <div class="chat-card">
          <div class="chat-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="chat-info">
            <div class="chat-title">AI 医疗助手</div>
            <div class="chat-desc">有医疗问题，随时向AI医生咨询</div>
          </div>
          <el-button 
            type="primary" 
            size="small" 
            @click="goToChat"
            class="chat-button"
            round
          >
            开始问诊
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ArrowRight, Picture, View, Star, Grid, ChatDotRound, Loading } from '@element-plus/icons-vue'
import { itemApi } from '@/api/item'
import { categoryApi } from '@/api/category'
import { favoriteApi } from '@/api/favorite'
import { pageMyActions } from '@/api/userAction'

const defaultAvatar = 'https://img0.baidu.com/it/u=520343531,2599065610&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500'
const defaultCover = 'https://image.benlailife.com/Content/images/ErrorNoPic/big.jpg'

const router = useRouter()
const userStore = useUserStore()
const userId = userStore.userInfo?.id
const loading = ref(true)
const userInfo = computed(() => userStore.userInfo)

const userStats = ref({
  favorites: 0,
  history: 0,
  purchases: 0
})

const banners = ref([
  {
    id: 1,
    title: 'AI医生系统正式上线',
    imageUrl: 'https://bpic.51yuansu.com/backgd/cover/00/42/44/5bee946c11f00.jpg?x-oss-process=image/resize,h_360,m_lfit/sharpen,100',
    link: '/user/items'
  },
  {
    id: 2,
    title: '典型医疗案例',
    imageUrl: 'https://copyright.bdstatic.com/vcg/creative/4f3552b7918c79e00c925e9990fd1236.jpg@c_1,w_900,h_600,x_150,y_0',
    link: '/user/categories'
  },
  {
    id: 3,
    title: 'AI医疗助手随时问诊',
    imageUrl: 'https://jg-app.obs.cn-north-4.myhuaweicloud.com/prod/upload/2/jpg/194F201B5C3526BF4E46316EEBF19387.jpg',
    link: '/user/chat'
  }
])

const recommendedItems = ref<any[]>([])

const popularItems = ref<any[]>([])

const popularCategories = ref<any[]>([])

const formatNumber = (num: number) => {
  if (num < 1000) return num
  if (num < 10000) return (num / 1000).toFixed(1) + 'k'
  return (num / 10000).toFixed(1) + 'w'
}

const handleBannerClick = (banner: any) => {
  router.push(banner.link)
}

const goToItemDetail = (id: number) => {
  router.push(`/user/item/${id}`)
}

const goToCategoryDetail = (id: number) => {
  router.push(`/user/category/${id}`)
}

const goToChat = () => {
  router.push('/user/chat')
}

const fetchRecommendedItems = async () => {
  try {
    const res = await itemApi.page({
      current: 1,
      size: 8
    })
    recommendedItems.value = res.records

  } catch (error) {
    console.error('获取常见病例失败', error)
  }
}

const fetchPopularItems = async () => {
  try {
    const res = await itemApi.page({
      current: 1,
      size: 12
    })
    let items = res.records


    items.sort((a, b) => {
      const scoreA = ((a.favorites ?? 0) * 1.5) + ((a.views ?? 0) * 0.7)
      const scoreB = ((b.favorites ?? 0) * 1.5) + ((b.views ?? 0) * 0.7)
      return scoreB - scoreA
    })

    popularItems.value = items.slice(0, 8)
  } catch (error) {
    console.error('获取典型病例失败', error)
  }
}

const fetchPopularCategories = async () => {
  try {
    const res = await categoryApi.page({
      current: 1,
      size: 6
    })
    popularCategories.value = res.records
  } catch (error) {
    console.error('获取热门科室失败', error)
  }
}

const fetchUserStats = async () => {
  try {
    const favoriteRes = await favoriteApi.getUserFavoriteItemIds(userId?userId:0);
    userStats.value.favorites = favoriteRes.length;
    const historyRes = await pageMyActions({
      userId: userId?userId:0,
      current: 1,
      size: 1,
      actionType: 0
    });
    userStats.value.history = historyRes.total;

    const purchaseRes = await pageMyActions({
      userId: userId?userId:0,
      current: 1,
      size: 1,
      actionType: 1
    });
    userStats.value.purchases = purchaseRes.total;
  } catch (error) {
    console.error('获取用户统计数据失败', error);
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchRecommendedItems(),
      fetchPopularItems(),
      fetchPopularCategories(),
      fetchUserStats()
    ])
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.user-home {
  padding: 16px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.banner-section {
  margin-bottom: 20px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.1);
}

.banner-item {
  position: relative;
  cursor: pointer;
  border-radius: 16px;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
  width: 100%;
  height: 100%;
}

.banner-item:hover {
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.2);
}

.banner-image {
  width: 100%;
  height: 100%;
  border-radius: 16px;
}

.image-loading {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
}

.loading-icon {
  font-size: 32px;
  color: #107ede;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #5309f2;
  font-size: 24px;
}

.placeholder-text {
  font-size: 14px;
  margin-top: 8px;
}

.banner-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(44, 90, 160, 0.95));
  color: white;
  padding: 20px 24px;
  border-radius: 0 0 16px 16px;
  font-size: 18px;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.home-content {
  display: flex;
  gap: 20px;
}

.main-section {
  flex: 1;
}

.sidebar-section {
  width: 320px;
}

.section-container {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  transition: all 0.3s ease;
}

.section-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.12);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e1f0ff;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: #2c5aa0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #d2d6d9 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.more-link {
  color: #1144ec;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s ease;
}

.more-link:hover {
  color: #2c5aa0;
  transform: translateX(3px);
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.item-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #f0f8ff;
  box-shadow: 0 4px 16px rgba(44, 90, 160, 0.06);
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(44, 90, 160, 0.15);
  border-color: #0a68e4;
}

.item-cover {
  position: relative;
  height: 140px;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-stats {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat {
  background: rgba(44, 90, 160, 0.9);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  backdrop-filter: blur(10px);
}

.item-info {
  padding: 15px;
}

.item-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #2c5aa0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  color: #5a6c7d;
  font-size: 12px;
}

.uploader {
  display: flex;
  align-items: center;
}

.user-card,
.sidebar-card,
.chat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  transition: all 0.3s ease;
}

.user-card:hover,
.sidebar-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.12);
}

.user-profile {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-details {
  margin-left: 15px;
}

.username {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #2c5aa0;
}

.user-role {
  font-size: 12px;
  color: #5a6c7d;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.user-stats {
  display: flex;
  justify-content: space-between;
  border-top: 2px solid #e1f0ff;
  padding-top: 15px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #2c5aa0;
}

.stat-label {
  font-size: 12px;
  color: #5a6c7d;
  margin-top: 4px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e1f0ff;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #2c5aa0;
}

.category-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.category-list .category-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 10px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e1f0ff;
}

.category-list .category-item:hover {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  transform: translateY(-1px);
  border-color: #0a24ed;
}

.category-icon {
  width: 28px;
  height: 28px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 8px;
  color: #0a70dd;
}

.category-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.category-name {
  font-size: 14px;
  color: #2c5aa0;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  border-radius: 16px;
  border: 1px solid #0f32cf;
}

.chat-icon {
  font-size: 32px;
  color: #2214e7;
  margin-right: 15px;
}

.chat-info {
  flex: 1;
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c5aa0;
  margin-bottom: 6px;
}

.chat-desc {
  font-size: 13px;
  color: #5a6c7d;
  line-height: 1.4;
}

.chat-button {
  margin-left: 10px;
  background: linear-gradient(135deg, #0851e2 0%, #2c5aa0 100%);
  border: none;
  color: white;
  font-weight: 500;
}

.chat-button:hover {
  background: linear-gradient(135deg, #0a07d2 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(34, 9, 226, 0.3);
}

.loading-container {
  padding: 20px 0;
}

@media (max-width: 1200px) {
  .item-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .home-content {
    flex-direction: column;
  }
  
  .sidebar-section {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .user-home {
    padding: 15px;
  }
  
  .item-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .section-container {
    padding: 20px;
  }
  
  .home-content {
    gap: 20px;
  }
  
  .el-carousel {
    height: 200px !important;
  }
  
  .banner-title {
    font-size: 14px;
    padding: 15px 16px;
  }
}

@media (max-width: 576px) {
  .item-grid {
    grid-template-columns: 1fr;
  }
  
  .category-list {
    grid-template-columns: 1fr;
  }
  
  .chat-card {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .chat-icon {
    margin-right: 0;
  }
  
  .el-carousel {
    height: 160px !important;
  }
}
</style>
