<template>
  <div class="register-container">
    <div class="register-background">
      <div class="medical-pattern"></div>
    </div>
    <div class="register-box">
      <div class="register-header">
        <div class="logo-container">
          <img src="@/assets/images/logo.png" alt="AI医生" class="logo-img" />
        </div>
        <h2>注册新账号</h2>
        <p class="register-subtitle">体验AI医生</p>
      </div>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
        size="large"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            class="medical-input"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
            class="medical-input"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请确认密码"
            show-password
            class="medical-input"
          />
        </el-form-item>
        <el-form-item label="真实姓名" prop="realName">
          <el-input
            v-model="registerForm.realName"
            placeholder="请输入真实姓名"
            class="medical-input"
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="registerForm.phone"
            placeholder="请输入手机号"
            class="medical-input"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            class="medical-input"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="register-button"
            @click="handleRegister"
          >
            <el-icon><UserFilled /></el-icon>
            {{ loading ? '注册中...' : '立即注册' }}
          </el-button>
        </el-form-item>
        <div class="register-options">
          已有账号？
          <router-link to="/login" class="login-link">
            <el-icon><Key /></el-icon>
            立即登录
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
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UserFilled, Key } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  realName: '',
  phone: '',
  email: ''
})

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '真实姓名长度应在2-20个字符之间', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email' as const, message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const loading = ref(false)
const registerFormRef = ref<FormInstance>()

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()
    loading.value = true

    const { confirmPassword, ...registerData } = registerForm.value
    await userStore.register(registerData)

    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background: url('@/assets/images/login-bg.jpg') center center/cover no-repeat;
  overflow: hidden;
  padding: 20px 0;
}

.register-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.medical-pattern {
  width: 100%;
  height: 100%;
}

.register-box {
  width: 520px;
  padding: 32px 30px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  z-index: 10;
  margin: 20px;
}

.register-header {
  text-align: center;
  margin-bottom: 24px;
}

.logo-container {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-img {
  height: 80px;
  width: auto;
  max-width: 200px;
  object-fit: contain;
  filter: drop-shadow(0 4px 12px rgba(22, 160, 133, 0.3));
}

.register-box h2 {
  color: #2c5aa0;
  margin-bottom: 8px;
  font-size: 1.8rem;
  font-weight: 600;
}

.register-subtitle {
  color: #5a6c7d;
  font-size: 1rem;
  margin: 0;
}

.register-form {
  margin-top: 20px;
}

.register-form .el-form-item__label {
  color: #2c5aa0;
  font-weight: 500;
}

.medical-input .el-input__wrapper {
  border-radius: 10px;
  border: 2px solid #e1f0ff;
  background: #f8fbff;
  transition: all 0.3s ease;
}

.medical-input .el-input__wrapper:hover {
  border-color: #0a56da;
}

.medical-input .el-input__wrapper.is-focus {
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.register-button {
  width: 100%;
  height: 50px;
  background: linear-gradient(135deg, #0851e3 0%, #2c5aa0 100%);
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 20px;
  transition: all 0.3s ease;
}

.register-button:hover {
  background: linear-gradient(135deg, #0983ed 0%, #1e4d8c 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(22, 160, 133, 0.3);
}

.register-options {
  margin-top: 20px;
  text-align: center;
  color: #5a6c7d;
}

.login-link {
  color: #0c2ce0;
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
  margin-left: 8px;
}

.login-link:hover {
  color: #2c5aa0;
  transform: translateX(3px);
}

@media (max-width: 600px) {
  .register-box {
    width: 95%;
    padding: 40px 25px;
    margin: 10px;
  }
  
  .logo-img {
    height: 60px;
  }
  
  .register-box h2 {
    font-size: 1.6rem;
  }
  
  .register-form .el-form-item__label {
    width: 70px !important;
  }
}
</style> 