# Smart Campaign Designer - Backend

基于 PLAID 方法论的微孔板布局设计 API 服务。

## 技术栈

- **框架**: FastAPI
- **约束求解**: OR-Tools CP-SAT
- **AI**: Amazon Bedrock (Claude)
- **数据处理**: Pandas, OpenPyXL

## 快速开始

### 1. 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
DEBUG=false
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

服务将在 http://localhost:8000 启动。

## API 端点

### 文件解析

```
POST /api/file/parse
Content-Type: multipart/form-data

上传 Excel 或 CSV 文件，返回解析后的源板数据。
```

### 布局生成

```
POST /api/layout/generate
Content-Type: application/json

{
  "source_plate": { ... },
  "parameters": {
    "plate_type": 96,
    "replicates": 6,
    "edge_empty_layers": 1,
    "distribution": "uniform"
  }
}
```

### AI 对话

```
POST /api/chat/
Content-Type: application/json

{
  "message": "我有10个基因，随机分布在96孔板",
  "history": []
}

返回 SSE 流式响应。
```

### Picklist 生成

```
POST /api/layout/picklist/csv
Content-Type: application/json

返回 Echo Picklist CSV 文件。
```

## 项目结构

```
backend/
├── app/
│   ├── main.py           # FastAPI 入口
│   ├── config.py         # 配置
│   ├── routers/          # API 路由
│   ├── services/         # 业务服务
│   ├── solver/           # 约束求解器
│   └── models/           # 数据模型
├── tests/                # 测试
└── requirements.txt
```

## 测试

```bash
pytest tests/ -v
```

## PLAID 约束

系统实现以下 PLAID 约束：

1. **数量精确** (硬约束): 每个基因的重复数必须正确
2. **同类型不相邻** (硬约束): 同类型对照不能在8方向相邻
3. **对照分散** (软约束): 对照之间有间隔
4. **象限平衡** (软约束): 四个象限样品数量均衡
5. **边缘空白** (软约束): 外圈留空
