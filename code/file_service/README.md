# 文件端（Python FastAPI）

提供前端 `fileRequest` 所需的文件上传、下载与删除能力，接口完全匹配 `{ code, msg, data }` 的约定。

## 启动步骤

```bash
cd /Users/rui/Desktop/Medical_Consultation/code/file_service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5001
```

## 主要接口

| 方法 | 路径 | 说明 |
| ---- | ---- | ---- |
| GET | `/health` | 健康检查 |
| POST | `/file/upload/{bucket}` | 上传文件（multipart/form-data） |
| GET | `/file/{bucket}/{objectKey}` | 下载文件 |
| DELETE | `/file/{bucket}/{objectKey}` | 删除文件 |

上传成功将返回：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "url": "http://localhost:8001/file/<bucket>/<objectKey>",
    "bucket": "...",
    "objectKey": "..."
  }
}
```

`objectKey` 由服务端自动生成（带时间戳+UUID），本地文件默认保存在 `file_service/storage` 目录，可通过环境变量 `FILE_STORAGE_ROOT` 自定义。
