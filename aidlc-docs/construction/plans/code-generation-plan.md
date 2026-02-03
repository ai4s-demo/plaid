# Smart Campaign Designer 代码生成计划

## 项目结构

```
smart-campaign-designer/
├── backend/                    # Python 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI 入口
│   │   ├── config.py          # 配置
│   │   ├── routers/           # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── file.py
│   │   │   └── layout.py
│   │   ├── services/          # 业务服务
│   │   │   ├── __init__.py
│   │   │   ├── agent_service.py
│   │   │   ├── file_service.py
│   │   │   └── layout_service.py
│   │   ├── solver/            # 约束求解器
│   │   │   ├── __init__.py
│   │   │   ├── constraint_solver.py
│   │   │   └── constraints.py
│   │   └── models/            # 数据模型
│   │       ├── __init__.py
│   │       ├── source_plate.py
│   │       ├── design_parameters.py
│   │       ├── plate_layout.py
│   │       └── picklist.py
│   ├── tests/                 # 测试
│   │   └── test_solver.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/                   # React 前端
    ├── src/
    │   ├── components/
    │   │   ├── ChatPanel.tsx
    │   │   ├── FileUpload.tsx
    │   │   ├── PlateView.tsx
    │   │   └── DownloadPanel.tsx
    │   ├── hooks/
    │   │   └── useChat.ts
    │   ├── services/
    │   │   └── api.ts
    │   ├── types/
    │   │   └── index.ts
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    ├── vite.config.ts
    └── README.md
```

---

## 代码生成步骤

### Backend 单元

#### Step 1: 项目结构和配置
- [x] 创建 backend/requirements.txt
- [x] 创建 backend/app/config.py
- [x] 创建 backend/app/__init__.py
- [x] 创建 backend/app/main.py (FastAPI 入口)

#### Step 2: 数据模型
- [x] 创建 backend/app/models/__init__.py
- [x] 创建 backend/app/models/source_plate.py
- [x] 创建 backend/app/models/design_parameters.py
- [x] 创建 backend/app/models/plate_layout.py
- [x] 创建 backend/app/models/picklist.py

#### Step 3: 约束求解器
- [x] 创建 backend/app/solver/__init__.py
- [x] 创建 backend/app/solver/constraints.py (约束定义)
- [x] 创建 backend/app/solver/constraint_solver.py (求解器核心)

#### Step 4: 业务服务
- [x] 创建 backend/app/services/__init__.py
- [x] 创建 backend/app/services/file_service.py
- [x] 创建 backend/app/services/layout_service.py
- [x] 创建 backend/app/services/agent_service.py

#### Step 5: API 路由
- [x] 创建 backend/app/routers/__init__.py
- [x] 创建 backend/app/routers/file.py
- [x] 创建 backend/app/routers/layout.py
- [x] 创建 backend/app/routers/chat.py

#### Step 6: 测试
- [x] 创建 backend/tests/test_solver.py

#### Step 7: 文档
- [x] 创建 backend/README.md

### Frontend 单元

#### Step 8: 项目配置
- [x] 创建 frontend/package.json
- [x] 创建 frontend/vite.config.ts
- [x] 创建 frontend/tsconfig.json

#### Step 9: 类型定义和 API
- [x] 创建 frontend/src/types/index.ts
- [x] 创建 frontend/src/services/api.ts

#### Step 10: Hooks
- [x] 创建 frontend/src/hooks/useChat.ts

#### Step 11: 组件
- [x] 创建 frontend/src/components/ChatPanel.tsx
- [x] 创建 frontend/src/components/FileUpload.tsx
- [x] 创建 frontend/src/components/PlateView.tsx
- [x] 创建 frontend/src/components/DownloadPanel.tsx

#### Step 12: 应用入口
- [x] 创建 frontend/src/App.tsx
- [x] 创建 frontend/src/main.tsx
- [x] 创建 frontend/index.html

#### Step 13: 样式和文档
- [x] 创建 frontend/src/index.css
- [x] 创建 frontend/README.md

---

## 生成顺序

1. Backend Step 1-7（后端完整）
2. Frontend Step 8-13（前端完整）

**预计文件数**: ~30 个文件
