# Smart Campaign Designer 组件定义

## 系统架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        React 前端                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │ ChatPanel│ │FileUpload│ │PlateView │ │DownloadPanel     │   │
│  │          │ │          │ │ (SVG)    │ │ (PDF/CSV)        │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │ SSE / REST API
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI 后端                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ AgentService │ │ FileService  │ │ LayoutService            │ │
│  │              │ │              │ │                          │ │
│  │ ┌──────────┐ │ │ ┌──────────┐ │ │ ┌──────────────────────┐ │ │
│  │ │ Bedrock  │ │ │ │ Parser   │ │ │ │ OR-Tools Solver      │ │ │
│  │ │ Client   │ │ │ │ (Excel/  │ │ │ │ (约束求解)           │ │ │
│  │ └──────────┘ │ │ │  CSV)    │ │ │ └──────────────────────┘ │ │
│  └──────────────┘ │ └──────────┘ │ │                          │ │
│                   └──────────────┘ │ ┌──────────────────────┐ │ │
│                                    │ │ PicklistGenerator    │ │ │
│                                    │ └──────────────────────┘ │ │
│                                    └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 前端组件 (React)

### 1. ChatPanel
**职责**: 对话式交互界面

| 属性 | 说明 |
|------|------|
| 功能 | 显示对话历史、发送用户消息、接收 Agent 流式响应 |
| 状态管理 | 本地存储对话历史 (localStorage) |
| 通信 | SSE 接收流式响应 |

**子组件**:
- `MessageList`: 消息列表展示
- `MessageInput`: 用户输入框
- `StreamingMessage`: 流式响应显示

### 2. FileUpload
**职责**: 源板文件上传

| 属性 | 说明 |
|------|------|
| 功能 | 拖拽/点击上传 Excel/CSV 文件 |
| 验证 | 文件类型、大小限制 |
| 反馈 | 上传进度、解析结果预览 |

### 3. PlateView
**职责**: 微孔板布局可视化（SVG）

| 属性 | 说明 |
|------|------|
| 功能 | 显示板布局、支持拖拽调整基因位置 |
| 交互 | 点击查看孔详情、拖拽移动基因、悬停高亮 |
| 渲染 | SVG 矢量图形，支持缩放 |

**子组件**:
- `Well`: 单个孔位组件（可拖拽）
- `PlateGrid`: 板网格背景
- `Legend`: 图例说明
- `WellTooltip`: 孔位详情提示

### 4. DownloadPanel
**职责**: 输出文件下载

| 属性 | 说明 |
|------|------|
| 功能 | 生成并下载 Echo Picklist CSV、PDF 报告 |
| PDF 生成 | 前端使用 jsPDF 生成 |
| 格式 | CSV, PDF |

### 5. ParameterPanel
**职责**: 设计参数显示与编辑

| 属性 | 说明 |
|------|------|
| 功能 | 显示当前设计参数、允许手动调整 |
| 参数 | 板类型、重复数、边缘空白、分布方式等 |

---

## 后端组件 (FastAPI)

### 1. AgentService
**职责**: AI Agent 编排与对话管理

| 属性 | 说明 |
|------|------|
| 功能 | 接收用户消息、调用 Bedrock、解析意图、编排工具调用 |
| LLM | Amazon Bedrock (Claude) |
| 输出 | SSE 流式响应 |

**核心能力**:
- 自然语言理解（中英文）
- 参数提取（基因数、重复数、板类型等）
- 主动提问（缺失信息时）
- 设计建议（优化方案）

### 2. FileService
**职责**: 文件解析服务

| 属性 | 说明 |
|------|------|
| 功能 | 解析上传的 Excel/CSV 文件，提取源板信息 |
| 处理 | 内存处理，不落盘 |
| 输出 | 结构化的源板数据 |

**支持格式**:
- Excel (.xlsx, .xls)
- CSV (.csv)

### 3. LayoutService
**职责**: 布局生成服务

| 属性 | 说明 |
|------|------|
| 功能 | 调用约束求解器生成优化布局 |
| 求解器 | OR-Tools CP-SAT |
| 约束 | PLAID 约束集（对照分散、不相邻等） |

**子模块**:
- `ConstraintSolver`: OR-Tools 约束求解器封装
- `PicklistGenerator`: Echo Picklist 生成器

### 4. ConstraintSolver (OR-Tools)
**职责**: 约束满足问题求解

| 属性 | 说明 |
|------|------|
| 功能 | 实现 PLAID 约束模型，生成满足约束的布局 |
| 算法 | 约束编程 (CP-SAT) |
| 约束 | 象限平衡、行列平衡、不相邻、分散等 |

---

## 数据模型

### SourcePlate (源板)
```python
class SourcePlate:
    barcode: str           # 源板条码
    wells: List[SourceWell] # 孔位列表

class SourceWell:
    position: str          # 孔位置 (如 A01)
    gene_symbol: str       # 基因名称
    volume: float          # 可用体积
    concentration: float   # 浓度
```

### DesignParameters (设计参数)
```python
class DesignParameters:
    plate_type: int        # 96, 384, 1536
    replicates: int        # 重复数
    edge_empty_layers: int # 边缘空白层数
    distribution: str      # random, column-based, row-based
    controls: List[Control] # 对照配置
```

### PlateLayout (板布局)
```python
class PlateLayout:
    plate_barcode: str     # 目标板条码
    plate_type: int        # 板类型
    wells: List[LayoutWell] # 布局孔位

class LayoutWell:
    position: str          # 孔位置
    content_type: str      # gene, positive_control, negative_control, empty
    gene_symbol: str       # 基因名称（如适用）
    source_plate: str      # 源板条码
    source_well: str       # 源孔位置
```

### EchoPicklist (转移清单)
```python
class PicklistEntry:
    source_plate_barcode: str
    source_well: str
    source_plate_type: str
    destination_plate_barcode: str
    destination_plate_type: str
    destination_well: str
    transfer_volume: float
    gene_symbol: str
```
