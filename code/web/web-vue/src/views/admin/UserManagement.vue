<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button
            type="primary"
            @click="handleAdd"
          >
            添加用户
          </el-button>
        </div>
      </template>

      <el-form
        :model="searchForm"
        inline
        class="search-form"
        id="searchForm"
      >
        <el-form-item label="用户名">
          <el-input
            v-model="searchForm.username"
            placeholder="请输入用户名"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input
            v-model="searchForm.realName"
            placeholder="请输入真实姓名"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="角色">
          <el-select
            v-model="searchForm.role"
            placeholder="请选择角色"
            clearable
            style="width: 140px"
            popper-class="role-select-dropdown"
            id="searchRoleSelect"
          >
            <el-option
              v-for="item in roleOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 140px"
            popper-class="status-select-dropdown"
            id="searchStatusSelect"
          >
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleSearch"
          >
            搜索
          </el-button>
          <el-button @click="handleReset">
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <el-table
        v-loading="loading"
        :data="tableData"
        style="width: 100%"
      >
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="realName" label="真实姓名" min-width="120" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 1 ? 'danger' : 'info'">
              {{ row.role === 1 ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleResetPassword(row)"
            >
              重置密码
            </el-button>
            <el-button
              :type="row.status === 1 ? 'danger' : 'success'"
              link
              @click="handleToggleStatus(row)"
            >
              {{ row.status === 1 ? '禁用' : '启用' }}
            </el-button>
            <el-button
              v-if="row.role !== 1"
              type="danger"
              link
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="100px"
        id="userForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            :disabled="dialogType === 'edit'"
            placeholder="请输入用户名"
          />
        </el-form-item>
        <el-form-item
          v-if="dialogType === 'add'"
          label="密码"
          prop="password"
        >
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
          />
        </el-form-item>
        <el-form-item label="真实姓名" prop="realName">
          <el-input
            v-model="form.realName"
            placeholder="请输入真实姓名"
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="form.phone"
            placeholder="请输入手机号"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select
            v-model="form.role"
            placeholder="请选择角色"
            style="width: 140px"
            popper-class="role-select-dropdown"
            id="formRoleSelect"
          >
            <el-option
              v-for="item in roleOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="resetPasswordVisible"
      title="重置密码"
      width="400px"
      id="resetPasswordDialog"
    >
      <div class="reset-password-content">
        <p>确定要重置该用户的密码吗？</p>
        <p class="warning-text">重置后密码将变为：123456</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetPasswordVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="resetPasswordLoading"
            @click="handleResetPasswordSubmit"
          >
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance, FormItemRule } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UserInfo } from '@/types/user'
import {
  getUserList,
  addUser,
  updateUser,
  deleteUser,
  resetPassword,
  updateUserStatus
} from '@/api/user'

const searchForm = ref({
  username: '',
  realName: '',
  role: undefined as number | undefined,
  status: undefined as number | undefined
})

const roleOptions = [
  { label: '管理员', value: 1 },
  { label: '普通用户', value: 0 }
]

const statusOptions = [
  { label: '正常', value: 1 },
  { label: '禁用', value: 0 }
]

const tableData = ref<UserInfo[]>([])
const loading = ref(false)

const pagination = ref({
  current: 1,
  size: 10,
  total: 0
})

const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const submitLoading = ref(false)
const formRef = ref<FormInstance>()

const form = ref({
  id: undefined as number | undefined,
  username: '',
  password: '',
  realName: '',
  phone: '',
  email: '',
  role: 0
})

const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
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
    { pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
} as const satisfies Record<string, FormItemRule[]>

const resetPasswordVisible = ref(false)
const resetPasswordLoading = ref(false)
const currentUserId = ref<number>()

const loadData = async () => {
  try {
    loading.value = true
    const params = {
      current: pagination.value.current,
      size: pagination.value.size,
      ...searchForm.value
    }

    const res = await getUserList(params)
    tableData.value = res.records
    pagination.value.total = res.total
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.current = 1
  loadData()
}

const handleReset = () => {
  searchForm.value = {
    username: '',
    realName: '',
    role: undefined,
    status: undefined
  }
  handleSearch()
}

const handleCurrentChange = (current: number) => {
  pagination.value.current = current
  loadData()
}

const handleSizeChange = (size: number) => {
  pagination.value.size = size
  pagination.value.current = 1
  loadData()
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    id: undefined,
    username: '',
    password: '',
    realName: '',
    phone: '',
    email: '',
    role: 0
  }
  dialogVisible.value = true
}

const handleEdit = (row: UserInfo) => {
  dialogType.value = 'edit'
  form.value = {
    id: row.id,
    username: row.username,
    password: '',
    realName: row.realName || '',
    phone: row.phone || '',
    email: row.email || '',
    role: row.role
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitLoading.value = true

    if (dialogType.value === 'add') {
      await addUser(form.value)
      ElMessage.success('添加成功')
    } else {
      await updateUser(form.value)
      ElMessage.success('更新成功')
    }

    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitLoading.value = false
  }
}

const handleResetPassword = (row: UserInfo) => {
  currentUserId.value = row.id
  resetPasswordVisible.value = true
}

const handleResetPasswordSubmit = async () => {
  if (!currentUserId.value) return

  try {
    resetPasswordLoading.value = true
    await resetPassword(currentUserId.value)
    ElMessage.success('密码已重置为：123456')
    resetPasswordVisible.value = false
  } catch (error) {
    console.error('重置密码失败:', error)
  } finally {
    resetPasswordLoading.value = false
  }
}

const handleToggleStatus = async (row: UserInfo) => {
  try {
    await ElMessageBox.confirm(
      `确定要${row.status === 1 ? '禁用' : '启用'}该用户吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await updateUserStatus({
      id: row.id,
      status: row.status === 1 ? 0 : 1
    })

    ElMessage.success(`${row.status === 1 ? '禁用' : '启用'}成功`)
    loadData()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row: UserInfo) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该用户吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteUser(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    console.error('删除失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.reset-password-content {
  text-align: center;
  padding: 20px 0;
}

.warning-text {
  color: #E6A23C;
  font-weight: bold;
  margin-top: 10px;
}

:deep(.el-form--inline .el-form-item) {
  margin-right: 16px;
}
</style>

<style>
.role-select-dropdown {
  min-width: 140px !important;
}

.status-select-dropdown {
  min-width: 140px !important;
}
</style> 