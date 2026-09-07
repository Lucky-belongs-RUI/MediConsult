<template>
  <div class="rag-management">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <el-icon><Search /></el-icon>
          <span>RAG技术-智能检索数据管理</span>
        </div>
      </template>
      
      <div class="index-info">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <div class="info-label">索引状态</div>
              <div class="info-value">
                <el-tag :type="vectorIndex.exists ? 'success' : 'danger'" size="large">
                  {{ vectorIndex.exists ? '已创建' : '未创建' }}
                </el-tag>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <div class="info-label">病例数量</div>
              <div class="info-value">{{ vectorIndex.count }} 个</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <div class="info-label">索引大小</div>
              <div class="info-value">{{ formatBytes(vectorIndex.size) }}</div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <div class="actions-section">
        <h3 class="section-title">索引操作</h3>
        <div class="button-group">
          <div class="button-item">
            <el-button 
              type="primary" 
              :loading="updating" 
              @click="updateVectorIndex"
              :icon="Refresh"
              size="large"
            >
              {{ updating ? '更新中...' : '更新索引' }}
            </el-button>
            <div class="button-desc">
              先删除旧索引再创建新索引，用于同步最新数据
            </div>
          </div>
          
          <div class="button-item">
            <el-button 
              type="success" 
              :loading="creating" 
              @click="createVectorIndex"
              :icon="Plus"
              :disabled="vectorIndex.exists"
              size="large"
            >
              {{ creating ? '创建中...' : '创建索引' }}
            </el-button>
            <div class="button-desc">
              为所有病例创建向量索引，启用语义检索功能
            </div>
          </div>
          
          <div class="button-item">
            <el-button 
              type="danger" 
              :loading="deleting" 
              @click="deleteVectorIndex"
              :icon="Delete"
              :disabled="!vectorIndex.exists"
              size="large"
            >
              {{ deleting ? '删除中...' : '删除索引' }}
            </el-button>
            <div class="button-desc">
              删除现有向量索引，删除后将无法使用语义检索
            </div>
          </div>
        </div>
      </div>
      
      <div class="actions-section kg-section">
        <h3 class="section-title">知识图谱管理</h3>
        
        <div class="kg-status">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <div class="info-label">知识图谱状态</div>
                <div class="info-value">
                  <el-tag :type="knowledgeGraph.exists ? 'success' : 'warning'" size="large">
                    {{ knowledgeGraph.exists ? '已构建' : '未构建' }}
                  </el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <div class="info-label">知识类别</div>
                <div class="info-value">{{ knowledgeGraph.disease_count }} 个</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <div class="info-label">三元组数量</div>
                <div class="info-value">{{ knowledgeGraph.triple_count }} 个</div>
              </div>
            </el-col>
          </el-row>
        </div>
        
        <div class="upload-section">
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            :auto-upload="false"
            :limit="1"
            accept=".xlsx,.xls"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
          >
            <el-button type="primary" :icon="Upload">
              选择Excel文件
            </el-button>
            <template #tip>
              <div class="upload-tip">
                仅支持 .xlsx, .xls 格式文件，每行数据将调用LLM提取三元组
              </div>
            </template>
          </el-upload>
          
          <div class="selected-file" v-if="selectedFile">
            <el-tag type="info">
              已选择: {{ selectedFile.name }}
            </el-tag>
          </div>
        </div>
        
        <div class="button-group">
          <div class="button-item">
            <el-button 
              type="warning" 
              :loading="kgBuilding" 
              @click="buildKnowledgeGraph"
              :icon="Link"
              :disabled="!selectedFile"
              size="large"
            >
              {{ kgBuilding ? '构建中...' : '构建知识图谱' }}
            </el-button>
            <div class="button-desc">
              上传Excel文件后构建知识图谱，逐行调用LLM提取三元组
            </div>
          </div>
          
          <div class="button-item">
            <el-button 
              type="danger" 
              :loading="kgDeleting" 
              @click="deleteKnowledgeGraph"
              :icon="Delete"
              :disabled="!knowledgeGraph.exists"
              size="large"
            >
              {{ kgDeleting ? '删除中...' : '删除知识图谱' }}
            </el-button>
            <div class="button-desc">
              删除现有知识图谱，删除后将无法使用知识图谱检索
            </div>
          </div>
        </div>
      </div>
      
      <div class="refresh-section">
        <h3 class="section-title">状态刷新</h3>
        <div class="button-group">
          <div class="button-item">
            <el-button 
              type="info" 
              @click="refreshIndexStatus"
              :icon="Refresh"
              size="large"
            >
              刷新状态
            </el-button>
            <div class="button-desc">
              重新获取当前索引的创建状态和统计信息
            </div>
          </div>
          
          <div class="button-item">
            <el-button 
              type="warning" 
              @click="refreshAllStats"
              :icon="Refresh"
              size="large"
            >
              刷新统计
            </el-button>
            <div class="button-desc">
              重新加载系统统计数据，更新页面显示内容
            </div>
          </div>
        </div>
      </div>
      
      <div class="description-section">
        <h3 class="section-title">功能说明</h3>
        <el-alert
          title="RAG向量索引技术说明"
          type="info"
          :closable="false"
          show-icon
        >
          <div class="description-content">
            <p><strong>什么是RAG技术？</strong></p>
            <p>RAG（Retrieval-Augmented Generation）即检索增强生成，是一种结合向量检索与生成式AI的技术，能够实现基于语义的理解和问答。</p>
            
            <p><strong>向量索引的作用：</strong></p>
            <ul>
              <li>将病例数据转换为向量形式存储，支持语义相似度检索</li>
              <li>用户可以通过自然语言描述症状、诊断或治疗方案来查找相关病例</li>
              <li>提高检索的准确性和用户体验</li>
            </ul>
            
            <p><strong>知识图谱的作用：</strong></p>
            <ul>
              <li>从医学知识文件中提取知识三元组</li>
              <li>按文件名作为知识类别</li>
              <li>问答时结合知识图谱提供更专业的医学建议</li>
            </ul>
            
            <p><strong>使用建议：</strong></p>
            <ul>
              <li>在新增或修改病例数据后，建议执行"更新索引"操作</li>
              <li>索引创建过程可能需要几分钟时间，请耐心等待</li>
              <li>如果不需要语义检索功能，可以删除索引以节省存储空间</li>
            </ul>
          </div>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Search, Refresh, Plus, Delete, Upload, Link } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { vectorIndexApi, knowledgeGraphApi, type VectorIndexInfo, type KnowledgeGraphInfo } from '@/api/vector'
