<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
      <div class="logo" :class="{ 'logo-collapse': isCollapse }">
        <img src="@/assets/images/logo.png" alt="logo" />
        <span v-show="!isCollapse">AI医生</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="menu"
        :router="true"
        :collapse="isCollapse"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <template v-if="isAdmin">
          <el-menu-item index="/admin">
            <el-icon><Monitor /></el-icon>
            <template #title>控制台</template>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <template #title>用户管理</template>
          </el-menu-item>
          <el-menu-item index="/admin/categories">
            <el-icon><Files /></el-icon>
            <template #title>科室管理</template>
          </el-menu-item>
          <el-menu-item index="/admin/items">
            <el-icon><Files /></el-icon>
            <template #title>病例管理</template>
          </el-menu-item>
          <el-menu-item index="/admin/user-actions">
            <el-icon><Clock /></el-icon>
            <template #title>患者行为历史</template>
          </el-menu-item>
          <el-menu-item index="/admin/rag">
            <el-icon><Search /></el-icon>
            <template #title>智能检索管理</template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-icon
            class="collapse-btn"
            @click="toggleCollapse"
          >
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/user' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <AlgoHealthCheck class="health-check" />
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" :src="userInfo?.avatarUrl" />
              <span>{{ userInfo?.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Monitor, User, Files, Fold, Expand, Clock, Search } from '@element-plus/icons-vue'
import AlgoHealthCheck from './AlgoHealthCheck.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const userInfo = computed(() => userStore.userInfo)

const isAdmin = computed(() => userStore.isAdmin())

const isCollapse = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleCommand = (command: string) => {
  switch (command) {
    case 'logout':
      userStore.logout()
      break
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: var(--color-page);
}

.aside {
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  transition: width 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 18px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-strong);
}

.logo-collapse {
  justify-content: center;
}

.logo img {
  width: 34px;
  height: 34px;
  border-radius: 8px;
}

.logo span {
  font-weight: 700;
  letter-spacing: 0.5px;
}

.menu {
  border-right: none;
  background: transparent;
  padding: 12px;
}

:deep(.el-menu-item) {
  border-radius: var(--radius-md);
  margin: 4px 0;
  color: var(--color-text-muted);
}

:deep(.el-menu-item.is-active) {
  background: rgba(37, 99, 235, 0.12);
  color: var(--color-primary);
}

:deep(.el-menu-item:hover) {
  background: rgba(37, 99, 235, 0.08);
  color: var(--color-primary-strong);
}

.header {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-soft);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  color: var(--color-primary);
  padding: 8px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  border-radius: 24px;
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  cursor: pointer;
}

.user-info span {
  color: var(--color-text);
  font-weight: 600;
}

.main {
  background: var(--color-page);
  padding: 16px;
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
  .header {
    padding: 0 14px;
  }

  .main {
    padding: 16px;
  }
}
</style>
