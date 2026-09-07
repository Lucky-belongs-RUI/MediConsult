export function formatDate(date: Date | string, format: string = 'YYYY-MM-DD HH:mm:ss'): string {
  if (!date) return '';
  
  const d = typeof date === 'string' ? new Date(date) : date
  if (isNaN(d.getTime())) return '';
  
  const year = d.getFullYear().toString()
  const month = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  const hours = d.getHours().toString().padStart(2, '0')
  const minutes = d.getMinutes().toString().padStart(2, '0')
  const seconds = d.getSeconds().toString().padStart(2, '0')
  
  return format
    .replace(/YYYY/g, year)
    .replace(/MM/g, month)
    .replace(/DD/g, day)
    .replace(/HH/g, hours)
    .replace(/mm/g, minutes)
    .replace(/ss/g, seconds)
}

export function relativeTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const months = Math.floor(days / 30)
  const years = Math.floor(months / 12)
  
  if (years > 0) {
    return `${years}年前`
  } else if (months > 0) {
    return `${months}个月前`
  } else if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}

export function formatCurrentTimeToMinute(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = (now.getMonth() + 1).toString().padStart(2, '0');
  const day = now.getDate().toString().padStart(2, '0');
  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

export function formatDateToMinute(date: string | Date): string {
  if (!date) return '';
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) return '';
  
  const year = dateObj.getFullYear();
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
  const day = dateObj.getDate().toString().padStart(2, '0');
  const hours = dateObj.getHours().toString().padStart(2, '0');
  const minutes = dateObj.getMinutes().toString().padStart(2, '0');
  
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

export function formatCurrentTimeToChineseDay(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  const hours = now.getHours();

  const period = hours < 12 ? '上午' : '下午';
  
  return `${year}年${month}月${day}日 ${period}`;
}

export function formatDateToChineseDay(date: string | Date): string {
  if (!date) return '';
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) return '';
  
  const year = dateObj.getFullYear();
  const month = dateObj.getMonth() + 1;
  const day = dateObj.getDate();
  const hours = dateObj.getHours();

  const period = hours < 12 ? '上午' : '下午';
  
  return `${year}年${month}月${day}日 ${period}`;
} 