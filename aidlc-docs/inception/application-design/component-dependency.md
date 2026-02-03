# Smart Campaign Designer 组件依赖设计

## 依赖关系图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              前端 (React)                                │
│                                                                         │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌────────────┐  │
│  │ChatPanel │ ───→ │PlateView │ ───→ │Download  │      │ Parameter  │  │
│  │          │      │  (SVG)   │      │  Panel   │      │   Panel    │  │
│  └────┬─────┘      └────┬─────┘      └────┬─────┘      └─────┬──────┘  │
│       │                 │                 │                   │         │
│       └────────┬────────┴────────┬────────┴───────────────────┘         │
│                │                 │                                       │
│                ▼                 ▼                                       │
│         ┌─────────────────────────────────┐                             │
│         │         API Client              │                             │
│         │   (Axios + EventSource)         │                             │
│         └───────────────┬─────────────────┘                             │
└─────────────────────────┼───────────────────────────────────────────────┘
                          │
                          │ HTTP (REST + SSE)
                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            后端 (FastAPI)                                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      API Router Layer                            │   │
│  │   /api/chat    /api/file/parse    /api/layout/generate          │   │
│  └───────────────────────────┬─────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    AgentOrchestrator                             │   │
│  │                    (主编排服务)                                   │   │
│  └───────┬───────────────────┬───────────────────┬─────────────────┘   │
│          │                   │                   │                      │
│          ▼                   ▼                   ▼                      │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐             │
│  │ AgentService  │   │ FileService   │   │LayoutService  │             │
│  │               │   │               │   │               │             │
│  │ ┌───────────┐ │   │ ┌───────────┐ │   │ ┌───────────┐ │             │
│  │ │ Bedrock   │ │   │ │ openpyxl  │ │   │ │ OR-Tools  │ │             │
│  │ │ Client    │ │   │ │ pandas    │ │   │ │ CP-SAT    │ │             │
│  │ └───────────┘ │   │ └───────────┘ │   │ └───────────┘ │             │
│  └───────────────┘   └───────────────┘   └───────────────┘             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         外部服务                                         │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    Amazon Bedrock (Claude)                         │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 依赖矩阵

### 前端组件依赖

| 组件 | 依赖 | 依赖类型 |
|------|------|----------|
| ChatPanel | API Client | 数据通信 |
| ChatPanel | PlateView | 布局展示 |
| ChatPanel | ParameterPanel | 参数显示 |
| FileUpload | API Client | 文件上传 |
| PlateView | react-dnd | 拖拽功能 |
| PlateView | Layout 数据 | 渲染数据 |
| DownloadPanel | jsPDF | PDF 生成 |
| DownloadPanel | PlateView | SVG 导出 |

### 后端服务依赖

| 服务 | 依赖 | 依赖类型 |
|------|------|----------|
| AgentOrchestrator | AgentService | 服务调用 |
| AgentOrchestrator | FileService | 服务调用 |
| AgentOrchestrator | LayoutService | 服务调用 |
| AgentService | boto3 (Bedrock) | 外部 API |
| FileService | openpyxl | 库依赖 |
| FileService | pandas | 库依赖 |
| LayoutService | ConstraintSolver | 模块依赖 |
| ConstraintSolver | ortools | 库依赖 |

---

## 数据流

### 1. 对话流程数据流

```
用户输入 (文本)
    │
    ▼
┌─────────────┐
│ ChatPanel   │ ──→ POST /api/chat
└─────────────┘         │
                        ▼
              ┌─────────────────┐
              │AgentOrchestrator│
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   AgentService   FileService   LayoutService
         │             │             │
         ▼             │             │
   Bedrock Claude      │             │
         │             │             │
         └─────────────┴─────────────┘
                       │
                       ▼
              SSE 流式响应
                       │
                       ▼
              ┌─────────────┐
              │ ChatPanel   │ ──→ 更新 UI
              └─────────────┘
```

### 2. 文件上传数据流

```
用户选择文件
    │
    ▼
┌─────────────┐
│ FileUpload  │ ──→ POST /api/file/parse
└─────────────┘         │
                        ▼
              ┌─────────────────┐
              │  FileService    │
              │  (内存解析)     │
              └────────┬────────┘
                       │
                       ▼
              SourcePlate 数据
                       │
                       ▼
              ┌─────────────┐
              │ ChatPanel   │ ──→ 存储到 Context
              └─────────────┘
```

### 3. 布局生成数据流

```
设计参数 + 源板数据
    │
    ▼
┌─────────────────┐
│ AgentOrchestrator│ ──→ LayoutService.generate()
└─────────────────┘         │
                            ▼
                  ┌─────────────────┐
                  │ConstraintSolver │
                  │  (OR-Tools)     │
                  └────────┬────────┘
                           │
                           ▼
                  PlateLayout 数据
                           │
                           ▼
                  ┌─────────────┐
                  │ PlateView   │ ──→ SVG 渲染
                  └─────────────┘
```

### 4. Picklist 生成数据流

```
PlateLayout + SourcePlate
    │
    ▼
┌─────────────────┐
│ LayoutService   │ ──→ generate_picklist()
└────────┬────────┘
         │
         ▼
List[PicklistEntry]
         │
         ▼
┌─────────────────┐
│ DownloadPanel   │ ──→ CSV 文件下载
└─────────────────┘
```

---

## 通信协议

### REST API

| 端点 | 方法 | 请求体 | 响应 |
|------|------|--------|------|
| /api/chat | POST | ChatRequest | SSE Stream |
| /api/file/parse | POST | multipart/form-data | SourcePlate |
| /api/layout/generate | POST | LayoutRequest | PlateLayout |
| /api/layout/update | PUT | UpdateRequest | PlateLayout |
| /api/layout/picklist | POST | PlateLayout | List[PicklistEntry] |

### SSE 事件格式

```
event: message
data: {"type": "text", "content": "正在分析您的需求..."}

event: message
data: {"type": "parameters", "content": {"plate_type": 96, ...}}

event: message
data: {"type": "layout", "content": {...PlateLayout...}}

event: done
data: {}
```

---

## 错误处理

### 前端错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 网络错误 | 显示重试按钮 |
| 文件格式错误 | 显示错误提示 |
| SSE 断开 | 自动重连 |

### 后端错误处理

| 错误类型 | HTTP 状态码 | 响应 |
|----------|-------------|------|
| 文件格式不支持 | 400 | {"error": "Unsupported file format"} |
| 文件解析失败 | 422 | {"error": "Failed to parse file", "details": ...} |
| 约束无解 | 422 | {"error": "No solution found", "constraints": ...} |
| Bedrock 错误 | 503 | {"error": "AI service unavailable"} |
