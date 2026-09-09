# 医疗问诊平台（Medical Consultation Platform）

前后端分离的**多服务医疗问诊系统**：Java Spring Boot 提供业务 API；Python 算法服务提供大模型问诊问答（支持 RAG 向量检索增强、知识图谱、问诊 / 病例文档生成）并统一管理图片、附件等文件的上传下载；Vue 3 前端提供问诊对话、健康内容浏览、收藏点赞评论、用户中心与管理后台。

> 本项目为演示 / 学习用途，内置的问答能力在未配置大模型 API Key 时会自动回退到示例回答，便于本地全流程联调。

## 核心功能

- **在线问诊对话**：LLM 生成回答，支持可选的 RAG 知识增强与图片占位
- **向量检索**：病例索引的构建、查询与删除，相似病例召回
- **文档生成**：问诊对话记录、病例文档生成与下载
- **内容社区**：健康条目分类浏览、收藏、点赞、评论
- **会话管理**：聊天会话与历史消息管理
- **用户体系**：注册 / 登录（JWT）、管理后台数据看板
- **文件管理**：算法服务内置文件上传、下载、删除（自动生成 objectKey）

## 技术栈与端口

| 服务 | 技术 | 默认端口 |
| ---- | ---- | ---- |
| `springboot` | Java 8 · Spring Boot 2.7.3 · MyBatis-Plus · MySQL · JWT · Swagger · PageHelper | 8090 |
| `algo_service` | Python 3.12 · FastAPI · 阿里云通义千问（OpenAI 兼容协议）· 内置文件管理 | 5000 |
| `web/web-vue` | Vue 3 · TypeScript · Vite 6 · Element Plus · ECharts · Pinia | 8080（开发服务器） |

前端 Vite 已配置代理：`/api` → `8090`、`/algo` → `5000`、`/file` → `5000`（文件接口已合并到算法服务）。

## 目录结构

```
Medical_Consultation/
├── code/
│   ├── springboot/          # Java 业务后端（用户/内容/聊天/互动）
│   ├── algo_service/        # Python 算法服务（LLM 问答/向量检索/文档生成/文件管理）
│   └── web/web-vue/         # Vue 3 前端
└── env/                     # 本地运行环境（如 nvm，勿提交）
```

## 环境要求

- **JDK** 8、**Maven** 3.6+
- **Python** 3.10+（推荐 3.12）
- **Node.js** 18+（推荐 20+）、npm 9+
- **MySQL** 5.7 / 8.0
- （可选）阿里云通义千问 API Key

## 快速开始

### 1. 初始化数据库

创建数据库 `medical`（默认连接 `jdbc:mysql://localhost:3306/medical`，账号 `root/root`，见 `springboot/src/main/resources/application.yml`，按需修改）。表结构由 MyBatis-Plus 实体与 Mapper 管理，请按 `entity/` 下的实体建表。

### 2. 启动 Spring Boot 业务后端（端口 8090）

```bash
cd code/springboot
mvn spring-boot:run
```

- Swagger 文档：<http://localhost:8090/swagger-ui.html>

### 3. 启动算法服务（端口 5000）

```bash
cd code/algo_service
python -m venv .venv
# Windows: .venv\Scripts\activate    Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 可选：配置阿里云通义千问（未配置时 /llm/chat 自动回退内置示例回答）
export ALIYUN_API_KEY="sk-xxxx"     # Windows PowerShell: $env:ALIYUN_API_KEY="sk-xxxx"

uvicorn main:app --reload --port 5000
```

### 4. 文件接口（已合并到算法服务）

文件上传、下载、删除接口已并入算法服务（端口 5000），无需再单独启动文件服务：

- 上传：`POST http://localhost:5000/api/file/upload/{bucket}`
- 下载：`GET http://localhost:5000/api/file/{bucket}/{objectKey}`
- 删除：`DELETE http://localhost:5000/api/file/{bucket}/{objectKey}`

文件默认保存在 `algo_service/data/files/`，可用环境变量 `FILE_STORAGE_ROOT` 自定义。

### 5. 启动前端（端口 8080）

```bash
cd code/web/web-vue
npm install
npm run dev
```

浏览器访问 <http://localhost:8080>。生产构建：`npm run build`。

## 配置说明

### 算法服务（`algo_service/config.env` 或环境变量）

| 变量 | 说明 | 默认值 |
| ---- | ---- | ------ |
| `SPRINGBOOT_API_BASE` | Java 后端网关地址 | `http://localhost:8090/api` |
| `FILE_SERVICE_BASE` | 文件接口对外地址（合并后即算法服务自身地址） | `http://localhost:5000` |
| `FILE_STORAGE_ROOT` | 文件存储根目录 | `<项目>/algo_service/data/files` |
| `ALIYUN_API_KEY` | 阿里云通义千问 API Key（必配才会调真实模型） | 无 |
| `ALIYUN_MODEL` | 默认模型 | `qwen-plus` |
| `ALGO_DATA_DIR` | 索引等数据存储路径 | `<项目>/algo_service/data` |

所有接口统一返回 `{ code, msg, data }` 结构，与前端约定一致。



## 开源声明

本项目仅用于**学习与交流**，**禁止任何形式的商业用途**。

任何使用、修改、二次开发或参考本项目的行为，必须注明出处并引用本项目仓库（GitHub：https://github.com/Lucky-belongs-RUI/MediConsult）。
