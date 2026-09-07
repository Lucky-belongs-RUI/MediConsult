<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="dashboard-title">
        <el-icon class="title-icon"><FirstAidKit /></el-icon>
        AI医生
      </h1>
      <p class="dashboard-subtitle">专业医疗服务，守护您的健康</p>
    </div>
    
    <div class="welcome-card">
      <div class="welcome-content">
        <h2>欢迎使用AI医生</h2>
        <p>这里为您提供专业的医疗咨询服务，您可以查看病例、与AI医生对话，获得专业的医疗建议。</p>
        <div class="quick-actions">
          <el-button type="primary" size="large" @click="router.push('/user/chat')">
            <el-icon><ChatDotRound /></el-icon>
            开始问诊
          </el-button>
          <el-button type="success" size="large" @click="router.push('/user/items')">
            <el-icon><Document /></el-icon>
            查看病例
          </el-button>
        </div>
      </div>
      <div class="welcome-image">
        <el-icon class="medical-icon"><FirstAidKit /></el-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { FirstAidKit, ChatDotRound, Document } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)

const currentDate = new Date().toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long'
})


</script>

<style scoped>
.dashboard {
  padding: 16px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.dashboard-header {
  text-align: center;
  margin-bottom: 24px;
  padding: 20px 0;
}

.dashboard-title {
  font-size: 2.5rem;
  color: #2c5aa0;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  font-weight: 600;
}

.title-icon {
  font-size: 2.5rem;
  color: #16a085;
}

.dashboard-subtitle {
  font-size: 1.2rem;
  color: #5a6c7d;
  margin: 0;
}

.welcome-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.1);
  border: 1px solid #e1f0ff;
  display: flex;
  align-items: center;
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.welcome-content {
  flex: 1;
}

.welcome-content h2 {
  color: #2c5aa0;
  font-size: 1.8rem;
  margin-bottom: 15px;
  font-weight: 600;
}

.welcome-content p {
  color: #5a6c7d;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 16px;
}

.quick-actions {
  display: flex;
  gap: 20px;
}

.quick-actions .el-button {
  border-radius: 25px;
  padding: 12px 30px;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.quick-actions .el-button--primary {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border: none;
}

.quick-actions .el-button--primary:hover {
  background: linear-gradient(135deg, #138d75 0%, #1e4d8c 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(22, 160, 133, 0.3);
}

.quick-actions .el-button--success {
  background: linear-gradient(135deg, #27ae60 0%, #16a085 100%);
  border: none;
}

.quick-actions .el-button--success:hover {
  background: linear-gradient(135deg, #229954 0%, #138d75 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
}

.welcome-image {
  flex-shrink: 0;
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #16a085;
}

.medical-icon {
  font-size: 5rem;
  color: #16a085;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 15px;
  }
  
  .dashboard-title {
    font-size: 2rem;
  }
  
  .welcome-card {
    flex-direction: column;
    padding: 30px 20px;
    text-align: center;
  }
  
  .quick-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .quick-actions .el-button {
    width: 200px;
  }
  
  .welcome-image {
    width: 120px;
    height: 120px;
  }
  
  .medical-icon {
    font-size: 4rem;
  }
}
</style> 