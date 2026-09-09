<template>
  <div class="user-action-history">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>患者行为历史</span>
          <el-button 
            v-if="selected.length > 0" 
            type="danger" 
            @click="handleBatchDelete"
          >
            批量删除 ({{ selected.length }})
          </el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="queryParams" class="demo-form-inline">
        <el-form-item label="患者姓名">
          <el-input v-model="queryParams.username" placeholder="患者姓名" clearable @keyup.enter="fetchHistoryList"></el-input>
        </el-form-item>
        <el-form-item label="病例名称">
          <el-input v-model="queryParams.itemTitle" placeholder="病例名称" clearable @keyup.enter="fetchHistoryList"></el-input>
        </el-form-item>
        <el-form-item label="行为类型">
          <el-select v-model="queryParams.actionType" placeholder="行为类型" clearable @keyup.enter="fetchHistoryList" style="width: 150px;">
            <el-option label="查看病例" :value="0"></el-option>
            <el-option label="咨询病例" :value="1"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchHistoryList">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table
        v-loading="loading"
        :data="historyList"
        border
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column
          prop="userInfo.username"
          label="患者姓名"
          min-width="100"
        >
          <template #default="scope">
            {{ scope.row.username ? scope.row.username : '-' }}
          </template>
        </el-table-column>
        <el-table-column
          prop="item.title"
          label="病例名称"
          min-width="120"
        >
          <template #default="scope">
            <router-link :to="'/user/item/' + scope.row.itemId" class="item-link">
              {{ scope.row.itemTitle ? scope.row.itemTitle : '未知病例' }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="actionType"
          label="行为类型"
          min-width="80"
        >
          <template #default="scope">
            {{ scope.row.actionType === 0 ? '查看病例' : '咨询病例' }}
          </template>
        </el-table-column>
        <el-table-column
          prop="extraData"
          label="附加信息"
          min-width="120"
        >
          <template #default="scope">
            <span v-if="scope.row.extraData" v-html="formatExtraData(scope.row.extraData)"></span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="行为时间"
          min-width="160"
        >
          <template #default="scope">
            {{ formatDate(scope.row.createTime) }}
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="queryParams.current"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="queryParams.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
    </el-card>
    
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <span>确认要删除选中的 {{ selected.length }} 条记录吗？此操作不可撤销。</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmBatchDelete" :loading="deleteLoading">
            确认删除
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { pageAllActions, batchDeleteActions, type UserActionQueryParams } from '@/api/userAction'
import { formatDate, formatDateToChineseDay } from '@/utils/date'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const deleteLoading = ref(false)
const historyList = ref<any[]>([])
const total = ref(0)
const selected = ref<any[]>([])
const deleteDialogVisible = ref(false)
const queryParams = ref<UserActionQueryParams>({
  current: 1,
  size: 10,
  username: undefined,
  itemTitle: undefined,
  actionType: undefined
})

const escapeHtml = (value: unknown): string => {
  return String(value ?? '').replace(/[&<>"']/g, (ch) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[ch])
}

const formatExtraData = (extraDataStr: string): string => {
  try {
    const extraData = JSON.parse(extraDataStr)

    if (extraData.viewTime) {
      let displayTime = extraData.viewTime
      if (typeof displayTime === 'string' && displayTime.includes('T')) {
        displayTime = formatDateToChineseDay(displayTime)
      }
      return `<div style="color: #409eff; font-weight: 600;">查看时间: ${escapeHtml(displayTime)}</div>`
    }

    if (extraData.consultTime || extraData.symptoms || extraData.medications) {
      let formattedData = '<div style="display: flex; flex-direction: column; gap: 8px;">'

      if (extraData.consultId) {
        formattedData += `<div style="margin-bottom: 5px;">
          <span style="font-weight: 600; color: #606266; margin-right: 5px;">咨询号:</span>
          <span style="color: #333;">${escapeHtml(extraData.consultId)}</span>
        </div>`
      }

      if (extraData.consultTime) {
        formattedData += `<div style="margin-bottom: 5px;">
          <span style="font-weight: 600; color: #606266; margin-right: 5px;">咨询时间:</span>
          <span style="color: #409eff; font-weight: 600;">${escapeHtml(extraData.consultTime)}</span>
        </div>`
      }

      if (extraData.symptoms) {
        formattedData += `<div style="margin-bottom: 5px;">
          <div style="font-weight: 600; color: #606266; margin-bottom: 3px;">症状描述:</div>
          <div style="color: #333; font-size: 12px; line-height: 1.4; background: #f5f7fa; padding: 4px 6px; border-radius: 3px;">${escapeHtml(extraData.symptoms)}</div>
        </div>`
      }

      if (extraData.medications) {
        formattedData += `<div style="margin-bottom: 5px;">
          <div style="font-weight: 600; color: #606266; margin-bottom: 3px;">用药方案:</div>
          <div style="color: #333; font-size: 12px; line-height: 1.4; background: #f0f9ff; padding: 4px 6px; border-radius: 3px; border-left: 2px solid #409eff;">${escapeHtml(extraData.medications)}</div>
        </div>`
      }

      formattedData += '</div>'
      return formattedData
    }

    return '-'
  } catch (e) {
    return '-'
  }
}

const fetchHistoryList = async () => {
  loading.value = true
  try {
    const response = await pageAllActions(queryParams.value)
    historyList.value = response.records || []
    total.value = response.total || 0
  } catch (error) {
    console.error('获取患者行为历史失败', error)
    ElMessage.error('获取患者行为历史失败')
  } finally {
    loading.value = false
  }
}

const resetQuery = () => {
  queryParams.value = {
    current: 1,
    size: 10,
    username: undefined,
    itemTitle: undefined,
    actionType: undefined
  }
  fetchHistoryList()
}

const handleSizeChange = (size: number) => {
  queryParams.value.size = size
  fetchHistoryList()
}

const handleCurrentChange = (current: number) => {
  queryParams.value.current = current
  fetchHistoryList()
}

const handleSelectionChange = (selection: any[]) => {
  selected.value = selection
}

const handleBatchDelete = () => {
  if (selected.value.length === 0) {
    ElMessage.warning('请至少选择一条记录')
    return
  }
  
  deleteDialogVisible.value = true
}

const confirmBatchDelete = async () => {
  if (selected.value.length === 0) {
    deleteDialogVisible.value = false
    return
  }
  
  deleteLoading.value = true
  try {
    const ids = selected.value.map(item => item.id)
    
    const result = await batchDeleteActions(ids)
    
    if (result) {
      ElMessage.success(`成功删除 ${selected.value.length} 条记录`)
      fetchHistoryList()
      selected.value = []
    } else {
      ElMessage.error('删除失败')
    }
    
    deleteDialogVisible.value = false
  } catch (error) {
    console.error('批量删除失败', error)
    ElMessage.error('批量删除失败')
  } finally {
    deleteLoading.value = false
  }
}

onMounted(() => {
  fetchHistoryList()
})
</script>

<style scoped>
.user-action-history {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  text-align: center;
}
.item-link {
  color: #409EFF;
  text-decoration: none;
}
.item-link:hover {
  text-decoration: underline;
}
.extra-data-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.extra-data-item {
  display: flex;
  align-items: baseline;
}
.extra-data-key {
  font-weight: 600;
  color: #606266;
  margin-right: 5px;
}
.extra-data-value {
  color: #333;
}
</style> 
