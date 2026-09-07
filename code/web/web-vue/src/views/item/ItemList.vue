<template>
  <div class="item-list">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="title-text">病例浏览</span>
        </div>
      </template>

      <div class="search-area">
        <el-form :model="queryForm" inline>
          <el-form-item label="病例名称">
            <el-input v-model="queryForm.title" placeholder="输入病例名称" @keyup.enter="handleSearch"/>
          </el-form-item>
          <el-form-item label="所属科室">
            <el-select
              v-model="queryForm.categoryId"
              placeholder="请选择科室"
              clearable
              style="width: 150px;"
              @keyup.enter="handleSearch"
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
            <el-input v-model="queryForm.tag" placeholder="输入症状标签" @keyup.enter="handleSearch"/>
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

      <div class="item-list-container">
        <div
          v-for="item in items"
          :key="item.id"
          class="item-row"
          @click="handleItemClick(item)"
        >
          <div class="item-thumb">
            <el-image
              v-if="item.coverUrl"
              :src="item.coverUrl"
              fit="cover"
              class="item-thumb-img"
            />
            <div v-else class="no-thumb">
              <el-icon><Picture /></el-icon>
            </div>
          </div>
          <div class="item-body">
            <div class="item-row-header">
              <h3 class="item-title">{{ item.title }}</h3>
              <el-tag type="info" effect="plain" size="small">{{ item.category.name }}</el-tag>
            </div>
            <p class="item-desc">{{ item.description }}</p>
            <div class="item-row-tags">
              <el-tag
                v-for="tag in (item as any).tags
                  ? (item as any).tags.split(',').map((t: string) => t.trim()).filter((t: string) => t)
                  : []"
                :key="tag"
                size="small"
                type="success"
                class="tag"
                round
              >
                {{ tag }}
              </el-tag>
              <span
                v-if="!(item as any).tags
                  || (item as any).tags.split(',').map((t: string) => t.trim()).filter((t: string) => t).length === 0"
                class="no-tags"
              >
                暂无症状标签
              </span>
            </div>
          </div>
          <div class="item-row-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <el-skeleton animated :rows="3" :loading="loading" />
      </div>

      <div v-if="!loading && items.length === 0" class="empty-container">
        <el-empty description="暂无病例数据" />
      </div>

      <el-pagination
        v-if="!loading && items.length > 0"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 30, 40]"
        :total="pagination.itemCount"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageSizeChange"
        @current-change="handlePageChange"
        class="pagination"
      />
    </el-card>

    <div class="image-viewer-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { itemApi } from '@/api/item'
import { categoryApi } from '@/api/category'
import type { ItemVO, ItemQueryDTO, CategoryVO } from '@/types/item'
import { Picture, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()
const items = ref<ItemVO[]>([])
const loading = ref(false)
const categories = ref<CategoryVO[]>([])

const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0
})

const queryForm = reactive<ItemQueryDTO>({
  title: '',
  categoryId: undefined,
  tag: '',
  current: 1,
  size: 10
})

const categoryOptions = computed(() => {
  return categories.value.map(item => ({
    label: item.name,
    value: item.id
  }))
})

const fetchItems = async () => {
  try {
    loading.value = true
    queryForm.current = pagination.page
    queryForm.size = pagination.pageSize
    const res = await itemApi.page(queryForm)
    console.log('获取病例列表', res)
    items.value = res.records || []
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
    const res = await categoryApi.list()
    categories.value = res || []
  } catch (error) {
    console.error('获取科室列表失败', error)
    ElMessage.error('获取科室列表失败')
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchItems()
}

const resetSearch = () => {
  queryForm.title = ''
  queryForm.categoryId = undefined
  queryForm.tag = ''
  pagination.page = 1
  fetchItems()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchItems()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize
  pagination.page = 1
  fetchItems()
}

const handleItemClick = (item: ItemVO) => {
  router.push({
    name: 'UserItemDetail',
    params: { id: item.id }
  })
}

onMounted(() => {
  const { keyword, categoryId, tag } = router.currentRoute.value.query;
  
  if (keyword) {
    queryForm.title = decodeURIComponent(keyword as string);
  }
  
  if (categoryId && !isNaN(Number(categoryId))) {
    queryForm.categoryId = Number(categoryId);
  }
  
  if (tag) {
    queryForm.tag = decodeURIComponent(tag as string);
  }
  
  fetchItems();
  fetchCategories();
})
</script>

<style scoped>
.item-list {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  min-height: calc(100vh - 170px);
}

.box-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(44, 90, 160, 0.08);
  border: 1px solid #e1f0ff;
  background: white;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.title-text {
  display: flex;
  align-items: center;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c5aa0;
  position: relative;
}

.title-text::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #09a3f0 0%, #2c5aa0 100%);
  border-radius: 2px;
  margin-right: 10px;
  flex-shrink: 0;
}

