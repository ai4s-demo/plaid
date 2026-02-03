# Smart Campaign Designer 开发单元定义

## 概述

基于应用设计，系统分解为以下开发单元。由于这是一个中小型项目，采用**单体应用 + 模块化**架构，所有后端代码在一个 Python 项目中，前端为独立的 React 项目。

---

## 单元划分

```
smart-campaign-designer/
├── frontend/          # Unit 1: 前端 (React)
└── backend/           # Unit 2: 后端 (FastAPI + OR-Tools)
```

---

## Unit 1: 前端 (Frontend)

**类型**: 独立部署单元  
**技术栈**: React + TypeScript  
**职责**: 用户界面、对话交互、可视化、文件下载

### 模块划分

| 模块 | 职责 | 主要组件 |
|------|------|----------|
| Chat | 对话交互 | ChatPanel, MessageList, MessageInput |
| Upload | 文件上传 | FileUpload, FilePreview |
| Plate | 板布局可视化 | PlateView, Well, Legend, WellTooltip |
| Download | 输出下载 | DownloadPanel, PDFGenerator |
| Common | 共享组件 | Layout, Header, Loading, ErrorBoundary |

### 目录结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatPanel.tsx
│   │   │   ├── MessageList.tsx
│   │   │   └── MessageInput.tsx
│   │   ├── upload/
│   │   │   └── FileUpload.tsx
│   │   ├── plate/
│   │   │   ├── PlateView.tsx
│   │   │   ├── Well.tsx
│   │   │   └── Legend.tsx
│   │   ├── download/
│   │   │   └── DownloadPanel.tsx
│   │   └── common/
│   │       └── Layout.tsx
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useSSE.ts
│   │   └── usePlate.ts
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── package.json
└── vite.config.ts
```

### 依赖

| 依赖 | 用途 |
|------|------|
| react | UI 框架 |
| @dnd-kit/core | 拖拽功能 |
| jspdf | PDF 生成 |
| axios | HTTP 请求 |

---

## Unit 2: 后端 (Backend)

**类型**: 独立部署单元  
**技术栈**: Python + FastAPI + OR-Tools  
**职责**: API 服务、AI Agent、文件解析、约束求解

### 模块划分

| 模块 | 职责 | 主要文件 |
|------|------|----------|
| api | REST API 端点 | routers/*.py |
| agent | AI Agent 服务 | services/agent_service.py |
| file | 文件解析服务 | services/file_service.py |
| layout | 布局生成服务 | services/layout_service.py |
| solver | 约束求解器 | solver/constraint_solver.py |
| models | 数据模型 | models/*.py |

### 目录结构

```
backend/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── file.py
│   │   └── layout.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py
│   │   ├── file_service.py
│   │   └── layout_service.py
│   ├── solver/
│   │   ├── __init__.py
│   │   ├── constraint_solver.py
│   │   └── constraints.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── source_plate.py
│   │   ├── design_parameters.py
│   │   ├── plate_layout.py
│   │   └── picklist.py
│   ├── config.py
│   └── main.py
├── requirements.txt
└── README.md
```

### 依赖

| 依赖 | 用途 |
|------|------|
| fastapi | Web 框架 |
| uvicorn | ASGI 服务器 |
| boto3 | AWS Bedrock 客户端 |
| ortools | 约束求解器 |
| openpyxl | Excel 解析 |
| pandas | 数据处理 |
| python-multipart | 文件上传 |

---

## 开发顺序

基于依赖关系，推荐以下开发顺序：

```
1. Backend - Models (数据模型)
      ↓
2. Backend - Solver (约束求解器核心)
      ↓
3. Backend - Services (业务服务)
      ↓
4. Backend - API (REST 端点)
      ↓
5. Frontend - Common (基础组件)
      ↓
6. Frontend - Plate (可视化)
      ↓
7. Frontend - Chat (对话)
      ↓
8. Frontend - Upload + Download (文件处理)
      ↓
9. 集成测试
```

---

## 部署架构

```
┌─────────────────────────────────────────────────────────┐
│                    本地服务器                            │
│                                                         │
│  ┌─────────────────┐      ┌─────────────────────────┐  │
│  │   Nginx         │      │   Python Backend        │  │
│  │   (静态文件)    │ ───→ │   (FastAPI + Uvicorn)   │  │
│  │   Port: 80      │      │   Port: 8000            │  │
│  └─────────────────┘      └─────────────────────────┘  │
│          │                           │                  │
│          ▼                           ▼                  │
│  ┌─────────────────┐      ┌─────────────────────────┐  │
│  │ React Build     │      │ Amazon Bedrock          │  │
│  │ (静态资源)      │      │ (外部 API)              │  │
│  └─────────────────┘      └─────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 接口契约

### 前后端接口

| 端点 | 方法 | 请求 | 响应 |
|------|------|------|------|
| /api/chat | POST | ChatRequest | SSE Stream |
| /api/file/parse | POST | FormData (file) | SourcePlate |
| /api/layout/generate | POST | LayoutRequest | PlateLayout |
| /api/layout/update | PUT | UpdateRequest | PlateLayout |
| /api/layout/picklist | POST | PlateLayout | PicklistEntry[] |
