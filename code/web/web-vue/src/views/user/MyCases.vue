<template>
  <div class="my-cases">
    <el-card shadow="never" class="header-card">
      <div class="header">
        <div>
          <h2 class="title">我的病例</h2>
          <p class="subtitle">智能医生问诊结束后，可点击「记录病例」将问诊保存到这里。公开后将在「公开病例」（病例库）中展示，所有人可见。</p>
        </div>
        <el-button type="primary" @click="goChat">
          <el-icon style="margin-right: 4px;"><Plus /></el-icon>
          新建问诊
        </el-button>
      </div>

      <el-form inline class="search-form" @submit.prevent>
        <el-form-item label="问诊名称">
          <el-input v-model="queryForm.title" placeholder="搜索问诊名称" clearable style="width: 220px" @keyup.enter="handleSearch" @clear="handleSearch" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table v-loading="loading" :data="caseList" style="width: 100%">
        <el-table-column label="问诊名称" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" :underline="false" @click="openDetail(row)">{{ row.title }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="patientName" label="患者姓名" width="110" />
        <el-table-column label="年龄 / 性别" width="110">
          <template #default="{ row }">
            {{ formatAgeGender(row.age, row.gender) }}
          </template>
        </el-table-column>
        <el-table-column prop="categoryName" label="问诊科室" width="130">
          <template #default="{ row }">
            {{ row.categoryName || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="公开状态" width="130">
          <template #default="{ row }">
            <el-tag :type="row.isPublic === 1 ? 'success' : 'info'" size="small">
              {{ row.isPublic === 1 ? '公开' : '私有' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updateTime" label="更新时间" width="170" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDetail(row)">查看</el-button>
            <el-switch
              :model-value="row.isPublic === 1"
              size="small"
              :loading="switchingId === row.id"
              inline-prompt
              active-text="公开"
              inactive-text="私有"
              @change="(val: boolean) => handleVisibilityChange(row, val)"
            />
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无病例记录，去智能医生完成一次问诊并记录病例吧" />
        </template>
      </el-table>

      <div class="pagination-container" v-if="pagination.itemCount > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.itemCount"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handlePageChange(1)"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="detailVisible" title="病例详情" width="640px">
      <div v-if="currentCase" class="case-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="问诊名称">{{ currentCase.title }}</el-descriptions-item>
          <el-descriptions-item label="患者姓名">{{ currentCase.patientName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ currentCase.age ?? '-' }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ currentCase.gender || '-' }}</el-descriptions-item>
          <el-descriptions-item label="问诊科室">{{ currentCase.categoryName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="公开状态">
            <el-tag :type="currentCase.isPublic === 1 ? 'success' : 'info'" size="small">
              {{ currentCase.isPublic === 1 ? '公开' : '私有' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="特殊情况备注" :span="2">{{ currentCase.remark || '无' }}</el-descriptions-item>
          <el-descriptions-item label="记录时间" :span="2">{{ currentCase.createTime }}</el-descriptions-item>
        </el-descriptions>

        <div v-if="aiSummaryData" class="content-title">AI 病例摘要（结构化数据）</div>
        <div v-if="aiSummaryData" class="ai-summary">
          <p><b>标题：</b>{{ aiSummaryData.title }}</p>
          <p><b>病例概述：</b>{{ aiSummaryData.description }}</p>
          <p v-if="aiSummaryData.basic_info"><b>患者基本信息：</b>{{ aiSummaryData.basic_info }}</p>
          <p v-if="aiSummaryData.clinical"><b>临床表现：</b>{{ aiSummaryData.clinical }}</p>
          <p v-if="aiSummaryData.diagnosis"><b>诊断结果：</b>{{ aiSummaryData.diagnosis }}</p>
          <p v-if="aiSummaryData.treatment"><b>治疗方案：</b>{{ aiSummaryData.treatment }}</p>
          <p v-if="aiSummaryData.follow_up"><b>注意事项与随访：</b>{{ aiSummaryData.follow_up }}</p>
          <p v-if="aiSummaryData.tags"><b>标签：</b>{{ aiSummaryData.tags }}</p>
        </div>
        <div class="content-title">问诊记录</div>
        <div class="content-body">{{ currentCase.content || '无问诊记录' }}</div>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { userCaseApi } from '@/api/userCase'
import type { UserCase } from '@/types/userCase'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const caseList = ref<UserCase[]>([])
const detailVisible = ref(false)
const currentCase = ref<UserCase | null>(null)
const aiSummaryData = computed(() => {
  if (!currentCase.value?.aiSummary) return null
  try { return JSON.parse(currentCase.value.aiSummary) } catch { return null }
})
const switchingId = ref<number | null>(null)

const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0
})

const queryForm = reactive({
  title: ''
})

const fetchCases = async () => {
  const userId = userStore.userInfo?.id
  if (!userId) return

  loading.value = true
  try {
    const res = await userCaseApi.myPage({
      current: pagination.page,
      size: pagination.pageSize,
      userId,
      title: queryForm.title || undefined
    })
    caseList.value = res.records
    pagination.itemCount = res.total
  } catch (error) {
    console.error('获取我的病例失败', error)
    ElMessage.error('获取我的病例失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchCases()
}

const handleReset = () => {
  queryForm.title = ''
  pagination.page = 1
  fetchCases()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchCases()
}

const formatAgeGender = (age: number | null | undefined, gender: string) => {
  if (age === null || age === undefined) return gender || '-'
  return `${age}岁${gender ? ' / ' + gender : ''}`
}

const openDetail = (row: UserCase) => {
  currentCase.value = row
  detailVisible.value = true
}

const handleVisibilityChange = async (row: UserCase, val: boolean) => {
  switchingId.value = row.id
  try {
    const isPublic = val ? 1 : 0
    await userCaseApi.updateVisibility(row.id, isPublic)
    row.isPublic = isPublic
    ElMessage.success(isPublic === 1 ? '已公开，可在公开病例（病例库）中查看' : '已取消公开')
  } catch (error) {
    console.error('更新公开状态失败', error)
    ElMessage.error('操作失败')
  } finally {
    switchingId.value = null
  }
}

const handleDelete = async (row: UserCase) => {
  try {
    await ElMessageBox.confirm(`确定删除病例「${row.title}」吗？删除后不可恢复`, '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await userCaseApi.delete(row.id)
    ElMessage.success('删除成功')
    if (caseList.value.length === 1 && pagination.page > 1) {
      pagination.page -= 1
    }
    fetchCases()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除病例失败', error)
      ElMessage.error('删除失败')
    }
  }
}

const goChat = () => {
  router.push('/user/chat')
}

onMounted(() => {
  fetchCases()
})
</script>

<style scoped>
.my-cases {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-card {
  margin-bottom: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.title {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.subtitle {
  margin: 6px 0 0;
  color: #909399;
  font-size: 13px;
}

.search-form {
  margin-top: 12px;
}

.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.case-detail .content-title {
  margin: 18px 0 8px;
  font-weight: 600;
  color: #303133;
}

.case-detail .ai-summary {
  background: #ecf5ff;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 8px;
  color: #303133;
  line-height: 1.7;
  font-size: 14px;
}

.case-detail .content-body {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.7;
  color: #606266;
  background: #f5f7fa;
  border-radius: 6px;
  padding: 12px;
  max-height: 360px;
  overflow-y: auto;
  font-size: 14px;
}
</style>
