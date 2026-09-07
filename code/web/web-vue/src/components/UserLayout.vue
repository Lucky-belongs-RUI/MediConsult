<template>
  <div class="user-layout">
    <header class="main-header">
      <div class="header-container">
        <div class="header-left">
          <div class="logo">
            <img src="@/assets/images/logo.png" alt="logo" />
            <span>AI医生</span>
          </div>
          <nav class="primary-nav">
            <router-link to="/user/home" class="nav-item">首页</router-link>
            <router-link to="/user/items" class="nav-item">公开病例</router-link>
            <router-link to="/user/categories" class="nav-item">全部科室</router-link>
            <router-link to="/user/chat" class="nav-item">智能医生</router-link>
          </nav>
        </div>

        <div class="header-center">
          <div class="search-box">
            <el-input
              v-model="searchText"
              placeholder="搜索病例..."
              @keyup.enter="handleSearch"
              clearable
            >
              <template #prefix>
                <el-dropdown trigger="click" @command="handleSearchModeChange">
                  <div class="search-mode">
                    {{ searchMode === 'title' ? '病例名称' : '症状标签' }}
                    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                  </div>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="title">病例名称</el-dropdown-item>
                      <el-dropdown-item command="tag">症状标签</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
              <template #suffix>
                <el-icon class="search-icon" @click="handleSearch"><Search /></el-icon>

                <el-popover
                  placement="bottom"
                  :width="320"
                  trigger="click"
                  v-model:visible="showAdvancedSearch"
                  popper-class="advanced-search-popover"
                  :teleported="true"
                  :stop-popper-mouse-event="false"
                >
                  <template #reference>
                    <el-icon class="advanced-search-icon" @click.stop><Setting /></el-icon>
                  </template>
                  <div class="advanced-search-panel">
                    <h4>高级搜索</h4>
                    <el-form :model="advancedSearchForm" label-position="top">
                      <el-form-item label="病例名称">
                        <el-input v-model="advancedSearchForm.title" placeholder="输入病例名称"></el-input>
                      </el-form-item>
                      <el-form-item label="症状标签">
                        <el-input v-model="advancedSearchForm.tag" placeholder="输入症状标签关键词"></el-input>
                      </el-form-item>
                      <el-form-item label="科室">
                        <el-select v-model="advancedSearchForm.categoryId" placeholder="选择科室" clearable style="width: 100%">
                          <el-option
                            v-for="category in popularCategories"
                            :key="category.id"
                            :label="category.name"
                            :value="category.id"
                          />
                        </el-select>
                      </el-form-item>
                      <div class="advanced-search-actions">
                        <el-button type="primary" @click="handleAdvancedSearch">搜索</el-button>
                        <el-button @click="resetAdvancedSearch">重置</el-button>
                      </div>
                    </el-form>
                  </div>
                </el-popover>
              </template>
            </el-input>
          </div>
        </div>

        <div class="header-right">
          <AlgoHealthCheck class="health-check" />
          <div class="user-actions">
            <router-link to="/user/favorites" class="action-item">
              <el-icon><Star /></el-icon>
              <span>病例收藏</span>
            </router-link>
            <router-link to="/user/history/browsing" class="action-item">
              <el-icon><View /></el-icon>
              <span>浏览记录</span>
            </router-link>
          </div>
          <el-dropdown @command="handleCommand" class="user-dropdown">
            <div class="user-info">
              <el-avatar :size="32" :src="userInfo?.avatarUrl || defaultAvatar">
                {{ userInfo?.username?.substring(0, 1) }}
              </el-avatar>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>

                <el-dropdown-item v-if="isAdmin" command="admin">管理控制台</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </router-view>
    </main>

    <el-backtop :right="20" :bottom="20" />

    <footer class="main-footer" v-if="isHomePage">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-logo">
            <img src="@/assets/images/logo.png" alt="logo" />
            <span>AI医生</span>
          </div>
          <div class="footer-info">
            <p>© 2025 AI医生 版权所有</p>
            <p>前端：Vue 3 + TypeScript + Vite + Element Plus + Pinia + Axios + ECharts + WebSocket | </p>
              <p>后端：Spring Boot + MyBatis-Plus + MySQL + JWT |</p>
              <p> 算法服务：FastAPI + Python + RAG + 向量检索 | </p>
              <p> 文件服务：FastAPI | 核心技术：检索增强生成、TF-IDF、余弦相似度</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AlgoHealthCheck from './AlgoHealthCheck.vue'
import { categoryApi } from '@/api/category'
import { Search, Star, View, User, House, Menu, ChatDotRound, Grid, ArrowDown, Setting } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const searchText = ref('')
const showAdvancedSearch = ref(false)
const searchMode = ref('title')
const advancedSearchForm = reactive({
  title: '',
  tag: '',
  categoryId: undefined as number | undefined
})

const userInfo = computed(() => userStore.userInfo)

const isAdmin = computed(() => userStore.isAdmin())

const isHomePage = computed(() => {
  return router.currentRoute.value.path === '/user/home'
})

const popularCategories = ref<any[]>([])

const defaultAvatar = 'https://img0.baidu.com/it/u=520343531,2599065610&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500'

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/user/profile')
      break

    case 'admin':
      router.push('/admin')
      break
    case 'logout':
      userStore.logout()
      break
  }
}

