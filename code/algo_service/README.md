# 算法端（Python FastAPI）

本服务模拟医疗问诊场景下的算法能力，包括：

- LLM 模型列表与问答能力（支持可选 RAG、图片信息占位）
- 向量检索索引的构建、查询及删除
- 问诊与病例文档生成与下载
- 文件管理（上传 / 下载 / 删除，由原独立文件服务合并而来）
- 健康检查接口

## 目录结构

```
algo_service/
├── app/
│   ├── config.py            # 全局配置
│   ├── routes/              # FastAPI 路由
│   └── services/            # 业务服务（LLM、向量、文档等）
├── data/                    # 自动创建的索引存储目录
├── main.py                  # 应用入口
└── requirements.txt         # Python 依赖
```

## 快速启动

1. 创建虚拟环境并安装依赖：

```bash
cd /Users/rui/Desktop/Medical_Consultation/code/algo_service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 启动服务（默认端口 5000，对应前端 `/algo` 代理到 `http://localhost:5000`）：

```bash
uvicorn main:app --reload --port 5000
```

## 环境变量（可选）

| 变量 | 说明 | 默认值 |
| ---- | ---- | ------ |
| `SPRINGBOOT_API_BASE` | Java 后端 API 网关地址 | `http://localhost:8090/api` |
| `FILE_SERVICE_BASE` | 文件接口对外地址（合并后即本服务自身地址） | `http://localhost:5000` |
| `ALGO_DATA_DIR` | 索引等数据存储路径 | `<project>/algo_service/data` |
| `ALGO_DOCS_DIR` | 文档存储路径 | `<project>/algo_service/data/docs` |
| `FILE_STORAGE_ROOT` | 文件存储根目录 | `<project>/algo_service/data/files` |
| `ALIYUN_API_KEY` | 调用阿里云通义千问所需的 API Key | `None`（必须手动配置） |
| `ALIYUN_MODEL` | 默认使用的模型名称 | `qwen-plus` |
| `ALIYUN_API_BASE` | OpenAI 兼容协议的网关地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `ALIYUN_TIMEOUT` | 请求阿里云服务的超时时间（秒） | `30` |

> 配置示例（Mac / Linux）：
>
> ```bash
> export ALIYUN_API_KEY="sk-xxxx"
> export ALIYUN_MODEL="qwen-plus"
> uvicorn main:app --reload --port 5000
> ```
>
> 当 `ALIYUN_API_KEY` 生效时，`/llm/chat` 将自动通过 API Key 调用阿里云大模型；若未配置或调用失败，则回退到内置的示例回答逻辑，便于本地联调。

## 主要接口

| 方法 | 路径 | 说明 |
| ---- | ---- | ---- |
| GET | `/health/health_check` | 健康检查 |
| GET | `/llm/models` | 获取可用模型列表 |
| POST | `/llm/chat` | 生成问答响应（支持 RAG） |
| GET | `/vector-index/status` | 查询索引状态 |
| POST | `/vector-index/create` | 构建索引（自动拉取后端病例，或使用内置示例） |
| DELETE | `/vector-index/delete` | 删除索引 |
| POST | `/vector-index/search` | 检索相似病例 |
| POST | `/document/generate-case-document` | 生成病例文档 |
| POST | `/document/generate-chat-document` | 生成问诊对话文档 |
| GET | `/document/download/{objectKey}` | 下载生成的文档 |
| GET | `/file/health` | 文件接口健康检查 |
| POST | `/file/upload/{bucket}` | 上传文件（multipart/form-data，`file` 字段） |
| GET | `/file/{bucket}/{objectKey}` | 下载文件 |
| DELETE | `/file/{bucket}/{objectKey}` | 删除文件 |

所有接口均返回 `{ code, msg, data }` 格式，与前端 `algoRequest` / `fileRequest` 保持一致。
