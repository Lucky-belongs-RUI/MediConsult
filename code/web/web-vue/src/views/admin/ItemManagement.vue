<template>
  <div class="item-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>病例管理</span>
          <div class="header-actions">
            <el-button type="success" @click="openBatchImportDialog">
              <el-icon><Upload /></el-icon>
              批量导入
            </el-button>
            <el-button type="primary" @click="openAddDialog">
              添加病例
            </el-button>
          </div>
        </div>
      </template>

      <div class="search-area">
        <el-form :model="queryForm" inline>
          <el-form-item label="病例名称">
            <el-input v-model="queryForm.title" placeholder="输入病例名称" @keyup.enter="handleSearch" />
          </el-form-item>
          <el-form-item label="所属科室">
            <el-select
              v-model="queryForm.categoryId"
              placeholder="请选择科室"
              clearable
              :options="categoryOptions"
              @keyup.enter="handleSearch"
              style="width: 150px;"
            >
              <el-option 
                v-for="item in categoryOptions" 
                :key="item.value" 
                :label="item.label" 
                :value="item.value" 
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="症状标签">
            <el-input v-model="queryForm.tags" placeholder="输入症状标签关键词，多个标签用英文逗号分隔" @keyup.enter="handleSearch" />
          </el-form-item>
          <el-form-item label="主治医生">
            <el-input v-model="queryForm.userRealName" placeholder="输入主治医生姓名" @keyup.enter="handleSearch" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              搜索
            </el-button>
            <el-button class="ml-4" @click="resetSearch">
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        v-loading="loading"
        :data="tableData"
        border
        style="width: 100%"
      >
        <el-table-column prop="title" label="病例名称" width="150" />
        <el-table-column label="病例封面" width="150">
          <template #default="scope">
            <div v-if="scope.row.coverUrl" class="cover-preview">
              <el-image
                :src="scope.row.coverUrl"
                style="width: 60px; height: 60px; object-fit: cover"
                :preview-src-list="[scope.row.coverUrl]"
                :initial-index="0"
                fit="cover"
                class="cover-image"
                :hide-on-click-modal="false"
                preview-teleported
              />
            </div>
            <div v-else class="no-cover">
              <el-icon><Picture /></el-icon>
              <span>暂无封面</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="所属科室" width="150">
          <template #default="scope">
            {{ scope.row.category ? scope.row.category.name : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="主治医生" width="120">
          <template #default="scope">
            {{ scope.row.userRealName || '-' }}
          </template>
        </el-table-column>
                <el-table-column label="症状标签" width="220">
          <template #default="scope">
            <div class="tags-container">
              <el-tag
                v-for="tag in (scope.row.tags?.split(',').filter(Boolean) || [])"
                :key="tag"
                type="success"
                effect="light"
                round
                class="item-tag"
              >
                {{ tag }}
              </el-tag>
              <span
                v-if="!(scope.row.tags?.split(',').filter(Boolean)?.length)"
                class="no-tags"
              >
                暂无症状标签
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="病例描述" show-overflow-tooltip />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="220">
          <template #default="scope">
            <el-button type="info" size="small" @click="viewItemDetail(scope.row)">详情</el-button>
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.itemCount"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>

      <el-dialog
        v-model="showBatchImportDialog"
        title="批量导入病例"
        width="600px"
        :before-close="cancelBatchImportDialog"
      >
        <div class="batch-import-content">
          <el-alert
            title="批量导入说明"
            type="info"
            :closable="false"
            style="margin-bottom: 20px;"
          >
            <template #default>
              <div class="import-instructions">
                <p>请上传包含病例数据的ZIP压缩包文件，格式要求：</p>
                <ul>
                  <li><strong>只支持ZIP格式压缩包</strong>（不支持RAR、7Z等格式）</li>
                  <li>压缩包内必须包含一个 <code>data.json</code> 文件，存储病例数据</li>
                  <li>压缩包内可选包含 <code>images</code> 目录，存储封面图片</li>
                  <li>JSON文件中的图片路径需要与images目录中的文件名一致</li>
                  <li>支持的图片格式：jpg、jpeg、png、gif</li>
                  <li>单个图片不超过10MB，总压缩包不超过500MB</li>
                </ul>
              </div>
            </template>
          </el-alert>

          <el-upload
            ref="batchUploadRef"
            :http-request="handleBatchImport"
            :show-file-list="false"
            :before-upload="beforeBatchUpload"
            accept=".zip"
            drag
            class="batch-upload"
          >
            <div class="upload-content">
              <el-icon class="upload-icon"><UploadFilled /></el-icon>
              <div class="upload-text">
                <p>将ZIP压缩包拖到此处，或<em>点击上传</em></p>
                <p class="upload-tip">🗂️ 只支持ZIP格式 | 📄 必需data.json文件</p>
              </div>
            </div>
          </el-upload>

          <div v-if="batchImportProgress" class="import-progress">
            <el-progress :percentage="batchImportProgress" :status="batchImportStatus" />
            <p class="progress-text">{{ batchImportProgressText }}</p>
          </div>
        </div>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="cancelBatchImportDialog" :disabled="batchImportLoading">取消</el-button>
          </span>
        </template>
      </el-dialog>

      <el-dialog
        v-model="showDialog"
        :title="dialogType === 'add' ? '添加病例' : '编辑病例'"
        width="600px"
        :before-close="cancelDialog"
      >
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          class="item-form"
        >
          <el-form-item label="病例名称" prop="title">
            <el-input v-model="form.title" placeholder="请输入病例名称" />
          </el-form-item>
            

          <el-form-item label="所属科室" prop="categoryId">
            <el-select v-model="form.categoryId" placeholder="请选择所属科室" class="w-full">
              <el-option
                v-for="item in categoryOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>

                  
          <el-form-item label="主治医生" prop="userId">
            <el-select v-model="form.userId" placeholder="请选择主治医生" class="w-full">
              <el-option
                v-for="item in userOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>


          <el-form-item label="病例描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="4"
              placeholder="请输入病例描述"
            />
          </el-form-item>

          <el-form-item label="症状标签" prop="tags">
            <el-input v-model="form.tags" placeholder="请输入症状标签，使用逗号分隔" />
          </el-form-item>
          
          <el-form-item label="病例信息" prop="extraData">
            <div class="medical-info-form">
              <div class="form-section">
                <h4 class="section-title">患者基本信息</h4>
                <el-row :gutter="16">
                  <el-col :span="12">
                    <el-form-item label="性别">
                      <el-select v-model="medicalData.gender" placeholder="请选择性别">
                        <el-option label="男" value="男" />
                        <el-option label="女" value="女" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="年龄">
                      <el-input-number v-model="medicalData.age" :min="0" :max="120" placeholder="请输入年龄" />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item label="生命体征">
                  <el-input
                    v-model="medicalData.vitalSigns"
                    type="textarea"
                    :rows="2"
                    placeholder="请输入生命体征信息，如：血压120/80mmHg，心率72次/分，体温36.5℃等"
                  />
                </el-form-item>
              </div>

              <div class="form-section">
                <h4 class="section-title">症状与诊断</h4>
                <el-form-item label="症状描述">
                  <el-input
                    v-model="medicalData.symptoms"
                    type="textarea"
                    :rows="3"
                    placeholder="请详细描述患者症状，包括主诉、现病史等"
                  />
                </el-form-item>
                <el-form-item label="诊断结果">
                  <el-input
                    v-model="medicalData.diagnosis"
                    type="textarea"
                    :rows="2"
                    placeholder="请输入诊断结果"
                  />
                </el-form-item>
                <el-form-item label="严重程度">
                  <el-select v-model="medicalData.severity" placeholder="请选择严重程度">
                    <el-option label="轻度" value="轻度" />
                    <el-option label="中度" value="中度" />
                    <el-option label="中重度" value="中重度" />
                    <el-option label="重度" value="重度" />
                  </el-select>
                </el-form-item>
              </div>

              <div class="form-section">
                <h4 class="section-title">治疗方案</h4>
                <el-form-item label="用药方案">
                  <el-input
                    v-model="medicalData.medications"
                    type="textarea"
                    :rows="4"
                    placeholder="请详细描述用药方案，包括药物名称、剂量、用法用量、疗程等"
                  />
                </el-form-item>
                <el-form-item label="治疗方案">
                  <el-input
                    v-model="medicalData.treatment"
                    type="textarea"
                    :rows="3"
                    placeholder="请描述治疗方案，包括手术、理疗、康复等非药物治疗"
                  />
                </el-form-item>
              </div>

              <div class="form-section">
                <h4 class="section-title">注意事项与随访</h4>
                <el-form-item label="注意事项">
                  <el-input
                    v-model="medicalData.precautions"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入患者注意事项，包括饮食、生活方式、并发症预防等"
                  />
                </el-form-item>
                <el-form-item label="随访要求">
                  <el-input
                    v-model="medicalData.followUp"
                    type="textarea"
                    :rows="2"
                    placeholder="请输入随访要求，包括复查时间、复查项目等"
                  />
                </el-form-item>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="封面">
            <el-upload
              :http-request="customCoverRequest"
              class="upload-component"
              :show-file-list="false"
              :before-upload="beforeCoverUpload"
              accept="image/*"
            >
              <div v-if="coverPreviewUrl" class="preview-container">
                <div class="preview-image">
                  <img :src="coverPreviewUrl" alt="封面预览" />
                </div>
                <div class="preview-actions">
                  <el-button
                    type="primary"
                    size="small"
                    @click.stop="previewCover"
                  >
                    预览
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click.stop="removeUploadedCover"
                  >
                    删除
                  </el-button>
                </div>
              </div>
              <el-button v-else type="primary">上传封面</el-button>
            </el-upload>
          </el-form-item>

          <el-form-item label="文件">
            <el-upload
              :http-request="customFileRequest"
              class="upload-component"
              :show-file-list="false"
              :before-upload="beforeFileUpload"
            >
              <div v-if="uploadedFileName" class="uploaded-file">
                <el-icon><document /></el-icon>
                <span class="ml-2">{{ uploadedFileName }}</span>
                <div class="file-actions">
                  <el-button
                    type="danger"
                    size="small"
                    @click.stop="removeUploadedFile"
                  >
                    删除
                  </el-button>
                </div>
              </div>
              <el-button v-else type="primary">上传文件</el-button>
            </el-upload>
          </el-form-item>
        </el-form>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="cancelDialog">取消</el-button>
            <el-button type="primary" @click="submitForm">确定</el-button>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, UploadRequestOptions, UploadFile, UploadFiles } from 'element-plus'
import { itemApi } from '@/api/item'
import { categoryApi } from '@/api/category'
import { fileRequest } from '@/api/file_request'
import type { ItemVO, ItemAddDTO, ItemUpdateDTO, CategoryVO } from '@/types/item'
import { Picture, View, Edit, Delete, Document, UploadFilled, Upload } from '@element-plus/icons-vue'
import { userApi } from '@/api/user' 
import type { UserVO } from '@/types/user' 
const router = useRouter()

const loading = ref(false)
const submitLoading = ref(false)
const tableData = ref<ItemVO[]>([])
const showDialog = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance | null>(null)
const coverUploadRef = ref()
const fileUploadRef = ref()
const coverPreviewUrl = ref('')
const categories = ref<CategoryVO[]>([])
const uploadedFileName = ref('')
const users = ref<UserVO[]>([])
const showBatchImportDialog = ref(false)
const batchUploadRef = ref()
const batchImportLoading = ref(false)
const batchImportProgress = ref(0)
const batchImportStatus = ref<'success' | 'exception' | undefined>(undefined)
const batchImportProgressText = ref('')

const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0
})

