<template>
  <div class="category-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">科室管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon> 添加科室
          </el-button>
        </div>
      </template>

      <div class="search-area">
        <el-form :model="queryForm" inline @submit.prevent="handleSearch">
          <el-form-item label="科室名称">
            <el-input 
              v-model="queryForm.name" 
              placeholder="输入科室名称" 
              clearable
              @keyup.enter.prevent="handleSearch"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon> 搜索
            </el-button>
            <el-button @click="resetSearch" class="ml-4">
              <el-icon><RefreshRight /></el-icon> 重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        v-loading="loading"
        :data="tableData"
        border
        stripe
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column prop="id" label="科室ID" width="80" align="center" />
        <el-table-column prop="name" label="科室名称" width="150" show-overflow-tooltip />
        <el-table-column label="科室图标" width="120" align="center">
          <template #default="scope">
            <div v-if="scope.row.iconUrl" class="icon-preview">
              <el-image
                :src="scope.row.iconUrl"
                style="width: 60px; height: 60px; object-fit: cover"
                :preview-src-list="[scope.row.iconUrl]"
                :initial-index="0"
                fit="cover"
                loading="lazy"
                class="icon-image"
                :hide-on-click-modal="false"
                preview-teleported
              />
            </div>
            <div v-else class="no-icon">
              <el-icon><Picture/></el-icon>
              <span>暂无图标</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="科室描述" min-width="100" show-overflow-tooltip />
        <el-table-column prop="createTime" label="创建时间" width="180" show-overflow-tooltip />
        <el-table-column label="操作" width="400" align="center" fixed="right">
          <template #default="scope">
            <el-button type="info" size="small" @click="viewCategoryDetail(scope.row)" plain>
              <el-icon><View /></el-icon> 详情
            </el-button>
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)" plain>
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)" plain>
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && tableData.length === 0" description="暂无数据" />

      <div class="pagination-container" v-if="pagination.itemCount > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.itemCount"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
          background
        />
      </div>

      <el-dialog 
        v-model="showDialog" 
        :title="dialogTitle" 
        width="600px"
        destroy-on-close
        @closed="resetForm"
      >
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          status-icon
        >
          <el-form-item label="科室名称" prop="name">
            <el-input 
              v-model="form.name" 
              placeholder="请输入科室名称" 
              maxlength="50"
              show-word-limit
            />
          </el-form-item>
          <el-form-item label="科室图标" prop="iconObjectKey">
            <div class="upload-container">
              <el-upload
                ref="uploadRef"
                class="icon-uploader"
                :http-request="customRequest"
                :show-file-list="false"
                accept="image/*"
                action="#"
                :auto-upload="true"
                :limit="1"
                drag
              >
                <div v-if="previewUrl" class="preview-wrapper">
                  <img :src="previewUrl" class="preview-image" />
                  <div class="preview-mask">
                    <el-icon class="preview-icon"><Edit /></el-icon>
                  </div>
                </div>
                <template v-else>
                  <el-icon class="upload-icon"><UploadFilled /></el-icon>
                  <div class="upload-text">拖拽图片到此处或<em>点击上传</em></div>
                </template>
              </el-upload>
              <div class="upload-actions" v-if="previewUrl">
                <el-button type="danger" size="small" @click="handleRemoveIcon" plain>
                  <el-icon><Delete /></el-icon> 删除图标
                </el-button>
              </div>
              <div class="upload-tip">
                <el-text type="info" size="small">推荐尺寸: 200x200px，支持jpg、png、gif格式，不超过10MB</el-text>
                <br />
                <el-text type="info" size="small">科室图标为可选项</el-text>
              </div>
            </div>
          </el-form-item>
          <el-form-item label="科室描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              placeholder="请输入科室描述"
              :rows="4"
              maxlength="255"
              show-word-limit
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showDialog = false">取消</el-button>
            <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
              确认
            </el-button>
          </span>
        </template>
      </el-dialog>

      <el-dialog
        v-model="showDeleteDialog"
        title="删除确认"
        width="400px"
        destroy-on-close
      >
        <div class="delete-confirm-content">
          <el-icon class="warning-icon"><WarningFilled /></el-icon>
          <div class="delete-confirm-text">
            <p class="delete-title">确定要删除该科室吗？</p>
            <p class="delete-desc">科室ID: {{ deleteItem?.id }}</p>
            <p class="delete-desc">科室名称: {{ deleteItem?.name }}</p>
            <p class="delete-warning">注意：如果该科室下有关联的病例，将无法删除。</p>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showDeleteDialog = false">取消</el-button>
            <el-button type="danger" @click="confirmDelete" :loading="deleteLoading">
              确认删除
            </el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>

    <div class="image-viewer-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, UploadRequestOptions } from 'element-plus'
