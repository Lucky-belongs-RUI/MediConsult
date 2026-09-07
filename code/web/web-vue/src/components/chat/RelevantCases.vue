<template>
  <div class="relevant-cases" v-if="cases.length > 0">
    <div class="cases-header">
      <el-icon><Document /></el-icon>
      <span>参考病例 ({{ cases.length }}个)</span>
      <el-button 
        link 
        size="small" 
        @click="collapsed = !collapsed"
        :icon="collapsed ? ArrowDown : ArrowUp"
      >
        {{ collapsed ? '展开' : '收起' }}
      </el-button>
    </div>
    
    <div class="cases-content" v-show="!collapsed">
      <div 
        v-for="(caseItem, index) in cases" 
        :key="caseItem.id" 
        class="case-item clickable"
        @click="goToItemDetail(caseItem.id)"
      >
        <div class="case-header">
          <div class="case-number">病例 {{ index + 1 }}</div>
          <el-tag 
            :type="getCategoryTagType(caseItem.categoryName)" 
            size="small"
          >
            {{ caseItem.categoryName }}
          </el-tag>
        </div>
        
        <div class="case-title">
          {{ caseItem.title }}
          <span class="view-detail-hint">点击查看详情 →</span>
        </div>
        
        <div class="case-description" v-if="caseItem.description">
          {{ caseItem.description }}
        </div>
        
        <div class="case-details" v-if="caseItem.extraData">
          <div 
            v-for="(value, key) in getDisplayableFields(caseItem.extraData)" 
            :key="key"
            class="detail-item"
          >
            <span class="detail-label">{{ getFieldLabel(key) }}：</span>
            <span class="detail-value">{{ value }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Document, ArrowDown, ArrowUp } from '@element-plus/icons-vue'

interface CaseData {
  id: number
  title: string
  description: string
  categoryName: string
  extraData?: Record<string, any>
}

interface Props {
  cases: CaseData[]
  defaultCollapsed?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  defaultCollapsed: false
})

const collapsed = ref(props.defaultCollapsed)
const router = useRouter()

const goToItemDetail = (caseId: number) => {
  try {
    router.push({
      name: 'UserItemDetail',
      params: { id: caseId }
    })

    console.log('📊 用户点击RAG推荐病例:', caseId)
  } catch (error) {
    console.error('跳转病例详情失败:', error)
  }
}

const getCategoryTagType = (categoryName: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const categoryTypes: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    '内科': 'primary',
    '外科': 'success',
    '妇产科': 'warning',
    '儿科': 'info',
    '急诊科': 'danger'
  }
  return categoryTypes[categoryName] || 'primary'
}

const getDisplayableFields = (extraData: Record<string, any>) => {
  const displayFields = ['gender', 'age', 'symptoms', 'diagnosis', 'treatment', 'medications', 'severity']
  const result: Record<string, any> = {}
  
  displayFields.forEach(field => {
    if (extraData[field] && extraData[field] !== '') {
      result[field] = extraData[field]
    }
  })
  
  return result
}

const getFieldLabel = (key: string) => {
  const labels: Record<string, string> = {
    gender: '性别',
    age: '年龄',
    symptoms: '症状',
    diagnosis: '诊断',
    treatment: '治疗',
    medications: '用药',
    severity: '严重程度',
    followUp: '随访'
  }
  return labels[key] || key
}
</script>

<style scoped>
.relevant-cases {
  margin: 12px 0;
  border: 1px solid #dce7fb;
  border-radius: 10px;
  background-color: #f9fbff;
  overflow: hidden;
}

.cases-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
  border-bottom: 1px solid #dce7fb;
  font-weight: 600;
  color: #1f3b60;
  gap: 8px;
}

.cases-header span {
  flex: 1;
}

.cases-content {
  padding: 16px;
}

.case-item {
  margin-bottom: 20px;
  padding: 16px;
  background-color: #fff;
  border: 1px solid #dce7fb;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(79, 141, 230, 0.08);
  transition: all 0.3s ease;
}

.case-item:last-child {
  margin-bottom: 0;
}

.case-item.clickable {
  cursor: pointer;
}

.case-item.clickable:hover {
  border-color: #4f8de6;
  box-shadow: 0 6px 20px rgba(79, 141, 230, 0.18);
  transform: translateY(-2px);
  background-color: #f5faff;
}

.case-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.case-number {
  font-weight: 600;
  color: #4f8de6;
  font-size: 14px;
}

.case-title {
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  font-size: 15px;
  line-height: 1.4;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.view-detail-hint {
  font-size: 12px;
  color: #7b8fb4;
  font-weight: 400;
  opacity: 0;
  transition: opacity 0.3s ease;
  white-space: nowrap;
}

.case-item.clickable:hover .view-detail-hint {
  opacity: 1;
  color: #4f8de6;
}

.case-description {
  color: #606266;
  margin-bottom: 12px;
  line-height: 1.6;
  font-size: 14px;
}

.case-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.detail-item {
  font-size: 13px;
  line-height: 1.5;
}

.detail-label {
  color: #909399;
  font-weight: 500;
}

.detail-value {
  color: #606266;
}

@media (max-width: 768px) {
  .case-details {
    grid-template-columns: 1fr;
  }
  
  .cases-header {
    padding: 10px 12px;
  }
  
  .cases-content {
    padding: 12px;
  }
  
  .case-item {
    padding: 12px;
  }
  
  .case-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .view-detail-hint {
    opacity: 1;
    font-size: 11px;
  }
}
</style> 