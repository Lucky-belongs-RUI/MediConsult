export const validatePhone = (phone: string) => {
  const reg = /^1[3-9]\d{9}$/
  return reg.test(phone)
}

export const validateEmail = (email: string) => {
  const reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
  return reg.test(email)
}

export const validatePassword = (password: string) => {
  const reg = /^[a-zA-Z0-9]{6,20}$/
  return reg.test(password)
}

export const validateUsername = (username: string) => {
  const reg = /^[a-zA-Z0-9_-]{4,16}$/
  return reg.test(username)
}

export const validateIP = (ip: string) => {
  return /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$/.test(ip)
}

export const validateRTSP = (rtsp: string) => {
  return /^rtsp:\/\/[^\s]*$/.test(rtsp)
}

export const validateImageType = (type: string) => {
  return ['image/jpeg', 'image/png', 'image/gif'].includes(type)
}

export const validateVideoType = (type: string) => {
  return ['video/mp4'].includes(type)
}

export const validateFileSize = (size: number, maxSize: number) => {
  return size <= maxSize * 1024 * 1024
} 