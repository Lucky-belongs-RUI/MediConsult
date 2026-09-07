<template>
  <div class="profile-container">
    <el-card class="profile-header-card" shadow="hover">
      <div class="profile-header">
        <div class="avatar-container">
          <el-avatar
            :size="100"
            :src="userInfo?.avatarUrl"
          />
          <el-upload
            class="avatar-uploader"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleAvatarChange"
            :before-upload="beforeAvatarUpload"
          >
            <el-button
              type="primary"
              link
              class="change-avatar-btn"
            >
              <el-icon><Camera /></el-icon>
              更换头像
            </el-button>
          </el-upload>
        </div>
        
        <div class="user-base-info">
          <h2 class="username">{{ userInfo?.username || '未登录' }}</h2>
          <div class="user-meta">
            <el-tag :type="userInfo?.role === 1 ? 'danger' : 'info'" size="small">
              {{ userInfo?.role === 1 ? '管理员' : '普通用户' }}
            </el-tag>
            <el-tag :type="userInfo?.status === 1 ? 'success' : 'danger'" size="small">
              {{ userInfo?.status === 1 ? '正常' : '禁用' }}
            </el-tag>
          </div>
          <p class="user-desc" v-if="userInfo?.email">{{ userInfo?.email }}</p>
        </div>
      </div>
    </el-card>

    <el-card class="profile-tabs-card" shadow="hover">
      <el-tabs type="border-card">
        <el-tab-pane label="个人信息">
          <div class="tab-header">
            <h3>个人详细信息</h3>
            <el-button
              type="primary"
              @click="handleEdit"
            >
              <el-icon><Edit /></el-icon>
              编辑资料
            </el-button>
          </div>
          
          <el-descriptions :column="2" border>
            <el-descriptions-item label="用户名">
              {{ userInfo?.username }}
            </el-descriptions-item>
            <el-descriptions-item label="真实姓名">
              {{ userInfo?.realName || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="手机号">
              {{ userInfo?.phone || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ userInfo?.email || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="角色" :span="2">
              <el-tag :type="userInfo?.role === 1 ? 'danger' : 'info'">
                {{ userInfo?.role === 1 ? '管理员' : '普通用户' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="账号状态" :span="2">
              <el-tag :type="userInfo?.status === 1 ? 'success' : 'danger'">
                {{ userInfo?.status === 1 ? '正常' : '禁用' }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
        
        <el-tab-pane label="修改密码">
          <div class="tab-header">
            <h3>安全设置</h3>
          </div>
          
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
            class="password-form"
            status-icon
          >
            <el-form-item label="原密码" prop="oldPassword">
              <el-input
                v-model="passwordForm.oldPassword"
                type="password"
                show-password
                placeholder="请输入原密码"
              />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                show-password
                placeholder="请输入新密码"
              />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                show-password
                placeholder="请确认新密码"
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                :loading="passwordLoading"
                @click="handleChangePassword"
              >
                <el-icon><Check /></el-icon>
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="我的收藏">
          <MyFavorites />
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog
      v-model="editDialogVisible"
      title="编辑个人信息"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="真实姓名" prop="realName">
          <el-input
            v-model="editForm.realName"
            placeholder="请输入真实姓名"
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="editForm.phone"
            placeholder="请输入手机号"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="editForm.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>

        <el-form-item class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="editLoading"
            @click="handleSaveEdit"
          >
            确定
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { FormInstance, UploadProps, FormItemRule } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { updateUser } from '@/api/user'
import { fileRequest } from '@/api/file_request'
import type { UpdateUserParams } from '@/types/user'
import { Edit, Camera, Check } from '@element-plus/icons-vue'
import MyFavorites from './MyFavorites.vue'

const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.value.newPassword) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

const passwordLoading = ref(false)
const passwordFormRef = ref<FormInstance>()

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true

    await userStore.changePassword({
      id: userInfo.value?.id as number,
      oldPassword: passwordForm.value.oldPassword,
      newPassword: passwordForm.value.newPassword
    })

    ElMessage.success('密码修改成功')
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    console.error('修改密码失败:', error)
  } finally {
    passwordLoading.value = false
  }
}

const editForm = ref({
  realName: '',
  phone: '',
  email: ''
})

const editRules = {
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
    { pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
} satisfies Record<string, FormItemRule[]>

const editDialogVisible = ref(false)
const editLoading = ref(false)
const editFormRef = ref<FormInstance>()

const handleEdit = () => {
  editForm.value = {
    realName: userInfo.value?.realName || '',
    phone: userInfo.value?.phone || '',
    email: userInfo.value?.email || ''
  }
  editDialogVisible.value = true
}

const handleSaveEdit = async () => {
  if (!editFormRef.value) return

  try {
    await editFormRef.value.validate()
    editLoading.value = true

    await updateUser({
      id: userInfo.value?.id as number,
      realName: editForm.value.realName,
      phone: editForm.value.phone,
      email: editForm.value.email,
      role: userInfo.value?.role as number,
      status: userInfo.value?.status as number
    })

    const storedUserInfo = localStorage.getItem('userInfo')
    if (storedUserInfo) {
      const data = JSON.parse(storedUserInfo)
      data.userInfo = {
        ...data.userInfo,
        realName: editForm.value.realName,
        phone: editForm.value.phone,
        email: editForm.value.email
      }
      localStorage.setItem('userInfo', JSON.stringify(data))
      userStore.initUserInfo()
    }

    ElMessage.success('个人信息修改成功')
    editDialogVisible.value = false
  } catch (error) {
    console.error('修改个人信息失败:', error)
  } finally {
    editLoading.value = false
  }
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (file: any) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isJPG && !isPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('头像大小不能超过 10MB!')
    return false
  }
  return true
}

const handleAvatarChange: UploadProps['onChange'] = async (uploadFile: any) => {
  if (!uploadFile.raw) return
  
  try {
    const { bucket, objectKey } = await fileRequest.upload('avatars', uploadFile.raw)
    
    const updateParams: UpdateUserParams = {
      id: userInfo.value?.id as number,
      avatarBucket: bucket,
      avatarObjectKey: objectKey
    }
    await updateUser(updateParams)
    
    const storedUserInfo = localStorage.getItem('userInfo')
    if (storedUserInfo) {
      const data = JSON.parse(storedUserInfo)
      data.userInfo = {
        ...data.userInfo,
        avatarBucket: bucket,
        avatarObjectKey: objectKey,
        avatarUrl: fileRequest.getFileUrl(bucket, objectKey)
      }
      localStorage.setItem('userInfo', JSON.stringify(data))
      userStore.initUserInfo()
    }
    
    ElMessage.success('头像更新成功')
  } catch (error) {
    console.error('头像上传失败:', error)
    ElMessage.error('头像上传失败')
  }
}
</script>

<style scoped>
.profile-container {
  padding: 16px;
  min-height: calc(100vh - 140px);
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.profile-header-card {
  transition: all 0.3s ease;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  overflow: hidden;
}

.profile-header-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.15);
}

.profile-header {
  display: flex;
  gap: 24px;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.avatar-container .el-avatar {
  border: 4px solid #0778e1;
  box-shadow: 0 8px 25px rgba(22, 55, 71, 0.2);
}

.change-avatar-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #0d9fd4;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 20px;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  border: 1px solid #0c90c9;
  transition: all 0.3s ease;
}

.change-avatar-btn:hover {
  background: linear-gradient(135deg, #0f9fdc 0%, #2c5aa0 100%);
  color: white;
  transform: translateY(-1px);
}

.user-base-info {
  flex: 1;
}

.username {
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c5aa0;
}

.user-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
}

.user-meta .el-tag {
  border-radius: 15px;
  font-weight: 500;
  padding: 4px 12px;
}

.user-meta .el-tag--danger {
  background: linear-gradient(135deg, #fde8e8 0%, #fad2d2 100%);
  color: #e53e3e;
  border-color: #e53e3e;
}

.user-meta .el-tag--info {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #0da8d6;
  border-color: #1894e6;
}

.user-meta .el-tag--success {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #0d5bc1;
  border-color: #197ddb;
}

.user-desc {
  color: #5a6c7d;
  margin: 8px 0;
  font-size: 1rem;
}

.profile-tabs-card {
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  overflow: hidden;
}

.profile-tabs-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.12);
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e1f0ff;
}

.tab-header h3 {
  margin: 0;
  font-size: 1.3rem;
  color: #2c5aa0;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-header h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #0c87d8 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.tab-header .el-button--primary {
  background: linear-gradient(135deg, #0783ee 0%, #2c5aa0 100%);
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-weight: 500;
}

.tab-header .el-button--primary:hover {
  background: linear-gradient(135deg, #197db4 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(22, 160, 133, 0.3);
}

.password-form {
  max-width: 500px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-radius: 12px;
  border: 1px solid #e1f0ff;
}

.password-form .el-form-item__label {
  color: #2c5aa0;
  font-weight: 500;
}

.password-form .el-button--primary {
  background: linear-gradient(135deg, #0bb5f3 0%, #2c5aa0 100%);
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-weight: 500;
}

.password-form .el-button--primary:hover {
  background: linear-gradient(135deg, #09b4e8 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(22, 63, 160, 0.3);
}

:deep(.el-tabs__item) {
  font-size: 16px;
  padding: 0 25px;
  color: #5a6c7d;
  font-weight: 500;
}

:deep(.el-tabs__item.is-active) {
  color: #2c5aa0;
  font-weight: 600;
}

:deep(.el-tabs__nav) {
  border-radius: 12px 12px 0 0;
}

:deep(.el-tabs--border-card > .el-tabs__header) {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-bottom: 2px solid #e1f0ff;
}

:deep(.el-tabs--border-card > .el-tabs__header .el-tabs__item.is-active) {
  background-color: #fff;
  border-bottom-color: #fff;
  color: #2c5aa0;
}

:deep(.el-tabs--border-card > .el-tabs__content) {
  padding: 20px;
}

:deep(.el-descriptions__label) {
  font-weight: 600;
  color: #2c5aa0;
}

:deep(.el-descriptions__content) {
  color: #5a6c7d;
}

:deep(.el-descriptions .el-tag) {
  border-radius: 15px;
  font-weight: 500;
}

:deep(.el-descriptions .el-tag--danger) {
  background: linear-gradient(135deg, #fde8e8 0%, #fad2d2 100%);
  color: #e53e3e;
  border-color: #e53e3e;
}

:deep(.el-descriptions .el-tag--info) {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #1d95df;
  border-color: #1586d6;
}

:deep(.el-descriptions .el-tag--success) {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #1071b6;
  border-color: #1a63ab;
}

:deep(.el-button--primary) {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

:deep(.el-form--label-top .el-form-item__label) {
  margin-bottom: 8px;
}

:deep(.el-form-item__content) {
  flex-wrap: nowrap;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  border: 2px solid #e1f0ff;
  background: #f8fbff;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #1954a6;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  padding: 20px 25px;
  border-bottom: 2px solid #e1f0ff;
}

:deep(.el-dialog__title) {
  color: #2c5aa0;
  font-weight: 600;
  font-size: 1.2rem;
}

:deep(.el-dialog__body) {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 25px;
  margin-bottom: 0;
}

.dialog-footer .el-button {
  border-radius: 20px;
  padding: 10px 20px;
  font-weight: 500;
}

.dialog-footer .el-button--primary {
  background: linear-gradient(135deg, #1d83be 0%, #2c5aa0 100%);
  border: none;
}

.dialog-footer .el-button--primary:hover {
  background: linear-gradient(135deg, #1a5eb3 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(25, 105, 167, 0.3);
}

@media (max-width: 768px) {
  .profile-container {
    padding: 15px;
    gap: 20px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    padding: 25px;
    gap: 20px;
  }
  
  .username {
    font-size: 1.5rem;
  }
  
  .tab-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .password-form {
    padding: 15px;
  }
}
</style> 