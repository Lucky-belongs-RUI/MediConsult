export interface WebSocketMessage {
  type: 'fire_detected' | 'camera_status' | 'frame' | 'start_stream' | 'stop_stream' | 'check_camera' | 'stream_stopped'
  data: {
    wsId?: string
    cameraId: number
    rtspUrl?: string
    frame?: string
    status?: number
    has_fire?: boolean
    has_smoke?: boolean
    fire_confidence?: number
    smoke_confidence?: number
    fire_bbox?: number[]
    smoke_bbox?: number[]
    level?: number
    location?: string
    [key: string]: any
  }
}

const WS_URL = import.meta.env.VITE_ALGO_WS_URL || `ws://${window.location.hostname}:5000/ws`

class WebSocketClient {
  private ws: WebSocket | null = null
  private url: string
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectTimeout = 3000
  private messageHandlers: ((message: WebSocketMessage) => void)[] = []
  private isActiveClose = false
  private reconnectTimer: number | null = null
  private messageQueue: any[] = []
  private isConnecting = false

  constructor(url: string) {
    this.url = url
    console.log('WebSocket URL:', url)
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket已经连接')
      this.processMessageQueue()
      return
    }

    if (this.ws?.readyState === WebSocket.CONNECTING || this.isConnecting) {
      console.log('WebSocket正在连接中')
      return
    }

    this.cleanup()

    this.isActiveClose = false
    this.isConnecting = true
    console.log('正在连接WebSocket:', this.url)

    try {
      this.ws = new WebSocket(this.url)

      this.ws.onopen = () => {
        console.log('WebSocket连接成功')
        this.reconnectAttempts = 0
        this.clearReconnectTimer()
        this.isConnecting = false
        this.processMessageQueue()
      }

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          this.messageHandlers.forEach(handler => handler(message))
        } catch (error) {
          console.error('WebSocket消息解析失败:', error)
        }
      }

      this.ws.onclose = (event) => {
        console.log('WebSocket连接关闭:', {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
          isActiveClose: this.isActiveClose
        })

        this.isConnecting = false

        if (!this.isActiveClose && !event.wasClean) {
          this.scheduleReconnect()
        } else {
          console.log('WebSocket正常关闭，不进行重连')
          this.cleanup()
        }
      }

      this.ws.onerror = (event) => {
        this.isConnecting = false
        if (import.meta.env.DEV) {
          console.error('WebSocket错误:', event)
        }
        console.error('WebSocket连接出错')
      }
    } catch (error) {
      this.isConnecting = false
      console.error('创建WebSocket连接失败:', error)
      this.scheduleReconnect()
    }
  }

  private processMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift()
      this.sendImmediate(message)
    }
  }

  private sendImmediate(message: any) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('WebSocket未连接，消息发送失败')
      return
    }

    try {
      this.ws.send(JSON.stringify(message))
    } catch (error) {
      console.error('发送消息失败:', error)
    }
  }

  send(message: any) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.log('WebSocket未连接，将消息加入队列并尝试连接')
      this.messageQueue.push(message)
      this.connect()
      return
    }

    this.sendImmediate(message)
  }

  private cleanup() {
    if (this.ws) {
      this.ws.onopen = null
      this.ws.onclose = null
      this.ws.onmessage = null
      this.ws.onerror = null

      if (this.ws.readyState === WebSocket.OPEN) {
        try {
          this.ws.close(1000, 'Normal closure')
        } catch (error) {
          console.error('关闭WebSocket连接失败:', error)
        }
      }

      this.ws = null
    }

    this.clearReconnectTimer()
  }

  private clearReconnectTimer() {
    if (this.reconnectTimer) {
      window.clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('WebSocket重连次数超过最大限制')
      this.cleanup()
      return
    }

    this.reconnectAttempts++
    console.log('WebSocket计划第' + this.reconnectAttempts + '次重连')

    this.clearReconnectTimer()
    this.reconnectTimer = window.setTimeout(() => {
      console.log('执行重连...')
      this.connect()
    }, this.reconnectTimeout)
  }

  addMessageHandler(handler: (message: WebSocketMessage) => void) {
    this.messageHandlers.push(handler)
  }

  removeMessageHandler(handler: (message: WebSocketMessage) => void) {
    const index = this.messageHandlers.indexOf(handler)
    if (index !== -1) {
      this.messageHandlers.splice(index, 1)
    }
  }

  close() {
    console.log('主动关闭WebSocket连接')
    this.isActiveClose = true
    this.cleanup()
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }
}

const wsClient = new WebSocketClient(WS_URL)

export default wsClient 