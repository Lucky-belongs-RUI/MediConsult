<template>
  <div class="case-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton animated :rows="3" :loading="loading" />
    </div>

    <div v-else-if="!item" class="error-container">
      <el-result 
        icon="error" 
        title="未找到"
        sub-title="未找到该病例信息">
        <template #extra>
          <el-button type="primary" @click="goBack">返回</el-button>
        </template>
      </el-result>
    </div>

    <template v-else>
      <div class="case-header">
        <el-button @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <div class="case-actions">
          <el-button type="primary" :icon="Share" @click="handleCopyLink" class="action-button">
            分享
          </el-button>
          <el-button type="info" :icon="Download" @click="generateDocument" class="action-button" :loading="documentLoading">
            生成病例文档
          </el-button>
          <el-button type="success" @click="purchaseItem" class="action-button">
            咨询病例
          </el-button>
        </div>
      </div>

      <el-card class="case-title-card">
        <div class="case-title-section">
          <h1 class="case-title">{{ item.title }}</h1>
          <div class="case-meta-info">
            <div class="meta-row">
              <span class="meta-label">科室：</span>
              <el-tag size="large" effect="plain" type="primary">{{ item.category.name }}</el-tag>
            </div>
            <div class="meta-row">
              <span class="meta-label">主治医生：</span>
              <span class="meta-value">{{ item.userRealName || '未知' }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">创建时间：</span>
              <span class="meta-value">{{ formatDate(item.createTime) }}</span>
            </div>
          </div>
        </div>

        <div class="case-actions-section">
          <LikeButton 
            :itemId="item.id" 
            v-model:isLiked="isLiked" 
            v-model:likeCount="likeCount"
            @like="onLike"
            @unlike="onUnlike"
            size="large"
          />
          <FavoriteButton
            :itemId="item.id"
            v-model:isFavorite="isFavorite"
            @favorite="onFavorite"
            @unfavorite="onUnfavorite"
            size="large"
          />
        </div>
      </el-card>

      <div class="case-content-grid">
        <div class="case-main-content">
          <el-card class="case-section-card">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><Document /></el-icon>
                <span class="section-title">病例概述</span>
              </div>
            </template>
            <div class="case-description">
              <p v-if="item.description">{{ item.description }}</p>
              <p v-else class="no-data">暂无病例概述</p>
            </div>
          </el-card>

          <el-card class="case-section-card" v-if="item.extraData">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><User /></el-icon>
                <span class="section-title">患者基本信息</span>
              </div>
            </template>
            <div class="patient-info-grid" v-if="parseExtraData(item.extraData).gender || parseExtraData(item.extraData).age || parseExtraData(item.extraData).vitalSigns">
              <div class="info-item" v-if="parseExtraData(item.extraData).gender">
                <span class="info-label">性别</span>
                <span class="info-value">{{ parseExtraData(item.extraData).gender }}</span>
              </div>
              <div class="info-item" v-if="parseExtraData(item.extraData).age">
                <span class="info-label">年龄</span>
                <span class="info-value">{{ parseExtraData(item.extraData).age }}岁</span>
              </div>
              <div class="info-item" v-if="parseExtraData(item.extraData).vitalSigns">
                <span class="info-label">生命体征</span>
                <span class="info-value">{{ parseExtraData(item.extraData).vitalSigns }}</span>
              </div>
            </div>
            <div class="patient-info-text" v-if="parseExtraData(item.extraData).basic_info">
              <p class="patient-info-text-content">{{ parseExtraData(item.extraData).basic_info }}</p>
            </div>
            <p v-if="!parseExtraData(item.extraData).gender && !parseExtraData(item.extraData).age && !parseExtraData(item.extraData).vitalSigns && !parseExtraData(item.extraData).basic_info" class="no-data">暂无患者基本信息</p>
          </el-card>

          <el-card class="case-section-card" v-if="item.extraData">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><Warning /></el-icon>
                <span class="section-title">临床表现</span>
              </div>
            </template>
            <div class="symptoms-content">
              <div class="symptoms-description" v-if="parseExtraData(item.extraData).symptoms || parseExtraData(item.extraData).clinical">
                <h4>症状描述</h4>
                <p class="symptom-text">{{ parseExtraData(item.extraData).symptoms || parseExtraData(item.extraData).clinical }}</p>
              </div>
              <div class="symptoms-tags" v-if="(item as any).tagList && (item as any).tagList.length > 0">
                <h4>症状标签</h4>
                <div class="tags-container">
                  <el-tag 
                    v-for="tag in (item as any).tagList" 
                    :key="tag" 
                    size="large" 
                    effect="light"
                    type="warning" 
                    class="symptom-tag"
                  >
                    {{ tag }}
                  </el-tag>
                </div>
              </div>
            </div>
          </el-card>

          <el-card class="case-section-card" v-if="item.extraData && parseExtraData(item.extraData).diagnosis">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><CircleCheck /></el-icon>
                <span class="section-title">诊断结果</span>
              </div>
            </template>
            <div class="diagnosis-content">
              <div class="diagnosis-main">
                <span class="diagnosis-label">诊断：</span>
                <span class="diagnosis-text">{{ parseExtraData(item.extraData).diagnosis }}</span>
              </div>
              <div class="severity-info" v-if="parseExtraData(item.extraData).severity">
                <span class="severity-label">严重程度：</span>
                <el-tag 
                  :type="getSeverityType(parseExtraData(item.extraData).severity)" 
                  size="large"
                  effect="light"
                >
                  {{ parseExtraData(item.extraData).severity }}
                </el-tag>
              </div>
            </div>
          </el-card>

          <el-card class="case-section-card" v-if="item.extraData">
            <template #header>
                             <div class="section-header">
                 <el-icon class="section-icon"><Document /></el-icon>
                 <span class="section-title">治疗方案</span>
               </div>
            </template>
            <div class="treatment-content">
              <div class="treatment-plan" v-if="parseExtraData(item.extraData).treatment">
                <h4>治疗方案</h4>
                <p class="treatment-text">{{ parseExtraData(item.extraData).treatment }}</p>
              </div>
              <div class="medications" v-if="parseExtraData(item.extraData).medications">
                <h4>用药方案</h4>
                <div class="medication-box">
                  <p class="medication-text">{{ parseExtraData(item.extraData).medications }}</p>
                </div>
              </div>
            </div>
          </el-card>

          <el-card class="case-section-card" v-if="item.extraData && (parseExtraData(item.extraData).precautions || parseExtraData(item.extraData).followUp || parseExtraData(item.extraData).follow_up)">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><InfoFilled /></el-icon>
                <span class="section-title">注意事项与随访</span>
              </div>
            </template>
            <div class="precautions-content">
              <div class="precautions" v-if="parseExtraData(item.extraData).precautions">
                <h4>注意事项</h4>
                <div class="precautions-box">
                  <p class="precautions-text">{{ parseExtraData(item.extraData).precautions }}</p>
                </div>
              </div>
              <div class="follow-up" v-if="parseExtraData(item.extraData).followUp || parseExtraData(item.extraData).follow_up">
                <h4>随访要求</h4>
                <div class="follow-up-box">
                  <p class="follow-up-text">{{ parseExtraData(item.extraData).followUp || parseExtraData(item.extraData).follow_up }}</p>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <div class="case-sidebar">
          <el-card class="sidebar-card">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><Folder /></el-icon>
                <span class="section-title">病例附件</span>
              </div>
            </template>
            <div class="attachments-content">
              <div class="case-cover-container" v-if="item.coverUrl">
                <el-image 
                  :src="item.coverUrl" 
                  class="case-cover"
                  fit="cover"
                  :preview-src-list="[item.coverUrl]"
                  :initial-index="0"
                  :hide-on-click-modal="false"
                  preview-teleported
                >
                  <template #error>
                    <div class="image-error">
                      <el-icon><Picture /></el-icon>
                      <span>图片加载失败</span>
                    </div>
                  </template>
                </el-image>
              </div>
              <div v-else class="no-image-placeholder">
                <el-icon><Picture /></el-icon>
                <span>暂无附件图片</span>
              </div>
              
              <div class="download-section" v-if="item.fileUrl">
                <el-button type="primary" @click="handleDownload" class="download-button" plain>
                  <el-icon><Download /></el-icon>
                  下载病例文件
                </el-button>
              </div>
              <div v-else class="no-file-section">
                <el-text type="info" size="small">暂无可下载文件</el-text>
              </div>
            </div>
          </el-card>

          <el-card class="sidebar-card">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><DataAnalysis /></el-icon>
                <span class="section-title">病例统计</span>
              </div>
            </template>
            <div class="stats-content">
              <div class="stat-item">
                <div class="stat-info">
                  <el-icon class="stat-icon"><Star /></el-icon>
                  <span class="stat-label">点赞数</span>
                </div>
                <span class="stat-value">{{ likeCount }}</span>
              </div>
              <div class="stat-item">
                <div class="stat-info">
                  <el-icon class="stat-icon"><ChatDotRound /></el-icon>
                  <span class="stat-label">评论数</span>
                </div>
                <span class="stat-value">{{ commentCount }}</span>
              </div>
              <div class="stat-item">
                <div class="stat-info">
                  <el-icon class="stat-icon"><Clock /></el-icon>
                  <span class="stat-label">更新时间</span>
                </div>
                <span class="stat-value stat-time">{{ formatShortDate(item.updateTime) }}</span>
              </div>
            </div>
          </el-card>

          <el-card class="sidebar-card">
            <template #header>
              <div class="section-header">
                <el-icon class="section-icon"><InfoFilled /></el-icon>
                <span class="section-title">操作指南</span>
              </div>
            </template>
            <div class="guide-content">
              <div class="guide-item">
                <el-icon class="guide-icon"><View /></el-icon>
                <span class="guide-text">点击图片可预览放大</span>
              </div>
              <div class="guide-item">
                <el-icon class="guide-icon"><Share /></el-icon>
                <span class="guide-text">可分享病例给同事</span>
              </div>
              <div class="guide-item">
                <el-icon class="guide-icon"><Star /></el-icon>
                <span class="guide-text">点赞收藏优质病例</span>
              </div>
              <div class="guide-item">
                <el-icon class="guide-icon"><ChatDotRound /></el-icon>
                <span class="guide-text">评论区交流学习</span>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <el-card class="comments-card" v-if="item">
        <template #header>
          <div class="comments-header">
            <div class="section-header">
              <el-icon class="section-icon"><ChatDotRound /></el-icon>
              <span class="section-title">病例讨论（{{ commentCount }}）</span>
            </div>
          </div>
        </template>
        <CommentList :item-id="Number(item.id)" @update-count="updateCommentCount" />
      </el-card>
    </template>

    <div class="image-viewer-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { itemApi } from '@/api/item'
import { addUserAction, type UserActionData } from '@/api/userAction'
import { documentApi } from '@/api/document'
import type { ItemVO } from '@/types/item'
import { 
  ArrowLeft, Download, Share, Picture, User, Document, Warning, 
  CircleCheck, InfoFilled, Folder, DataAnalysis, ChatDotRound, Star, Clock, View 
} from '@element-plus/icons-vue'
import LikeButton from '@/components/LikeButton.vue'
import FavoriteButton from '@/components/FavoriteButton.vue'
import CommentList from '@/components/CommentList.vue'
import { formatCurrentTimeToChineseDay, formatCurrentTimeToMinute } from '@/utils/date'
import { useUserStore } from '@/stores/user' 

const userStore = useUserStore()
userStore.initUserInfo() 

const route = useRoute()
const router = useRouter()
const item = ref<ItemVO | null>(null)
const loading = ref(true)
const isLiked = ref(false)
const likeCount = ref(0)
const isFavorite = ref(false)
const commentCount = ref(0)
const documentLoading = ref(false)
const getCurrentUserId = (): number | null => {

  return userStore.userInfo?.id || null
}
const fetchItemDetail = async () => {
  try {
    loading.value = true
    const rawId = Number(route.params.id)
    if (!rawId || Number.isNaN(rawId)) {
      ElMessage.error('病例ID无效')
      loading.value = false
      return
    }
    const data = await itemApi.getById(rawId)

    item.value = data
    if (item.value) {
      const itemAny = item.value as any
      if (typeof itemAny.tags === 'string') {
        itemAny.tagList = itemAny.tags.split(',')
      } else if (Array.isArray(itemAny.tags)) {
        itemAny.tagList = itemAny.tags
      } else {
        itemAny.tagList = []
      }
    }

    addViewRecord(item.value.id)
  } catch (error) {
    console.error('获取病例详情失败', error)
    ElMessage.error('获取病例详情失败')
  } finally {
    loading.value = false
  }
}

const parseExtraData = (extraDataStr: string): Record<string, any> => {
  if (!extraDataStr) return {}
  try {
    return JSON.parse(extraDataStr)
  } catch (e) {
    console.error('解析额外数据失败:', e)
    return { raw: extraDataStr }
  }
}

const formatKey = (key: string): string => {
  return key
    .replace(/([A-Z])/g, ' $1')
    .replace(/_/g, ' ')
    .replace(/^\s+/, '')
    .replace(/^./, (str: string) => str.toUpperCase())
}

const addViewRecord = async (itemId: number): Promise<void> => {
  try {
    const actionData: UserActionData = {
      userId: getCurrentUserId(),
      itemId: itemId,
      actionType: 0,
      extraData: JSON.stringify({
        viewTime: formatCurrentTimeToChineseDay()
      })
    }

    await addUserAction(actionData)
  } catch (error) {
    console.error('添加查看记录失败', error)
  }
}

const generateDocument = async (): Promise<void> => {
  if (!item.value) return

  try {
    documentLoading.value = true
    ElMessage.info('正在生成病例文档，请稍候...')

    const result = await documentApi.generateCaseDocument(item.value.id)

    window.open(result.downloadUrl, '_blank')

    ElMessage.success('病例文档生成成功！正在下载...')

    const actionData: UserActionData = {
      userId: getCurrentUserId(),
      itemId: item.value.id,
      actionType: 2,
      extraData: JSON.stringify({
        actionTime: formatCurrentTimeToMinute(),
        fileName: result.fileName
      })
    }
    await addUserAction(actionData)
    
  } catch (error) {
    console.error('生成病例文档失败', error)
    ElMessage.error('生成病例文档失败，请稍后重试')
  } finally {
    documentLoading.value = false
  }
}

const purchaseItem = async (): Promise<void> => {
  if (!item.value) return
  try {
    const consultId = 'CST' + Date.now()

    const extraData = parseExtraData((item.value as any).extraData || '{}')
    const symptoms = extraData.symptoms || '患者症状描述'
    const medications = extraData.medications || '暂无用药方案'

    const actionData: UserActionData = {
      userId: getCurrentUserId(),
      itemId: item.value.id,
      actionType: 1,
      extraData: JSON.stringify({
        consultId: consultId,
        consultTime: formatCurrentTimeToMinute(),
        symptoms: symptoms,
        medications: medications
      })
    }
    
    const result = await addUserAction(actionData)
    if (result) {
      ElMessage.success('咨询成功！咨询号：' + consultId)
    } else {
      ElMessage.error('咨询失败，请稍后重试')
    }
  } catch (error) {
    console.error('咨询失败', error)
    ElMessage.error('咨询失败，请稍后重试')
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
}

const formatShortDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
}

const handleDownload = () => {
  if (!item.value || !item.value.fileUrl) {
    ElMessage.warning('无可下载文件')
    return
  }

  ElMessage.info('正在准备文件，请稍候...')

  const xhr = new XMLHttpRequest();
  xhr.open('GET', item.value.fileUrl, true);
  xhr.responseType = 'blob';

  xhr.onload = function() {
    if (xhr.status === 200) {
      const fileName = getFileNameFromUrl(item.value!.fileUrl);

      const blob = new Blob([xhr.response]);
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      link.style.display = 'none';
      document.body.appendChild(link);

      link.click();

      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);

      ElMessage.success('文件下载已开始');
    } else {
      ElMessage.error('下载失败，请稍后再试');
    }
  };

  xhr.onerror = function() {
    ElMessage.error('下载失败，请检查网络连接');
  };

  xhr.send();
}

