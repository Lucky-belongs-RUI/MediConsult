<template>
  <div class="user">
    <div class="toolbar">
      <div class="left">
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新增用户
        </el-button>
      </div>
    </div>

    <el-form :model="queryParams" inline class="search-form">
      <el-form-item label="用户名">
        <el-input v-model="queryParams.username" placeholder="请输入用户名" clearable />
      </el-form-item>
      <el-form-item label="真实姓名">
        <el-input v-model="queryParams.realName" placeholder="请输入真实姓名" clearable />
      </el-form-item>
      <el-form-item label="用户角色">
        <el-select v-model="queryParams.role" placeholder="请选择用户角色" clearable class="form-select">
          <el-option :value="0" label="普通用户" />
          <el-option :value="1" label="管理员" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="loading" @click="handleQuery">
          <el-icon><Search /></el-icon>
          查询
        </el-button>
        <el-button @click="handleReset">
          <el-icon><Refresh /></el-icon>
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="list" border stripe>
      <el-table-column type="index" label="序号" width="60" align="center" />
      <el-table-column prop="username" label="用户名" min-width="120" show-overflow-tooltip />
      <el-table-column prop="realName" label="真实姓名" min-width="120" show-overflow-tooltip />
      <el-table-column prop="phone" label="手机号码" width="120" show-overflow-tooltip />
      <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
      <el-table-column prop="role" label="用户角色" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.role === 1 ? 'danger' : 'info'">
            {{ row.role === 1 ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" width="180" align="center">
        <template #default="{ row }">
          {{ formatDateTime(row.createTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" align="center" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleUpdate(row)">
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
          <el-button link type="primary" @click="handleResetPassword(row)">
            <el-icon><Key /></el-icon>
            重置密码
          </el-button>
          <el-button link type="danger" @click="handleDelete(row)">
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-model:current="queryParams.current"
      v-model:size="queryParams.size"
      :total="total"
      @change="getList"
    />

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新增用户' : '编辑用户'"
      width="500px"
      @close="resetForm"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" :disabled="dialogType === 'update'" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="realName">
          <el-input v-model="form.realName" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号码" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="用户角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择用户角色">
            <el-option :value="0" label="普通用户" />
            <el-option :value="1" label="管理员" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="dialogType === 'create'" label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import type { UserInfo } from '@/types/user'
import {
  getUserList,
  addUser,
  updateUser,
  deleteUser,
  resetPassword
} from '@/api/user'
import { formatDateTime } from '@/utils/format'
import { validatePhone, validateEmail } from '@/utils/validate'
import Pagination from '@/components/Pagination/index.vue'

const queryParams = reactive({
  current: 1,
  size: 10,
  username: undefined,
  realName: undefined,
  role: undefined,
})

const list = ref<UserInfo[]>([])
const total = ref(0)
const loading = ref(false)

const getList = async () => {
  loading.value = true
  try {
    const res = await getUserList(queryParams)
    list.value = res.records
    total.value = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryParams.current = 1
  getList()
}

const handleReset = () => {
  Object.assign(queryParams, {
    current: 1,
    size: 10,
    username: undefined,
    realName: undefined,
    role: undefined,
  })
  getList()
}

const formRef = ref<FormInstance>()
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'update'>('create')
const submitLoading = ref(false)

const form = reactive({
  id: 0,
  username: '',
  password: '',
  realName: '',
  phone: '',
  email: '',
  role: 0,
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { validator: (rule: any, value: string, callback: any) => {
      if (!validatePhone(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { validator: (rule: any, value: string, callback: any) => {
      if (!validateEmail(value)) {
        callback(new Error('请输入正确的邮箱'))
      } else {
        callback()
      }
    }, trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择用户角色', trigger: 'change' }
  ]
}

const handleCreate = () => {
  dialogType.value = 'create'
  dialogVisible.value = true
}

const handleUpdate = (row: UserInfo) => {
  dialogType.value = 'update'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleResetPassword = (row: UserInfo) => {
  ElMessageBox.confirm('确认重置该用户的密码？', '警告', {
    type: 'warning',
  })
    .then(async () => {
      await resetPassword(row.id)
      ElMessage.success('重置成功')
    })
    .catch(() => {})
}

const handleDelete = (row: UserInfo) => {
  ElMessageBox.confirm('确认删除该用户？删除后无法恢复！', '警告', {
    type: 'warning',
  })
    .then(async () => {
      await deleteUser(row.id)
      ElMessage.success('删除成功')
      getList()
    })
    .catch(() => {})
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.assign(form, {
    id: 0,
    username: '',
    password: '',
    realName: '',
    phone: '',
    email: '',
    role: 0,
  })
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  submitLoading.value = true
  try {
    if (dialogType.value === 'create') {
      await addUser(form)
      ElMessage.success('新增成功')
    } else {
      await updateUser(form)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  getList()
})
</script>

<style lang="scss" scoped>
.user {
  padding: 20px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);

  .el-card {
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
    border: 1px solid #e1f0ff;
    overflow: hidden;
    margin-bottom: 25px;
  }

  .toolbar {
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 25px;
    background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
    border-radius: 16px;
    border: 1px solid #e1f0ff;
    box-shadow: 0 4px 20px rgba(44, 90, 160, 0.08);

    .left {
      display: flex;
      gap: 12px;
    }

    h2 {
      margin: 0;
      font-size: 1.3rem;
      font-weight: 600;
      color: #2c5aa0;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    h2::before {
      content: '';
      width: 4px;
      height: 20px;
      background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
      border-radius: 2px;
    }

    .el-button--primary {
      background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
      border: none;
      border-radius: 20px;
      padding: 10px 20px;
      font-weight: 500;
    }

    .el-button--primary:hover {
      background: linear-gradient(135deg, #138d75 0%, #1e4d8c 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(22, 160, 133, 0.3);
    }
  }

  .search-form {
    margin-bottom: 25px;
    padding: 20px;
    background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
    border-radius: 12px;
    border: 1px solid #e1f0ff;
    
    :deep(.el-form-item) {
      margin-bottom: 18px;
      margin-right: 18px;
      
      .el-form-item__label {
        color: #2c5aa0;
        font-weight: 500;
      }
      
      .el-input {
        width: 200px;
      }
      
      .el-input__wrapper {
        border-radius: 10px;
        border: 2px solid #e1f0ff;
        background: #f8fbff;
        transition: all 0.3s ease;
      }

      .el-input__wrapper:hover {
        border-color: #16a085;
      }

      .el-input__wrapper.is-focus {
        border-color: #2c5aa0;
        box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
      }
      
      .form-select {
        width: 200px;
      }

      .form-select .el-input__wrapper {
        border-radius: 10px;
        border: 2px solid #e1f0ff;
        background: #f8fbff;
      }
    }

    .el-button {
      border-radius: 20px;
      padding: 8px 20px;
      font-weight: 500;
    }

    .el-button--primary {
      background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
      border: none;
    }

    .el-button--primary:hover {
      background: linear-gradient(135deg, #138d75 0%, #1e4d8c 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(22, 160, 133, 0.3);
    }
  }
}

:deep(.el-card__header) {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-bottom: 2px solid #e1f0ff;
  padding: 20px 25px;
}

:deep(.el-card__body) {
  padding: 25px;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(44, 90, 160, 0.08);
}

:deep(.el-table th) {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  color: #2c5aa0;
  font-weight: 600;
  border-color: #e1f0ff;
}

:deep(.el-table td) {
  border-color: #e1f0ff;
}

:deep(.el-table tr:hover > td) {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

:deep(.el-pagination__total),
:deep(.el-pagination__sizes),
:deep(.el-pagination__jump) {
  color: #5a6c7d;
}

:deep(.el-pager li) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  margin: 0 2px;
  border: 1px solid #e1f0ff;
}

:deep(.el-pager li:hover),
:deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  color: white;
  border-color: #16a085;
}

:deep(.btn-prev),
:deep(.btn-next) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  border: 1px solid #e1f0ff;
}

:deep(.btn-prev:hover),
:deep(.btn-next:hover) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  color: white;
}

:deep(.el-tag) {
  border-radius: 15px;
  font-weight: 500;
}

:deep(.el-tag--success) {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #16a085;
  border-color: #16a085;
}

:deep(.el-tag--danger) {
  background: linear-gradient(135deg, #fde8e8 0%, #fad2d2 100%);
  color: #e53e3e;
  border-color: #e53e3e;
}

:deep(.el-tag--info) {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #16a085;
  border-color: #16a085;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border: none;
  border-radius: 18px;
  font-weight: 500;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #138d75 0%, #1e4d8c 100%);
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  border: none;
  border-radius: 18px;
  font-weight: 500;
}

:deep(.el-button--warning:hover) {
  background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
}

:deep(.el-button--danger) {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  border: none;
  border-radius: 18px;
  font-weight: 500;
}

:deep(.el-button--danger:hover) {
  background: linear-gradient(135deg, #c53030 0%, #9c2626 100%);
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
  padding: 25px;
}

:deep(.el-form-item__label) {
  color: #2c5aa0;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  border: 2px solid #e1f0ff;
  background: #f8fbff;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #16a085;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

@media (max-width: 768px) {
  .user {
    padding: 15px;

    .toolbar {
      flex-direction: column;
      gap: 15px;
      align-items: flex-start;
      padding: 15px 20px;
    }

    .search-form {
      padding: 15px;

      :deep(.el-form-item) {
        margin-right: 0;
        width: 100%;

        .el-input,
        .form-select {
          width: 100%;
        }
      }
    }
  }
}
</style> 