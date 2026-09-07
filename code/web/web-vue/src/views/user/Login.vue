<template>
  <div class="login-container">
    <div class="login-background">
      <div class="medical-pattern"></div>
    </div>
    <div class="login-box">
      <div class="login-header">
        <div class="logo-container">
          <img src="@/assets/images/logo.png" alt="AI医生" class="logo-img" />
        </div>
        <h2>AI医生</h2>
        <p class="login-subtitle">智能AI</p>
      </div>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        size="large"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            class="medical-input"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            class="medical-input"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            <el-icon><UserFilled /></el-icon>
            {{ loading ? '登录中...' : '安全登录' }}
          </el-button>
        </el-form-item>
        <div class="login-options">
          <router-link to="/register" class="register-link">
            <el-icon><Plus /></el-icon>
            注册新账号
          </router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useRoute, useRouter } from 'vue-router'
import { UserFilled, Plus } from '@element-plus/icons-vue'

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const loginForm = ref({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ]
}

const loading = ref(false)
const loginFormRef = ref<FormInstance>()

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    loading.value = true

    await userStore.login(loginForm.value.username, loginForm.value.password)

    const redirect = route.query.redirect as string
    const targetPath = (redirect && redirect.startsWith('/')) ? redirect : '/'

    router.replace(targetPath)
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background: radial-gradient(circle at 20% 30%, rgba(37, 99, 235, 0.08), transparent 35%),
    radial-gradient(circle at 80% 10%, rgba(6, 182, 212, 0.1), transparent 40%),
    var(--color-page);
  overflow: hidden;
}

.login-background {
  position: absolute;
  inset: 0;
}

.medical-pattern {
  width: 100%;
  height: 100%;
}

.login-box {
  width: 420px;
  padding: 36px 32px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-strong);
  border: 1px solid var(--color-border);
  z-index: 10;
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.logo-container {
  margin-bottom: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-img {
  height: 72px;
  width: auto;
  max-width: 200px;
  object-fit: contain;
  filter: drop-shadow(0 6px 20px rgba(37, 99, 235, 0.25));
}

.login-box h2 {
  color: var(--color-text-strong);
  margin-bottom: 6px;
  font-size: 1.7rem;
  font-weight: 700;
}

.login-subtitle {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  margin: 0;
}

.medical-input {
  margin-bottom: 16px;
}

.medical-input .el-input__wrapper {
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  transition: all 0.2s ease;
}

.medical-input .el-input__wrapper.is-focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.login-button {
  width: 100%;
  height: 50px;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 1.05rem;
  font-weight: 700;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.login-button:hover {
  background: var(--color-primary-strong);
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
}

.login-options {
  margin-top: 18px;
  text-align: center;
}

.register-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.register-link:hover {
  color: var(--color-primary-strong);
  transform: translateX(2px);
}

@media (max-width: 480px) {
  .login-box {
    width: 90%;
    padding: 38px 28px;
    margin: 20px;
  }

  .logo-img {
    height: 60px;
  }

  .login-box h2 {
    font-size: 1.5rem;
  }
}
</style>