const getFileNameFromUrl = (url: string): string => {
  const pathParts = url.split('/');
  let fileName = pathParts[pathParts.length - 1];

  if (fileName.includes('?')) {
    fileName = fileName.split('?')[0];
  }

  if (!fileName.includes('.')) {
    fileName += '.bin';
  }

  return fileName;
}

const goBack = () => {
  router.back()
}

const handleCopyLink = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    ElMessage.success('链接已复制，可以分享给好友了')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

const onLike = () => {
  ElMessage.success('点赞成功')
}

const onUnlike = () => {
  ElMessage.success('已取消点赞')
}

const onFavorite = () => {
  ElMessage.success('收藏成功')
}

const onUnfavorite = () => {
  ElMessage.success('已取消收藏')
}

const updateCommentCount = (count: number) => {
  commentCount.value = count
}

const getSeverityType = (severity: string) => {
  switch (severity) {
    case '轻度':
      return 'success' as const
    case '中度':
      return 'warning' as const
    case '重度':
      return 'danger' as const
    default:
      return 'info' as const
  }
}

onMounted(() => {
  fetchItemDetail()
})
</script>

<style scoped>
.case-detail {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 20px 25px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-radius: 16px;
  border: 1px solid #e1f0ff;
  box-shadow: 0 4px 20px rgba(44, 90, 160, 0.08);
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #2c5aa0;
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  border: 1px solid #4204e0;
  border-radius: 20px;
  padding: 8px 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: linear-gradient(135deg, #0a51ec 0%, #2c5aa0 100%);
  color: white;
  transform: translateY(-1px);
}

.case-actions {
  display: flex;
  gap: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 20px;
  padding: 8px 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-button.el-button--primary {
  background: linear-gradient(135deg, #065ae1 0%, #2c5aa0 100%);
  border: none;
}

.action-button.el-button--primary:hover {
  background: linear-gradient(135deg, #1d08d4 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(22, 160, 133, 0.3);
}

.case-title-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  background-color: #fff;
  margin-bottom: 16px;
  overflow: hidden;
  border: 1px solid #e1f0ff;
  transition: all 0.3s ease;
}

.case-title-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.12);
}

.case-title-section {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.case-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c5aa0;
  margin-bottom: 20px;
  line-height: 1.3;
  display: flex;
  align-items: center;
  gap: 12px;
}

.case-title::before {
  content: '';
  width: 4px;
  height: 30px;
  background: linear-gradient(135deg, #1528f9 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.case-meta-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.meta-label {
  font-size: 0.9rem;
  color: #2c5aa0;
  min-width: 80px;
  font-weight: 500;
}

.meta-value {
  font-size: 1rem;
  color: #5a6c7d;
}

.meta-value .el-tag {
  border-radius: 15px;
  font-weight: 500;
}

.meta-value .el-tag--success {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #2704f0;
  border-color: #1d06ee;
}

.meta-value .el-tag--warning {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #f39c12;
  border-color: #f39c12;
}

.meta-value .el-tag--danger {
  background: linear-gradient(135deg, #fde8e8 0%, #fad2d2 100%);
  color: #e53e3e;
  border-color: #e53e3e;
}

.meta-value .el-tag--info {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #0a59ed;
  border-color: #1f11e2;
}

.case-actions-section {
  display: flex;
  justify-content: center;
  gap: 25px;
  padding: 20px 0;
  border-top: 2px solid #e1f0ff;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.case-content-grid {
  display: flex;
  flex-direction: column;
  gap: 25px;
  padding: 0;
}

.case-main-content {
  width: 100%;
}

.case-section-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  background-color: #fff;
  margin-bottom: 20px;
  border: 1px solid #e1f0ff;
  transition: all 0.3s ease;
}

.case-section-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(44, 90, 160, 0.12);
}

.case-section-card:last-child {
  margin-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 25px;
  border-bottom: 2px solid #e1f0ff;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c5aa0;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #0841ed 0%, #2c5aa0 100%);
  border-radius: 2px;
}

.section-content {
  padding: 25px;
  color: #5a6c7d;
  line-height: 1.6;
}

.section-content h1,
.section-content h2,
.section-content h3,
.section-content h4,
.section-content h5,
.section-content h6 {
  color: #2c5aa0;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.section-content p {
  margin-bottom: 1em;
}

.section-content ul,
.section-content ol {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.section-content li {
  margin-bottom: 0.3em;
}

.section-content strong {
  color: #2c5aa0;
  font-weight: 600;
}

.section-content code {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #e1f0ff;
  color: #16a085;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.section-content pre {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e1f0ff;
  overflow-x: auto;
}

.section-content blockquote {
  border-left: 4px solid #0f72eb;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  padding: 15px 20px;
  margin: 15px 0;
  border-radius: 0 8px 8px 0;
}

.section-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e1f0ff;
}

.section-content th,
.section-content td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e1f0ff;
}

