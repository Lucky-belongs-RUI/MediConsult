import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

export const getMultiLineChartOptions = (
  xData: string[],
  series: Array<{
    name: string
    data: number[]
    color: string
  }>
): EChartsOption => {
  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: series.map(item => item.name)
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: xData
    },
    yAxis: {
      type: 'value'
    },
    series: series.map(item => ({
      name: item.name,
      type: 'line',
      smooth: true,
      data: item.data,
      itemStyle: {
        color: item.color
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: item.color.replace(')', ', 0.3)')
          },
          {
            offset: 1,
            color: item.color.replace(')', ', 0.1)')
          }
        ])
      }
    }))
  }
}

export const getPieChartOptions = (
  data: Array<{
    name: string
    value: number
    color?: string
  }>,
  title?: string
): EChartsOption => {
  return {
    title: title ? {
      text: title,
      left: 'center'
    } : undefined,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: '70%',
        data: data.map(item => ({
          ...item,
          itemStyle: item.color ? { color: item.color } : undefined
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
}

export const getBarChartOptions = (
  xData: string[],
  series: Array<{
    name: string
    data: number[]
    color?: string
  }>,
  title?: string
): EChartsOption => {
  return {
    title: title ? {
      text: title,
      left: 'center'
    } : undefined,
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: series.map(item => item.name)
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: xData
    },
    yAxis: {
      type: 'value'
    },
    series: series.map(item => ({
      name: item.name,
      type: 'bar',
      data: item.data,
      itemStyle: item.color ? { color: item.color } : undefined
    }))
  }
}

export const getDoughnutChartOptions = (
  data: Array<{
    name: string
    value: number
    color?: string
  }>,
  title?: string
): EChartsOption => {
  return {
    title: title ? {
      text: title,
      left: 'center'
    } : undefined,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map(item => ({
          ...item,
          itemStyle: item.color ? { color: item.color } : undefined
        }))
      }
    ]
  }
} 