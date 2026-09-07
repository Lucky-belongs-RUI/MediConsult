import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: to => {
      const userStore = useUserStore();
      if (!userStore.isLoggedIn()) {
        return '/login';
      }
      
      if (userStore.isAdmin()) {
        return '/admin';
      } else {
        return '/user/home';
      }
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/user/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/user/Register.vue'),
    meta: {
      title: '注册',
      requiresAuth: false
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/admin/Dashboard.vue'),
    meta: {
      title: '首页'
    }
  },
  {
    path: '/user',
    component: () => import('@/components/UserLayout.vue'),
    redirect: '/user/home',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'home',
        name: 'UserHome',
        component: () => import('@/views/user/Home.vue'),
        meta: {
          title: '首页',
          requiresAuth: true
        }
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('@/views/user/Profile.vue'),
        meta: {
          title: '个人中心',
          requiresAuth: true
        }
      },
      {
        path: 'favorites',
        name: 'UserFavorites',
        component: () => import('@/views/user/MyFavorites.vue'),
        meta: {
          title: '我的病例收藏',
          requiresAuth: true
        }
      },
      {
        path: 'history/browsing',
        name: 'UserBrowsingHistory',
        component: () => import('@/views/history/BrowsingHistory.vue'),
        meta: {
          title: '浏览病例历史',
          requiresAuth: true
        }
      },

      {
        path: 'categories',
        name: 'UserCategories',
        component: () => import('@/views/category/CategoryList.vue'),
        meta: {
          title: '科室浏览',
          requiresAuth: true
        }
      },
      {
        path: 'category/:id',
        name: 'UserCategoryDetail',
        component: () => import('@/views/category/CategoryDetail.vue'),
        meta: {
          title: '科室详情',
          requiresAuth: true
        }
      },
      {
        path: 'items',
        name: 'UserItems',
        component: () => import('@/views/item/ItemList.vue'),
        meta: {
          title: '病例浏览',
          requiresAuth: true
        }
      },
      {
        path: 'item/:id',
        name: 'UserItemDetail',
        component: () => import('@/views/item/ItemDetail.vue'),
        meta: {
          title: '病例详情',
          requiresAuth: true
        }
      },
      {
        path: 'chat',
        name: 'UserChatSessionList',
        component: () => import('@/views/chat/ChatView.vue'),
        meta: {
          title: 'AI问诊',
          requiresAuth: true
        }
      },
    ]
  },
  {
    path: '/admin',
    component: () => import('@/components/Layout.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
    children: [
      {
        path: '',
        name: 'Admin',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: {
          title: '管理控制台',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('@/views/admin/UserManagement.vue'),
        meta: {
          title: '用户管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'categories',
        name: 'CategoryManagement',
        component: () => import('@/views/admin/CategoryManagement.vue'),
        meta: {
          title: '科室管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'items',
        name: 'ItemManagement',
        component: () => import('@/views/admin/ItemManagement.vue'),
        meta: {
          title: '病例管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'user-actions',
        name: 'UserActionHistory',
        component: () => import('@/views/admin/UserActionHistory.vue'),
        meta: {
          title: '患者行为历史',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'rag',
        name: 'RagManagement',
        component: () => import('@/views/admin/RagManagement.vue'),
        meta: {
          title: 'RAG技术-智能检索数据管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)

  if (requiresAuth) {
    if (!userStore.isLoggedIn()) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }

    if (requiresAdmin && !userStore.isAdmin()) {
      next({ name: 'UserHome' })
      return
    }
  }

  next()
})

export default router 