import { categoryApi } from '@/api/category'
import { fileRequest } from '@/api/file_request'
import type { CategoryVO, CategoryAddDTO, CategoryUpdateDTO, CategoryQueryDTO } from '@/types/item'
import { 
  Plus, 
  Edit, 
  Delete, 
  Search, 
  RefreshRight, 
  Picture,
  View, 
  WarningFilled,
  UploadFilled
} from '@element-plus/icons-vue'

const router = useRouter()

const loading = ref(false)
const submitLoading = ref(false)
const deleteLoading = ref(false)
const tableData = ref<CategoryVO[]>([])
const showDialog = ref(false)
const showDeleteDialog = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance | null>(null)
const uploadRef = ref()
const previewUrl = ref('')
const deleteItem = ref<CategoryVO | null>(null)

const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0
})

const queryForm = reactive<CategoryQueryDTO>({
  name: '',
  current: 1,
  size: 10
})

const form = reactive<CategoryAddDTO & { id?: number }>({
  name: '',
  iconObjectKey: '',
  iconBucket: '',
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入科室名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度应为2-50个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入科室描述', trigger: 'blur' },
    { max: 255, message: '长度不能超过255个字符', trigger: 'blur' }
  ]
}

const fetchData = async () => {
  try {
    loading.value = true
    queryForm.current = pagination.page
    queryForm.size = pagination.pageSize
    const res = await categoryApi.page(queryForm)
    tableData.value = res.records || []
    pagination.itemCount = res.total || 0
  } catch (error) {
    console.error('获取科室列表失败', error)
    ElMessage.error('获取科室列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const resetSearch = () => {
  queryForm.name = ''
  pagination.page = 1
  fetchData()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchData()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchData()
}

const openAddDialog = () => {
  dialogType.value = 'add'
  resetForm()
  showDialog.value = true
}

const openEditDialog = async (row: CategoryVO) => {
  dialogType.value = 'edit'
  resetForm()
  form.id = row.id
  form.name = row.name
  form.description = row.description
  previewUrl.value = row.iconUrl || ''
  showDialog.value = true

  try {
    const res = await categoryApi.getById(row.id)
    if (res) {
      form.iconObjectKey = res.iconObjectKey || ''
      form.iconBucket = res.iconBucket || ''
    }
  } catch (error) {
    console.error('获取科室详情失败', error)
    ElMessage.error('获取科室详情失败')
  }
}

const resetForm = () => {
  form.id = undefined
  form.name = ''
  form.iconObjectKey = ''
  form.iconBucket = ''
  form.description = ''
  previewUrl.value = ''
}

const customRequest = (options: UploadRequestOptions): Promise<any> => {
  if (!options.file) return Promise.reject(new Error('没有文件'))
  return new Promise((resolve, reject) => {
    uploadIcon(options.file as File)
      .then(res => {
        if (options.onSuccess) {
          options.onSuccess(res)
        }
        resolve(res)
      })
      .catch(err => {
        if (options.onError) {
          options.onError(err)
        }
        reject(err)
      })
  })
}

const uploadIcon = async (file: File) => {
  try {
    submitLoading.value = true

    const isImage = /\.(jpg|jpeg|png|gif)$/i.test(file.name)
    if (!isImage) {
      ElMessage.error('只能上传jpg、png、gif格式的图片')
      return Promise.reject(new Error('文件格式不正确'))
    }

      const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB')
      return Promise.reject(new Error('文件大小超过限制'))
    }

    previewUrl.value = URL.createObjectURL(file)
    
    const bucketName = 'category-icon'
    const res = await fileRequest.upload(bucketName, file, false)
    
    if (res) {
      form.iconObjectKey = res.objectKey || ''
      form.iconBucket = res.bucket || bucketName
      ElMessage.success('图标上传成功')
      return Promise.resolve(res)
    } else {
      ElMessage.warning('上传成功但返回数据格式有误')
      return Promise.reject(new Error('返回数据格式有误'))
    }
  } catch (error) {
    console.error('上传图标失败', error)
    ElMessage.error('上传图标失败')
    previewUrl.value = ''
    return Promise.reject(error)
  } finally {
    submitLoading.value = false
  }
}

const handleSubmit = () => {
  if (!formRef.value) return
  
  formRef.value.validate(async (valid, fields) => {
    if (!valid) {
      console.log('表单验证失败:', fields)
      return
    }
    
    try {
      submitLoading.value = true
      
      if (dialogType.value === 'add') {
        const categoryData = {
          name: form.name,
          description: form.description,
          iconBucket: form.iconBucket || '',
          iconObjectKey: form.iconObjectKey || ''
        }
        
        await categoryApi.add(categoryData)
        ElMessage.success('添加科室成功')
      } else {
        const updateData: CategoryUpdateDTO = {
          id: form.id!,
          name: form.name,
          description: form.description,
          iconObjectKey: form.iconObjectKey || '',
          iconBucket: form.iconBucket || ''
        }
        await categoryApi.update(updateData)
        ElMessage.success('更新科室成功')
      }
      
      showDialog.value = false
      fetchData()
    } catch (error) {
      console.error(dialogType.value === 'add' ? '添加科室失败' : '更新科室失败', error)
      ElMessage.error(dialogType.value === 'add' ? '添加科室失败' : '更新科室失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDelete = (row: CategoryVO) => {
  deleteItem.value = row
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!deleteItem.value) return
  
  try {
    deleteLoading.value = true
    await categoryApi.delete(deleteItem.value.id)
    ElMessage.success('删除科室成功')
    showDeleteDialog.value = false
    fetchData()
  } catch (error: any) {
    console.error('删除科室失败', error)

    if (error.response && error.response.data && error.response.data.msg) {
      ElMessage.error(error.response.data.msg)
    } else {
      ElMessage.error('删除科室失败，请稍后重试')
    }
  } finally {
    deleteLoading.value = false
  }
}

const dialogTitle = computed(() => {
  return dialogType.value === 'add' ? '添加科室' : '编辑科室'
})

const viewCategoryDetail = (category: CategoryVO) => {
  router.push({
    name: 'UserCategoryDetail',
    params: { id: category.id }
  })
}

const handleRemoveIcon = async () => {
  try {
    if (form.iconBucket && form.iconObjectKey) {
      await fileRequest.delete(form.iconBucket, form.iconObjectKey)
      ElMessage.success('图标文件已从服务器删除')
    }
    form.iconObjectKey = ''
    form.iconBucket = ''
    previewUrl.value = ''
    ElMessage.success('图标已移除')
  } catch (error) {
    console.error('删除图标文件失败', error)
    ElMessage.error('删除图标文件失败，但本地记录已清除')
    form.iconObjectKey = ''
    form.iconBucket = ''
    previewUrl.value = ''
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.category-management {
  width: 100%;
  position: relative;
  z-index: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.search-area {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.icon-preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon-image {
  border-radius: 4px;
  transition: transform 0.3s;
  cursor: pointer;
}

.icon-image:hover {
  transform: scale(1.05);
}

.no-icon {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #909399;
  font-size: 12px;
  margin: 0 auto;
}

.no-icon .el-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.upload-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.icon-uploader {
  width: 200px;
  height: 200px;
}

.icon-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon-uploader :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.icon-uploader :deep(.el-upload-dragger) {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0;
  border: none;
}

.preview-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.preview-wrapper:hover .preview-mask {
  opacity: 1;
}

.preview-icon {
  color: #fff;
  font-size: 28px;
}

.upload-icon {
  font-size: 32px;
  color: #c0c4cc;
  margin-bottom: 8px;
}

.upload-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  text-align: center;
  padding: 0 20px;
}

.upload-text em {
  color: #409EFF;
  font-style: normal;
}

.upload-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-start;
}

.upload-tip {
  margin-top: 12px;
  line-height: 1.5;
  color: #909399;
}

.ml-4 {
  margin-left: 16px;
}

.delete-confirm-content {
  display: flex;
  align-items: flex-start;
  padding: 10px 0;
}

.warning-icon {
  font-size: 28px;
  color: #f56c6c;
  margin-right: 16px;
  margin-top: 4px;
}

.delete-confirm-text {
  flex: 1;
}

.delete-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
}

.delete-desc {
  margin-bottom: 8px;
  color: #606266;
}

.delete-warning {
  color: #f56c6c;
  font-size: 14px;
}

:deep(.el-image-viewer__mask) {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  opacity: 0.5;
  background: #000;
  z-index: 2010;
}

:deep(.el-image-viewer__wrapper) {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 2011;
}

:deep(.el-image-viewer__close) {
  z-index: 2012;
}

:deep(.el-image-viewer__canvas) {
  z-index: 2011;
}

:deep(.el-image-viewer__actions) {
  z-index: 2012;
}

:deep(.el-image-viewer__prev), 
:deep(.el-image-viewer__next) {
  z-index: 2012;
}

:deep(.el-image-viewer__btn) {
  z-index: 2012;
}

.image-viewer-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  z-index: 2009;
  pointer-events: none;
}
</style> 