.search-area {
  margin-bottom: 16px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
  border-radius: 12px;
  border: 1px solid #e1f0ff;
}

.search-area .el-form-item__label {
  color: #2c5aa0;
  font-weight: 500;
}

.search-area .el-button--primary {
  background: linear-gradient(135deg, #d9cceb 0%, #2c5aa0 100%);
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  font-weight: 500;
}

.search-area .el-button--primary:hover {
  background: linear-gradient(135deg, #0940f5 0%, #1e4d8c 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(24, 63, 220, 0.3);
}

.search-area .el-button {
  border-radius: 20px;
  padding: 8px 20px;
  font-weight: 500;
}

.item-list-container {
  display: flex;
  flex-direction: column;
}

.item-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #e8eaed;
  cursor: pointer;
  transition: background 0.2s ease;
}

.item-row:hover {
  background: #f5f8ff;
}

.item-row:last-child {
  border-bottom: none;
}

.item-thumb {
  flex-shrink: 0;
  width: 100px;
  height: 75px;
  border-radius: 8px;
  overflow: hidden;
  background: linear-gradient(135deg, #f8fbff 0%, #f0f8ff 100%);
}

.item-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-thumb {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #bbb;
  font-size: 24px;
}

.item-body {
  flex: 1;
  min-width: 0;
}

.item-row-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.item-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #2c5aa0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-desc {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: #5a6c7d;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-row-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.tag {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #106ae0;
  border: 1px solid #e7f1ef;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.tag.el-tag--success {
  background: linear-gradient(135deg, #e8f5e8 0%, #d5f2d5 100%);
  color: #104bd4;
  border-color: #bbc7cb;
}

.no-tags {
  color: #aaa;
  font-size: 12px;
  font-style: italic;
}

.item-row-arrow {
  flex-shrink: 0;
  color: #bbb;
  font-size: 16px;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.empty-container {
  padding: 60px 0;
}

.ml-4 {
  margin-left: 16px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.pagination :deep(.el-pagination__total),
.pagination :deep(.el-pagination__sizes),
.pagination :deep(.el-pagination__jump) {
  color: #5a6c7d;
}

.pagination :deep(.el-pager li) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  margin: 0 2px;
  border: 1px solid #e1f0ff;
}

.pagination :deep(.el-pager li:hover),
.pagination :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #107fda 0%, #2c5aa0 100%);
  color: white;
  border-color: #0e30ca;
}

.pagination :deep(.btn-prev),
.pagination :deep(.btn-next) {
  background-color: white;
  color: #2c5aa0;
  border-radius: 6px;
  border: 1px solid #e1f0ff;
}

.pagination :deep(.btn-prev:hover),
.pagination :deep(.btn-next:hover) {
  background: linear-gradient(135deg, #0783dc 0%, #2c5aa0 100%);
  color: white;
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

@media (max-width: 768px) {
  .item-list {
    padding: 12px;
  }

  .search-area {
    padding: 12px;
  }

  .item-row {
    padding: 12px;
    gap: 12px;
  }

  .item-thumb {
    width: 72px;
    height: 54px;
  }

  .item-title {
    font-size: 0.95rem;
  }

  .item-desc {
    font-size: 0.8rem;
  }
}
</style> 