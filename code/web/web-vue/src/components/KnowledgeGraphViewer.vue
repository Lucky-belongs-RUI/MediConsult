<template>
  <el-dialog
    :model-value="visible"
    title="知识图谱可视化"
    width="86%"
    top="4vh"
    :close-on-click-modal="false"
    destroy-on-close
    @update:model-value="emit('update:visible', $event)"
    @open="handleOpen"
    @closed="handleClosed"
  >
    <div v-loading="loading" class="kg-viewer">
      <div class="kg-stats" v-if="graphData && graphData.node_count > 0">
        <el-tag type="success">节点 {{ graphData.total_node_count }}</el-tag>
        <el-tag type="primary">关系 {{ graphData.total_edge_count }}</el-tag>
        <el-tag type="warning">类别 {{ graphData.categories.length }}</el-tag>
        <span class="truncate-hint" v-if="graphData.node_count < graphData.total_node_count">
          图谱较大，当前展示度数最高的 {{ graphData.node_count }} 个节点 / {{ graphData.edge_count }} 条关系
        </span>
        <span class="drag-hint">可拖拽节点、滚轮缩放查看</span>
      </div>

      <div ref="chartEl" class="kg-chart" v-show="graphData && graphData.node_count > 0"></div>

      <el-empty
        v-if="!loading && graphData && graphData.node_count === 0"
        description="暂无图谱数据，请先构建知识图谱"
      />
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { knowledgeGraphApi, type KnowledgeGraphData } from '@/api/vector'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const loading = ref(false)
const graphData = ref<KnowledgeGraphData | null>(null)
const chartEl = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

const COLOR_PALETTE = [
  '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
  '#9C27B0', '#00BCD4', '#FF9800', '#4CAF50', '#3F51B5',
  '#E91E63', '#8BC34A', '#795548', '#607D8B', '#FF5722'
]

const fetchGraph = async () => {
  loading.value = true
  try {
    graphData.value = await knowledgeGraphApi.getGraph()
    if (graphData.value && graphData.value.node_count > 0) {
      await nextTick()
      renderChart()
    }
  } catch (error) {
    console.error('获取知识图谱数据失败:', error)
    ElMessage.error('获取知识图谱数据失败')
  } finally {
    loading.value = false
  }
}

const renderChart = () => {
  if (!chartEl.value || !graphData.value) return

  if (chart) {
    chart.dispose()
  }
  chart = echarts.init(chartEl.value)

  const data = graphData.value
  const categoryMap = new Map<string, number>()
  data.categories.forEach((cat, index) => {
    categoryMap.set(cat, index)
  })

  const nodes = data.nodes.map(node => ({
    id: node.id,
    name: node.name,
    category: categoryMap.get(node.category) ?? 0,
    symbolSize: Math.min(60, 12 + node.degree * 2),
    value: node.degree,
    label: { show: true, fontSize: 11 }
  }))

  const links = data.edges.map(edge => ({
    source: edge.source,
    target: edge.target,
    label: edge.label ? {
      show: true,
      fontSize: 10,
      formatter: edge.label,
      color: '#606266'
    } : { show: false }
  }))

  chart.setOption({
    color: COLOR_PALETTE,
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          return `<b>${params.name}</b><br/>类别：${data.categories[params.category] || '-'}<br/>关联度：${params.value ?? 0}`
        }
        if (params.dataType === 'edge' && params.data.label) {
          return `${params.data.source.split('::').pop()} — ${params.data.label.formatter || ''} — ${params.data.target.split('::').pop()}`
        }
        return ''
      }
    },
    legend: {
      top: 0,
      data: data.categories,
      textStyle: { fontSize: 12 },
      type: 'scroll'
    },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      data: nodes,
      links,
      categories: data.categories.map(name => ({ name })),
      label: {
        show: true,
        position: 'right',
        fontSize: 11,
        color: '#303133'
      },
      edgeLabel: {
        show: false
      },
      emphasis: {
        focus: 'adjacency',
        label: { show: true, fontSize: 13, fontWeight: 'bold' },
        lineStyle: { width: 3 }
      },
      force: {
        repulsion: 300,
        edgeLength: [60, 180],
        gravity: 0.08,
        layoutAnimation: true
      },
      lineStyle: {
        color: 'source',
        curveness: 0.08,
        opacity: 0.7,
        width: 1.4
      }
    }]
  })

  window.addEventListener('resize', handleResize)
}

const handleResize = () => {
  chart?.resize()
}

const handleOpen = () => {
  fetchGraph()
}

const handleClosed = () => {
  window.removeEventListener('resize', handleResize)
  if (chart) {
    chart.dispose()
    chart = null
  }
  graphData.value = null
}
</script>

<style scoped>
.kg-viewer {
  min-height: 420px;
  position: relative;
}

.kg-stats {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.truncate-hint,
.drag-hint {
  font-size: 12px;
  color: #909399;
}

.drag-hint {
  margin-left: auto;
}

.kg-chart {
  width: 100%;
  height: 66vh;
  min-height: 420px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fafbfc;
}
</style>