.section-content th {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  color: #2c5aa0;
  font-weight: 600;
}

.section-content tr:hover {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

@media (max-width: 768px) {
  .case-detail {
    padding: 15px;
  }
  
  .case-header {
    flex-direction: column;
    gap: 15px;
    padding: 20px;
  }
  
  .case-actions {
    width: 100%;
    justify-content: center;
  }
  
  .case-title {
    font-size: 1.3rem;
  }
  
  .case-title-section {
    padding: 20px;
  }
  
  .section-header {
    padding: 15px 20px;
  }
  
  .section-content {
    padding: 20px;
  }
  
  .case-actions-section {
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .meta-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .meta-label {
    min-width: auto;
  }
}

.case-sidebar {
  width: 100%;
}

.sidebar-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  background-color: #fff;
  margin-bottom: 15px;
}

.attachments-content {
  padding: 15px;
}

.case-cover-container {
  width: 100%;
  height: 180px;
  overflow: hidden;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  background-color: #f5f7fa;
  margin-bottom: 15px;
  position: relative;
}

.case-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.case-cover:hover {
  transform: scale(1.02);
}

.download-section {
  display: flex;
  justify-content: center;
}

.download-button {
  width: 100%;
  border-radius: 6px;
  height: 36px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.download-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(64, 158, 255, 0.3);
}

.no-image-placeholder {
  width: 100%;
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  color: #909399;
  font-size: 14px;
  border-radius: 6px;
}

.no-image-placeholder .el-icon {
  font-size: 32px;
  margin-bottom: 8px;
  color: #c0c4cc;
}

.no-file-section {
  display: flex;
  justify-content: center;
  padding: 10px;
  border-radius: 6px;
  background-color: #f5f7fa;
}

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-icon {
  font-size: 16px;
  color: #409eff;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.stat-time {
  font-size: 12px;
  color: #909399;
}

.no-data {
  color: #909399;
  font-style: italic;
  font-size: 13px;
}

h4 {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.loading-container, .error-container {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

@media (min-width: 768px) {
  .case-detail {
    padding: 15px;
  }
  
  .case-content-grid {
    flex-direction: row;
    gap: 20px;
  }
  
  .case-main-content {
    width: 70%;
  }
  
  .case-sidebar {
    width: 30%;
  }
  
  .case-title {
    font-size: 22px;
  }
  
  .case-meta-info {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .case-cover-container,
  .no-image-placeholder,
  .image-error {
    height: 160px;
  }
  
  .patient-info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .case-detail {
    padding: 20px;
    max-width: 1400px;
  }
  
  .case-main-content {
    width: 68%;
  }
  
  .case-sidebar {
    width: 32%;
  }
  
  .case-title {
    font-size: 24px;
  }
  
  .case-cover-container,
  .no-image-placeholder,
  .image-error {
    height: 200px;
  }
  
  .patient-info-grid {
    grid-template-columns: repeat(3, 1fr);
  }
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

.comments-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  background-color: #fff;
  margin-bottom: 20px;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fafafa;
}

.image-error {
  width: 100%;
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  color: #909399;
  font-size: 14px;
  border-radius: 6px;
}

.guide-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 15px;
}

  .guide-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .guide-item:last-child {
    border-bottom: none;
  }
  
  .guide-icon {
    font-size: 14px;
    color: #409eff;
  }
  
  .guide-text {
    font-size: 13px;
    color: #606266;
  }
</style> 