import { itemApi } from '@/api/item'
import { categoryApi } from '@/api/category'
import { getUserList } from '@/api/user'

const vectorIndex = ref<VectorIndexInfo>({
  exists: false,
  count: 0,
  size: 0
})

const knowledgeGraph = ref<KnowledgeGraphInfo>({
  exists: false,
  disease_count: 0,
  triple_count: 0
})

const updating = ref(false)
const creating = ref(false)
const deleting = ref(false)

const kgBuilding = ref(false)
const kgDeleting = ref(false)

const uploadRef = ref()
const selectedFile = ref<File | null>(null)

const userCount = ref(0)
const caseCount = ref(0)
const categoryCount = ref(0)

const formatBytes = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getVectorIndexStatus = async () => {
  try {
    const result = await vectorIndexApi.getStatus()
    vectorIndex.value = result
  } catch (error) {
    console.error('获取向量索引状态失败:', error)
  }
}

const getKnowledgeGraphStatus = async () => {
  try {
    const result = await knowledgeGraphApi.getStatus()
    knowledgeGraph.value = result
  } catch (error) {
    console.error('获取知识图谱状态失败:', error)
  }
}

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

const buildKnowledgeGraph = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择Excel文件')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      '构建知识图谱将逐行调用LLM提取三元组，此过程可能需要较长时间，是否继续？',
      '确认构建',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    kgBuilding.value = true
    
    const uploadResult = await knowledgeGraphApi.uploadFile(selectedFile.value)
    
    await knowledgeGraphApi.build(uploadResult.relative_path)
    
    ElMessage.success('知识图谱构建成功')

    await getKnowledgeGraphStatus()

    selectedFile.value = null
    uploadRef.value?.clearFiles()
    
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '知识图谱构建失败')
    }
  } finally {
    kgBuilding.value = false
  }
}

const deleteKnowledgeGraph = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除知识图谱吗？删除后将无法使用知识图谱检索功能。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    kgDeleting.value = true
    await knowledgeGraphApi.delete()
    ElMessage.success('知识图谱删除成功')
    await getKnowledgeGraphStatus()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '知识图谱删除失败')
    }
  } finally {
    kgDeleting.value = false
  }
}

const updateVectorIndex = async () => {
  try {
    await ElMessageBox.confirm(
      '更新索引将先删除旧索引再创建新索引，此过程可能需要几分钟时间，是否继续？',
      '确认更新',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    updating.value = true
    await vectorIndexApi.update()
    ElMessage.success('索引更新成功')
    await Promise.all([
      getVectorIndexStatus()
    ])
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '索引更新失败')
    }
  } finally {
    updating.value = false
  }
}

const createVectorIndex = async () => {
  try {
    await ElMessageBox.confirm(
      '创建索引将处理所有病例数据，此过程可能需要几分钟时间，是否继续？',
      '确认创建',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info',
      }
    )
    
    creating.value = true
    await vectorIndexApi.create()
    ElMessage.success('索引创建成功')
    await Promise.all([
      getVectorIndexStatus()
    ])
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '索引创建失败')
    }
  } finally {
    creating.value = false
  }
}

const deleteVectorIndex = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除向量索引吗？删除后将无法使用语义检索功能。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    deleting.value = true
    await vectorIndexApi.delete()
    ElMessage.success('索引删除成功')
    await Promise.all([
      getVectorIndexStatus()
    ])
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '索引删除失败')
    }
  } finally {
    deleting.value = false
  }
}

