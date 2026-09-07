<template>
  <div class="browsing-history">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>查看历史</span>
          <el-button 
            v-if="selected.length > 0" 
            type="danger" 
            @click="handleBatchDelete"
          >
            批量删除 ({{ selected.length }})
          </el-button>
        </div>
      </template>
      <el-table
        v-loading="loading"
        :data="historyList"
        border
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column
          prop="item.title"
          label="商品名称"
          min-width="120"
        >
          <template #default="scope">
            <router-link :to="'/user/item/' + scope.row.itemId" class="item-link">
              {{ scope.row.itemTitle ? scope.row.itemTitle : '未知病例' }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="item.category.name"
          label="科室"
          min-width="100"
        >
        <template #default="scope">
            <router-link :to="'/user/item/' + scope.row.itemId" class="item-link">
              {{ scope.row.category.name ? scope.row.category.name : '未知病例' }}
            </router-link>
          </template>
        </el-table-column>




        <el-table-column
          prop="extraData"
          label="查看详情"
          min-width="120"
        >
          <template #default="scope">
            <span v-if="scope.row.extraData" v-html="formatExtraData(scope.row.extraData)"></span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="查看时间"
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
      <span>确认要删除选中的 {{ selected.length }} 条查看记录吗？此操作不可撤销。</span>
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
import { pageMyActions, batchDeleteMyActions, type UserActionQueryParams } from '@/api/userAction'
import { formatDate, formatDateToChineseDay } from '@/utils/date'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const userId = userStore.userInfo?.id
const loading = ref(false)
const deleteLoading = ref(false)
const historyList = ref<any[]>([])
const total = ref(0)
const selected = ref<any[]>([])
const deleteDialogVisible = ref(false)
const queryParams = ref<UserActionQueryParams>({
  userId: userId?userId:0,
  current: 1,
  size: 10,
  actionType: 0
})

const formatExtraData = (extraDataStr: string): string => {
  try {
    const extraData = JSON.parse(extraDataStr)

    if (extraData.viewTime) {
      let displayTime = extraData.viewTime

      if (typeof displayTime === 'string' && displayTime.includes('T')) {
        displayTime = formatDateToChineseDay(displayTime)
      }

      return `<span style="color: #409eff; font-weight: 600;">${displayTime}</span>`
    }

    return '-'
  } catch (e) {
    return '-'
  }
}

const fetchHistoryList = async () => {
  loading.value = true
  try {
    const response = await pageMyActions(queryParams.value)
    historyList.value = response.records || []
    total.value = response.total || 0
  } catch (error) {
    console.error('获取查看历史失败', error)
    ElMessage.error('获取查看历史失败')
  } finally {
    loading.value = false
  }
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

    const result = await batchDeleteMyActions(ids)

    if (result) {
      ElMessage.success(`成功删除 ${selected.value.length} 条查看记录`)
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
.browsing-history {
  padding: 16px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.browsing-history .box-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c5aa0;
}

.card-header::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #163fa0 0%, #2c5aa0 100%);
  border-radius: 2px;
  margin-right: 10px;
}

.card-header .el-button--danger {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  font-weight: 500;
}

.card-header .el-button--danger:hover {
  background: linear-gradient(135deg, #c53030 0%, #9c2626 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(229, 62, 62, 0.3);
}

.pagination-container {
  margin-top: 25px;
  text-align: center;
}

.pagination-container :deep(.el-pagination__total),
.pagination-container :deep(.el-pagination__sizes),
.pagination-container :deep(.el-pagination__jump) {
  color: #5a6c7d;
}

.pagination-container :deep(.el-pager li) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  margin: 0 2px;
  border: 1px solid #e1f0ff;
}

.pagination-container :deep(.el-pager li:hover),
.pagination-container :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  color: white;
  border-color: #16a085;
}

.pagination-container :deep(.btn-prev),
.pagination-container :deep(.btn-next) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  border: 1px solid #e1f0ff;
}

.pagination-container :deep(.btn-prev:hover),
.pagination-container :deep(.btn-next:hover) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  color: white;
}

.item-link {
  color: #2c5aa0;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.item-link:hover {
  color: #16a085;
  text-decoration: underline;
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

:deep(.el-table__border) {
  border-color: #e1f0ff;
}

:deep(.el-table::before),
:deep(.el-table__fixed-right::before),
:deep(.el-table__fixed::before) {
  background-color: #e1f0ff;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background: linear-gradient(135deg, #16a085 0%, #2c5aa0 100%);
  border-color: #16a085;
}

:deep(.el-checkbox__input:not(.is-disabled):hover .el-checkbox__inner) {
  border-color: #16a085;
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
  color: #5a6c7d;
  line-height: 1.6;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.dialog-footer .el-button {
  border-radius: 20px;
  padding: 10px 20px;
  font-weight: 500;
}

.dialog-footer .el-button--danger {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  border: none;
}

.dialog-footer .el-button--danger:hover {
  background: linear-gradient(135deg, #c53030 0%, #9c2626 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(229, 62, 62, 0.3);
}

@media (max-width: 768px) {
  .browsing-history {
    padding: 15px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  :deep(.el-card__header) {
    padding: 15px 20px;
  }
  
  :deep(.el-card__body) {
    padding: 20px;
  }
  
  :deep(.el-table) {
    font-size: 0.85rem;
  }
  
  .pagination-container {
    margin-top: 20px;
    padding: 0 10px;
  }
}
</style> 