const handleSearch = () => {
  if (searchText.value.trim()) {
    const query: Record<string, string | number> = {}

    if (searchMode.value === 'title') {
      query.keyword = searchText.value.trim()
    } else if (searchMode.value === 'tag') {
      query.tag = searchText.value.trim()
    }

    router.push({
      path: '/user/items',
      query
    })

    showAdvancedSearch.value = false
  }
}

const fetchPopularCategories = async () => {
  try {
    const res = await categoryApi.page({
      current: 1,
      size: 6
    })
    if (res && res.records) {
      popularCategories.value = res.records
    }
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

const handleAdvancedSearch = () => {
  const query: Record<string, string | number> = {}

  if (advancedSearchForm.title.trim()) {
    query.keyword = advancedSearchForm.title.trim()
  }

  if (advancedSearchForm.tag.trim()) {
    query.tag = advancedSearchForm.tag.trim()
  }

  if (advancedSearchForm.categoryId !== undefined) {
    query.categoryId = advancedSearchForm.categoryId
  }

  router.push({
    path: '/user/items',
    query
  })

  showAdvancedSearch.value = false
}

const resetAdvancedSearch = () => {
  advancedSearchForm.title = ''
  advancedSearchForm.tag = ''
  advancedSearchForm.categoryId = undefined
}

const handleSearchModeChange = (command: string) => {
  searchMode.value = command
}

watch(() => router.currentRoute.value.fullPath, () => {
  showAdvancedSearch.value = false
})

const documentClickHandler = (e: MouseEvent) => {
  if (showAdvancedSearch.value) {
    const popover = document.querySelector('.advanced-search-popover')
    const target = e.target as Node
    if (popover && !popover.contains(target)) {
      showAdvancedSearch.value = false
    }
  }
}

onMounted(() => {
  fetchPopularCategories()

  document.addEventListener('click', documentClickHandler)
})

onUnmounted(() => {
  document.removeEventListener('click', documentClickHandler)
})
</script>

<style>
body {
  margin: 0;
  min-height: 100vh;
  overflow-y: auto !important;
}

.el-overlay {
  overflow: hidden;
  position: fixed;
}

.el-popup-parent--hidden {
  overflow: auto !important;
  padding-right: 0 !important;
}
</style>

<style scoped>
.user-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--color-page);
}

.main-header {
  position: fixed;
  inset: 0 0 auto 0;
  height: 72px;
  z-index: 1000;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-soft);
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 100%;
  height: 100%;
  padding: 0 20px;
  gap: 16px;
  box-sizing: border-box;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: var(--color-text-strong);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  background: var(--color-surface-muted);
  border: 1px solid var(--color-border);
}

.logo img {
  height: 32px;
  border-radius: 8px;
}

.primary-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  padding: 0 14px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  transition: all 0.2s ease;
}

.nav-item:hover {
  color: var(--color-primary);
  background: rgba(37, 99, 235, 0.08);
}

.nav-item.router-link-active {
  color: var(--color-primary);
  background: rgba(37, 99, 235, 0.12);
  font-weight: 600;
}

.header-center {
  flex: 1;
  max-width: 600px;
}

.search-box {
  width: 100%;
}

:deep(.el-input__wrapper) {
  border-radius: 999px;
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  box-shadow: none;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
}

.search-mode {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 14px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
}

.search-icon,
.advanced-search-icon {
  cursor: pointer;
  color: var(--color-text-subtle);
}

.advanced-search-panel {
  padding: 16px;
}

.advanced-search-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 12px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-actions {
  display: flex;
  gap: 8px;
}

.action-item {
  padding: 8px 12px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  transition: all 0.2s ease;
}

.action-item:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.user-info {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 24px;
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  cursor: pointer;
}

.user-info .el-avatar {
  border: 2px solid var(--color-border);
}

.category-nav {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 12px 0;
  margin-top: 68px;
}

.category-nav-container {
  max-width: var(--container-width);
  margin: 0 auto;
  padding: 0 20px;
}

.primary-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 18px;
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  transition: all 0.2s ease;
}

.category-item:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.category-item.router-link-active {
  color: var(--color-primary);
  background: rgba(37, 99, 235, 0.12);
  border-color: rgba(37, 99, 235, 0.4);
}

.category-icon {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  object-fit: cover;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 100%;
  margin: 72px 0 12px;
  padding: 0 16px;
  box-sizing: border-box;
}

.main-footer {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: 20px 0;
  margin-top: 20px;
}

.footer-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0 20px;
  box-sizing: border-box;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
  color: var(--color-text-muted);
}

.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: var(--color-text-strong);
}

.footer-logo img {
  height: 26px;
  border-radius: 6px;
}

.footer-info p {
  margin: 4px 0;
}

:deep(.el-dropdown-menu) {
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-soft);
}

:deep(.el-dropdown-menu__item) {
  color: var(--color-text-muted);
}

:deep(.el-dropdown-menu__item:hover) {
  color: var(--color-primary);
}

:deep(.advanced-search-popover) {
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-strong);
}

:deep(.el-button--primary) {
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-md);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 14px;
    gap: 12px;
  }

  .header-left {
    gap: 12px;
  }

  .nav-item {
    padding: 0 10px;
    height: 44px;
    font-size: 14px;
  }

  .header-center {
    max-width: 360px;
  }

  .main-content {
    padding: 0 12px;
  }

  .category-nav-container {
    padding: 0 14px;
  }
}
</style>