const refreshIndexStatus = async () => {
  await Promise.all([
    getVectorIndexStatus(),
    getKnowledgeGraphStatus()
  ])
  ElMessage.success('状态已刷新')
}

const refreshAllStats = async () => {
  try {
    const [userResult, caseResult, categoryResult] = await Promise.all([
      getUserList({ current: 1, size: 1 }),
      itemApi.page({ current: 1, size: 1 }),
      categoryApi.page({ current: 1, size: 1 })
    ])
    
    userCount.value = userResult.total || 0
    caseCount.value = caseResult.total || 0
    categoryCount.value = categoryResult.total || 0
    
    ElMessage.success('统计数据已刷新')
  } catch (error) {
    console.error('刷新统计数据失败:', error)
    ElMessage.error('刷新统计数据失败')
  }
}

onMounted(async () => {
  await Promise.all([
    getVectorIndexStatus(),
    getKnowledgeGraphStatus()
  ])
})
</script>

<style scoped>
.rag-management {
  padding: 16px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.box-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #2c5aa0;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  padding: 15px 20px;
  margin: -16px -16px 16px -16px;
}

.card-header .el-icon {
  font-size: 1.2rem;
  color: #16a085;
}

.index-info {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #e1f0ff;
}

.info-item {
  text-align: center;
}

.info-label {
  font-size: 0.95rem;
  color: #5a6c7d;
  margin-bottom: 10px;
  font-weight: 500;
}

.info-value {
  font-size: 1.4rem;
  font-weight: 600;
  color: #2c5aa0;
}

.info-value .el-tag {
  font-size: 1rem;
  font-weight: 600;
  border-radius: 20px;
  padding: 6px 16px;
}

.info-value .el-tag--success {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #16a085;
  border: 1px solid #16a085;
}

.info-value .el-tag--warning {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  color: #f57c00;
  border: 1px solid #f57c00;
}

.info-value .el-tag--danger {
  background: linear-gradient(135deg, #fde8e8 0%, #fad2d2 100%);
  color: #e53e3e;
  border: 1px solid #e53e3e;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c5aa0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e1f0ff;
}

.actions-section,
.refresh-section {
  margin-bottom: 20px;
}

.kg-section {
  padding-top: 20px;
  border-top: 2px dashed #e1f0ff;
}

.kg-status {
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #ffe082;
}

.upload-section {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.upload-tip {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #5a6c7d;
}

.selected-file {
  margin-left: 10px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.button-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.button-item .el-button {
  border-radius: 25px;
  padding: 12px 30px;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 140px;
}

.button-item .el-button--primary {
  background: linear-gradient(135deg, #2c5aa0 0%, #16a085 100%);
  border: none;
}

.button-item .el-button--primary:hover {
  background: linear-gradient(135deg, #1e4d8c 0%, #138d75 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(44, 90, 160, 0.3);
}

.button-item .el-button--success {
  background: linear-gradient(135deg, #16a085 0%, #27ae60 100%);
  border: none;
}

.button-item .el-button--success:hover {
  background: linear-gradient(135deg, #138d75 0%, #229954 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(22, 160, 133, 0.3);
}

.button-item .el-button--success:disabled {
  background: linear-gradient(135deg, #a8d5cd 0%, #a8d5cd 100%);
  cursor: not-allowed;
}

.button-item .el-button--warning {
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  border: none;
}

.button-item .el-button--warning:hover {
  background: linear-gradient(135deg, #f57c00 0%, #e65100 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 124, 0, 0.3);
}

.button-item .el-button--warning:disabled {
  background: linear-gradient(135deg, #ffcc80 0%, #ffb74d 100%);
  cursor: not-allowed;
}

.button-item .el-button--danger {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  border: none;
}

.button-item .el-button--danger:hover {
  background: linear-gradient(135deg, #c53030 0%, #9c2626 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(229, 62, 62, 0.3);
}

.button-item .el-button--danger:disabled {
  background: linear-gradient(135deg, #f0a8a8 0%, #f0a8a8 100%);
  cursor: not-allowed;
}

.button-item .el-button--info {
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  border: none;
}

.button-item .el-button--info:hover {
  background: linear-gradient(135deg, #475569 0%, #334155 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(100, 116, 139, 0.3);
}

.button-desc {
  margin-top: 10px;
  font-size: 0.85rem;
  color: #5a6c7d;
  max-width: 200px;
  line-height: 1.4;
}

.description-section {
  background: #f8fbff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e1f0ff;
}

.description-section .el-alert {
  background: transparent;
  border: none;
  padding: 0;
}

.description-content {
  color: #5a6c7d;
  line-height: 1.8;
}

.description-content p {
  margin-bottom: 10px;
}

.description-content p strong {
  color: #2c5aa0;
}

.description-content ul {
  margin: 10px 0;
  padding-left: 20px;
}

.description-content li {
  margin-bottom: 5px;
}

@media (max-width: 768px) {
  .rag-management {
    padding: 15px;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .button-item {
    width: 100%;
  }
  
  .button-item .el-button {
    width: 100%;
  }
  
  .button-desc {
    max-width: 100%;
  }
}
</style>