const queryForm = ref({
  title: '',
  categoryId: undefined,
  tags: '',
  userRealName: '',
  current: 1,
  size: 10
})

const form = reactive<ItemAddDTO & { id?: number }>({
  title: '',
  description: '',
  coverObjectKey: '',
  coverBucket: '',
  fileObjectKey: '',
  fileBucket: '',
  tags: '',
  extraData: '',
  categoryId: undefined as unknown as number,
  userId: undefined as unknown as number
})

const rules = {
  title: [
    { required: true, message: '请输入病例名称', trigger: 'blur' }
  ],
  categoryId: [
    { required: true, message: '请选择所属科室', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入病例描述', trigger: 'blur' }
  ]
}

const categoryOptions = computed(() => {
  return categories.value.map((item: CategoryVO) => ({
    label: `[${item.id}] ${item.name}`,
    value: item.id
  }))
})

const userOptions = computed(() => {
  return users.value.map((item: UserVO) => ({
    label: `[${item.id}] ${item.realName}`,
    value: item.id
  }))
})

const fetchData = async () => {
  try {
    loading.value = true
    const params = {
      title: queryForm.value.title,
      categoryId: queryForm.value.categoryId,
      tag: queryForm.value.tags,
      userRealName: queryForm.value.userRealName,
      current: pagination.page,
      size: pagination.pageSize
    }
    const res = await itemApi.page(params)
    tableData.value = res.records || []
    pagination.itemCount = res.total || 0
  } catch (error) {
    console.error('获取病例列表失败', error)
    ElMessage.error('获取病例列表失败')
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const data = await categoryApi.list()
    categories.value = data
  } catch (error) {
    console.error('获取科室列表失败', error)
    ElMessage.error('获取科室列表失败')
  }
}
const fetchUsers = async () => {
  try {
    const data = await userApi.list()
    users.value = data
  } catch (error) {
    console.error('获取主治医生列表失败', error)
    ElMessage.error('获取主治医生列表失败')
  }
}
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const resetSearch = () => {
  queryForm.value.title = ''
  queryForm.value.categoryId = undefined
  queryForm.value.tags = ''
  queryForm.value.userRealName = ''
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

const openEditDialog = async (row: ItemVO) => {
  dialogType.value = 'edit'
  resetForm()
  form.id = row.id
  form.title = row.title
  form.description = row.description
  form.categoryId = row.category.id
  form.userId = row.userId
  
  form.tags = typeof row.tags === 'string' ? row.tags : ((row as any).tagList || []).join(',')
  coverPreviewUrl.value = row.coverUrl
  showDialog.value = true

  try {
    const data = await itemApi.getById(row.id)
    form.coverObjectKey = (data as any).coverObjectKey || ''
    form.coverBucket = (data as any).coverBucket || ''
    form.fileObjectKey = (data as any).fileObjectKey || ''
    form.fileBucket = (data as any).fileBucket || ''
    form.extraData = (data as any).extraData || ''

    if (form.extraData) {
      loadMedicalDataFromForm()
    }

    if (form.fileObjectKey) {
      const filename = form.fileObjectKey.split(/[\/\_]/).pop() || '';
      try {
        uploadedFileName.value = decodeURIComponent(filename);
      } catch (e) {
        uploadedFileName.value = filename;
      }
    }
  } catch (error) {
    console.error('获取病例详情失败', error)
    ElMessage.error('获取病例详情失败')
  }
}

const resetForm = () => {
  form.id = undefined
  form.title = ''
  form.description = ''
  form.coverObjectKey = ''
  form.coverBucket = ''
  form.fileObjectKey = ''
  form.fileBucket = ''
  form.tags = ''
  form.userId = undefined as unknown as number
  form.categoryId = undefined as unknown as number
  coverPreviewUrl.value = ''
  uploadedFileName.value = ''
  resetMedicalData()
}

const customCoverRequest = (options: UploadRequestOptions): Promise<any> => {
  if (!options.file) return Promise.reject(new Error('没有文件'))
  return new Promise((resolve, reject) => {
    uploadCover(options.file as File)
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

const customFileRequest = (options: UploadRequestOptions): Promise<any> => {
  if (!options.file) return Promise.reject(new Error('没有文件'))
  return new Promise((resolve, reject) => {
    uploadFile(options.file as File)
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

const uploadCover = async (file: File) => {
  try {
    submitLoading.value = true

    const isImage = /\.(jpg|jpeg|png|gif)$/i.test(file.name)
    if (!isImage) {
      ElMessage.error('只能上传jpg、png、gif格式的图片')
      return Promise.reject(new Error('文件格式不正确'))
    }

    const isLt2M = file.size / 1024 / 1024 < 2
    if (!isLt2M) {
      ElMessage.error('图片大小不能超过2MB')
      return Promise.reject(new Error('文件大小超过限制'))
    }

    const bucketName = 'item-cover'
    const res = await fileRequest.upload(bucketName, file, false)
    
    if (res) {
      form.coverObjectKey = res.objectKey || ''
      form.coverBucket = res.bucket || bucketName
      ElMessage.success('封面上传成功')

      coverPreviewUrl.value = URL.createObjectURL(file)
      return Promise.resolve(res)
    } else {
      ElMessage.warning('封面上传成功但返回数据格式有误')
      return Promise.reject(new Error('返回数据格式有误'))
    }
  } catch (error) {
    console.error('上传封面失败', error)
    ElMessage.error('上传封面失败')
    return Promise.reject(error)
  } finally {
    submitLoading.value = false
  }
}

const uploadFile = async (file: File) => {
  try {
    submitLoading.value = true

    uploadedFileName.value = file.name

    const bucketName = 'item-file'
    const res = await fileRequest.upload(bucketName, file, false)
    
    if (res) {
      form.fileObjectKey = res.objectKey || ''
      form.fileBucket = res.bucket || bucketName
      ElMessage.success('文件上传成功')
      return Promise.resolve(res)
    } else {
      ElMessage.warning('文件上传成功但返回数据格式有误')
      return Promise.reject(new Error('返回数据格式有误'))
    }
  } catch (error) {
    console.error('上传文件失败', error)
    ElMessage.error('上传文件失败')
    return Promise.reject(error)
  } finally {
    submitLoading.value = false
  }
}

const handleCoverUploadChange = (uploadFile: UploadFile, uploadFiles: UploadFiles) => {
  if (uploadFile.raw) {
    uploadCover(uploadFile.raw)
  }
}

const handleFileUploadChange = (uploadFileObj: UploadFile, uploadFiles: UploadFiles) => {
  if (uploadFileObj.raw) {
    const processFile = async (file: File) => {
      await uploadFile(file);
    };
    processFile(uploadFileObj.raw);
  }
}

const cancelDialog = () => {
  showDialog.value = false
  resetForm()
}

const beforeCoverUpload = (file: File) => {
  const isImage = /\.(jpg|jpeg|png|gif)$/i.test(file.name)
  if (!isImage) {
    ElMessage.error('只能上传jpg、png、gif格式的图片')
    return false
  }

  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB')
    return false
  }
  
  return true
}

const previewCover = () => {
  if (coverPreviewUrl.value) {
    window.open(coverPreviewUrl.value)
  }
}

const removeUploadedCover = async () => {
  try {
    if (form.coverBucket && form.coverObjectKey) {
      await fileRequest.delete(form.coverBucket, form.coverObjectKey)
    }
    form.coverObjectKey = ''
    form.coverBucket = ''
    coverPreviewUrl.value = ''
    ElMessage.success('封面已移除')
  } catch (error) {
    console.error('删除封面文件失败', error)
    ElMessage.error('删除封面文件失败，但本地记录已清除')
    form.coverObjectKey = ''
    form.coverBucket = ''
    coverPreviewUrl.value = ''
  }
}

const beforeFileUpload = (file: File) => {
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过10MB')
    return false
  }
  
  return true
}

const removeUploadedFile = async () => {
  try {
    if (form.fileBucket && form.fileObjectKey) {
      await fileRequest.delete(form.fileBucket, form.fileObjectKey)
    }
    form.fileObjectKey = ''
    form.fileBucket = ''
    uploadedFileName.value = ''
    ElMessage.success('文件已移除')
  } catch (error) {
    console.error('删除文件失败', error)
    ElMessage.error('删除文件失败，但本地记录已清除')
    form.fileObjectKey = ''
    form.fileBucket = ''
    uploadedFileName.value = ''
  }
}

const submitForm = () => {
  if (!formRef.value) return
  
  formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      submitLoading.value = true

      const medicalJson: Record<string, any> = {};
      if (medicalData.gender) medicalJson.gender = medicalData.gender;
      if (medicalData.age !== null && medicalData.age !== undefined) medicalJson.age = medicalData.age;
      if (medicalData.vitalSigns) medicalJson.vitalSigns = medicalData.vitalSigns;
      if (medicalData.symptoms) medicalJson.symptoms = medicalData.symptoms;
      if (medicalData.diagnosis) medicalJson.diagnosis = medicalData.diagnosis;
      if (medicalData.severity) medicalJson.severity = medicalData.severity;
      if (medicalData.medications) medicalJson.medications = medicalData.medications;
      if (medicalData.treatment) medicalJson.treatment = medicalData.treatment;
      if (medicalData.precautions) medicalJson.precautions = medicalData.precautions;
      if (medicalData.followUp) medicalJson.followUp = medicalData.followUp;

      const formData = { 
        ...form,
        extraData: JSON.stringify(medicalJson)
      }
      
      if (dialogType.value === 'add') {
        await itemApi.add({
          ...formData,
          tags: formData.tags,
          coverObjectKey: formData.coverObjectKey || '',
          coverBucket: formData.coverBucket || '',
          fileObjectKey: formData.fileObjectKey || '',
          fileBucket: formData.fileBucket || ''
        })
        ElMessage.success('添加成功')
      } else {
        const updateData: ItemUpdateDTO = {
          userId: formData.userId,
          id: formData.id!,
          title: formData.title,
          description: formData.description,
          tags: formData.tags,
          categoryId: formData.categoryId,
          extraData: formData.extraData || '',
          coverObjectKey: formData.coverObjectKey || '',
          coverBucket: formData.coverBucket || '',
          fileObjectKey: formData.fileObjectKey || '',
          fileBucket: formData.fileBucket || ''
        }
        await itemApi.update(updateData)
        ElMessage.success('更新成功')
      }
      
      showDialog.value = false
      fetchData()
    } catch (error) {
      console.error(dialogType.value === 'add' ? '添加失败' : '更新失败', error)
      ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该病例吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消', 
      type: 'warning'
    })
    
    await itemApi.delete(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
      ElMessage.error('删除失败')
    }
  }
}

const dialogTitle = computed(() => {
  return dialogType.value === 'add' ? '添加病例' : '编辑病例'
})

const viewItemDetail = (item: ItemVO) => {
  router.push({
    name: 'UserItemDetail',
    params: { id: item.id }
  })
}

const medicalData = reactive({
  gender: '',
  age: null as number | null,
  vitalSigns: '',
  symptoms: '',
  diagnosis: '',
  severity: '',
  medications: '',
  treatment: '',
  precautions: '',
  followUp: ''
})

const resetMedicalData = (showMessage = false) => {
  medicalData.gender = '';
  medicalData.age = null;
  medicalData.vitalSigns = '';
  medicalData.symptoms = '';
  medicalData.diagnosis = '';
  medicalData.severity = '';
  medicalData.medications = '';
  medicalData.treatment = '';
  medicalData.precautions = '';
  medicalData.followUp = '';
  if (showMessage) {
    ElMessage.success('医疗数据表单已重置');
  }
}

const loadMedicalDataFromForm = () => {
  try {
    if (!form.extraData || form.extraData.trim() === '') {
      resetMedicalData();
      return;
    }
    
    const jsonData = JSON.parse(form.extraData);

    medicalData.gender = jsonData.gender || '';
    medicalData.age = jsonData.age || null;
    medicalData.vitalSigns = jsonData.vitalSigns || '';
    medicalData.symptoms = jsonData.symptoms || '';
    medicalData.diagnosis = jsonData.diagnosis || '';
    medicalData.severity = jsonData.severity || '';
    medicalData.medications = jsonData.medications || '';
    medicalData.treatment = jsonData.treatment || '';
    medicalData.precautions = jsonData.precautions || '';
    medicalData.followUp = jsonData.followUp || '';
  } catch (error) {
    console.error('JSON解析失败', error);
    resetMedicalData();
  }
}

const openBatchImportDialog = () => {
  showBatchImportDialog.value = true
  batchImportProgress.value = 0
  batchImportStatus.value = undefined
  batchImportProgressText.value = ''
}

const cancelBatchImportDialog = () => {
  if (batchImportLoading.value) {
    ElMessageBox.confirm('正在导入中，确定要取消吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      showBatchImportDialog.value = false
      batchImportLoading.value = false
      batchImportProgress.value = 0
      batchImportStatus.value = undefined
      batchImportProgressText.value = ''
    }).catch(() => {})
  } else {
    showBatchImportDialog.value = false
    batchImportProgress.value = 0
    batchImportStatus.value = undefined
    batchImportProgressText.value = ''
  }
}

const beforeBatchUpload = (file: File) => {
  const isValidType = /\.zip$/i.test(file.name)
  if (!isValidType) {
    ElMessage.error('只支持ZIP格式的压缩包文件')
    return false
  }

  const isLt500M = file.size / 1024 / 1024 < 500
  if (!isLt500M) {
    ElMessage.error('压缩包大小不能超过500MB')
    return false
  }

  return true
}

const handleBatchImport = async (options: any) => {
  try {
    batchImportLoading.value = true
    batchImportProgress.value = 10
    batchImportProgressText.value = '正在上传文件...'
    
    const file = options.file as File
    const result = await itemApi.batchImport(file)
    
    batchImportProgress.value = 100
    batchImportStatus.value = 'success'
    batchImportProgressText.value = `导入完成！成功：${result.successCount} 个，失败：${result.failureCount} 个`
    
    if (result.failureCount > 0 && result.errors && result.errors.length > 0) {
      ElMessageBox.alert(
        result.errors.join('\n'),
        '导入错误详情',
        {
          confirmButtonText: '确定',
          type: 'warning',
          customClass: 'import-error-dialog'
        }
      )
    } else {
      ElMessage.success(`批量导入成功！共导入 ${result.successCount} 个病例`)
    }

    await fetchData()

    setTimeout(() => {
      showBatchImportDialog.value = false
      batchImportProgress.value = 0
      batchImportStatus.value = undefined
      batchImportProgressText.value = ''
    }, 2000)
    
  } catch (error) {
    console.error('批量导入失败', error)
    batchImportProgress.value = 100
    batchImportStatus.value = 'exception'
    batchImportProgressText.value = '导入失败，请检查ZIP文件格式'
    ElMessage.error('批量导入失败，请检查ZIP文件格式和数据内容')
  } finally {
    batchImportLoading.value = false
  }
}

onMounted(() => {
  fetchData()
  fetchCategories()
  fetchUsers()
})
</script>

<style scoped>
.item-management {
  width: 100%;
  position: relative;
  z-index: 1;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-area {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.preview-image {
  width: 100%;
  max-width: 200px;
  height: 150px;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 10px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.preview-image img:hover {
  transform: scale(1.05);
}

.preview-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 5px;
}

.ml-4 {
  margin-left: 16px;
}

.mt-2 {
  margin-top: 8px;
}

.mt-4 {
  margin-top: 16px;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.file-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.file-uploader .el-upload:hover {
  border-color: #409EFF;
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

.cover-preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-image {
  border-radius: 4px;
  transition: transform 0.3s;
  cursor: pointer;
}

.cover-image:hover {
  transform: scale(1.05);
}

.no-cover {
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

.no-cover .el-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 4px 0;
}

.item-tag {
  margin-right: 0;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-tags {
  color: #909399;
  font-size: 13px;
}

.form-tips {
  margin-top: 4px;
  color: #909399;
  font-size: 12px;
}

.upload-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.cover-uploader {
  width: 240px;
  height: 240px;
}

.cover-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 240px;
  height: 240px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-uploader :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.cover-uploader :deep(.el-upload-dragger) {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0;
  border: none;
}

.cover-preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
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

.file-uploader {
  width: 360px;
}

.file-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 360px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100px;
}

.file-uploader :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.file-uploader :deep(.el-upload-dragger) {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0;
  border: none;
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

.file-info-container {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 16px;
}

.file-icon {
  font-size: 32px;
  color: #409EFF;
  margin-right: 16px;
}

.file-info {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-size: 16px;
  color: #303133;
  margin-bottom: 4px;
  font-weight: 500;
  word-break: break-all;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
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



.medical-info-form {
  width: 100%;
}

.form-section {
  margin-bottom: 24px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  background-color: #fafafa;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  border-bottom: 2px solid #409eff;
  padding-bottom: 8px;
}

.form-actions {
  margin-top: 20px;
  text-align: center;
}

.form-actions .el-button {
  margin: 0 8px;
}

.batch-import-content {
  padding: 20px 0;
}

.import-instructions p {
  margin: 10px 0;
  font-size: 14px;
  color: #606266;
}

.import-instructions ul {
  margin: 10px 0;
  padding-left: 20px;
}

.import-instructions li {
  margin: 5px 0;
  font-size: 13px;
  color: #909399;
  line-height: 1.5;
}

.import-instructions code {
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  color: #e6a23c;
}

.batch-upload {
  margin: 20px 0;
}

.batch-upload :deep(.el-upload) {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 100%;
  height: 160px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.batch-upload :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.batch-upload :deep(.el-upload.is-dragover) {
  border-color: #409EFF;
  background-color: rgba(64, 158, 255, 0.06);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
}

.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.upload-text p {
  font-size: 16px;
  color: #606266;
  margin: 8px 0;
}

.upload-text em {
  color: #409EFF;
  font-style: normal;
}

.upload-tip {
  font-size: 12px;
  color: #909399 !important;
}

.import-progress {
  margin-top: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 6px;
}

.progress-text {
  margin-top: 10px;
  text-align: center;
  font-size: 14px;
  color: #606266;
}

:deep(.import-error-dialog) {
  max-height: 400px;
  overflow-y: auto;
}

:deep(.import-error-dialog .el-message-box__message) {
  white-space: pre-line;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
}
</style> 