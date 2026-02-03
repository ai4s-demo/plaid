# Smart Campaign Designer 服务层设计

## 服务架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      服务编排层                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   AgentOrchestrator                      │   │
│  │  (协调 Agent、文件处理、布局生成的主服务)                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ AgentService  │ │ FileService   │ │ LayoutService │
│               │ │               │ │               │
│ - Bedrock调用 │ │ - Excel解析   │ │ - 约束求解    │
│ - 意图识别    │ │ - CSV解析     │ │ - Picklist生成│
│ - 参数提取    │ │ - 数据验证    │ │ - 布局验证    │
└───────────────┘ └───────────────┘ └───────────────┘
```

---

## 1. AgentOrchestrator（主编排服务）

**职责**: 协调整个对话流程，根据用户意图调用相应服务

### 工作流程

```
用户消息 → 意图识别 → 工具选择 → 执行 → 响应生成
                ↓
        ┌───────┴───────┐
        ↓               ↓
   需要文件?        需要生成布局?
        ↓               ↓
   FileService    LayoutService
```

### 核心方法

```python
class AgentOrchestrator:
    """主编排服务"""
    
    async def process_message(
        self,
        message: str,
        history: List[Message],
        context: SessionContext
    ) -> AsyncGenerator[str, None]:
        """
        处理用户消息，返回流式响应
        
        流程:
        1. 调用 AgentService 理解意图
        2. 根据意图调用相应服务
        3. 流式返回结果
        """
    
    async def handle_file_upload(
        self,
        file: UploadFile,
        context: SessionContext
    ) -> SourcePlate:
        """处理文件上传"""
    
    async def handle_layout_request(
        self,
        parameters: DesignParameters,
        source_data: SourcePlate,
        context: SessionContext
    ) -> PlateLayout:
        """处理布局生成请求"""
```

### 意图类型

| 意图 | 描述 | 触发服务 |
|------|------|----------|
| `UPLOAD_FILE` | 用户要上传文件 | FileService |
| `DESIGN_PLATE` | 用户描述设计需求 | AgentService → LayoutService |
| `MODIFY_LAYOUT` | 用户要修改布局 | LayoutService |
| `GENERATE_PICKLIST` | 用户要生成 Picklist | LayoutService |
| `ASK_QUESTION` | 用户提问 | AgentService |
| `CLARIFY` | Agent 需要澄清 | AgentService |

---

## 2. AgentService（AI Agent 服务）

**职责**: 与 Bedrock Claude 交互，理解用户意图，提取参数

### 核心方法

```python
class AgentService:
    """AI Agent 服务"""
    
    def __init__(self, bedrock_client: BedrockClient):
        self.client = bedrock_client
        self.system_prompt = self._load_system_prompt()
    
    async def chat(
        self,
        message: str,
        history: List[Message],
        context: Dict
    ) -> AsyncGenerator[str, None]:
        """
        与 Claude 对话，流式返回响应
        
        context 包含:
        - source_data: 已上传的源板数据
        - current_layout: 当前布局
        - parameters: 当前设计参数
        """
    
    def extract_parameters(
        self,
        message: str,
        history: List[Message]
    ) -> DesignParameters:
        """从对话中提取设计参数"""
    
    def detect_intent(
        self,
        message: str,
        history: List[Message]
    ) -> Intent:
        """识别用户意图"""
    
    def generate_clarification(
        self,
        missing_params: List[str]
    ) -> str:
        """生成澄清问题"""
```

### System Prompt 设计要点

```
你是 Smart Campaign Designer 的 AI 助手，帮助科学家设计微孔板布局。

你的能力:
1. 理解中英文自然语言描述的实验需求
2. 提取设计参数（基因数、重复数、板类型、分布方式等）
3. 当信息不完整时，主动询问缺失信息
4. 解释 PLAID 约束和设计原理
5. 提供优化建议

当用户描述需求时，提取以下参数:
- plate_type: 板类型 (96/384/1536)
- replicates: 每个基因的重复数
- edge_empty_layers: 边缘空白层数
- distribution: 分布方式 (random/column-based/row-based)
- controls: 对照配置
```

---

## 3. FileService（文件处理服务）

**职责**: 解析上传的源板文件

### 核心方法

```python
class FileService:
    """文件处理服务"""
    
    async def parse(self, file: UploadFile) -> SourcePlate:
        """
        解析文件，返回源板数据
        
        支持格式: Excel (.xlsx, .xls), CSV (.csv)
        处理方式: 内存处理，不落盘
        """
    
    def parse_excel(self, content: bytes) -> SourcePlate:
        """解析 Excel 文件"""
    
    def parse_csv(self, content: bytes) -> SourcePlate:
        """解析 CSV 文件"""
    
    def validate(self, data: SourcePlate) -> ValidationResult:
        """验证数据完整性"""
    
    def detect_columns(self, df: DataFrame) -> ColumnMapping:
        """自动检测列映射"""
```

### 列映射规则

| 标准字段 | 可能的列名 |
|----------|-----------|
| plate_barcode | plate_barcode, Plate Barcode, Source Plate |
| well_alpha | well_alpha, Well, Position, Source Well |
| gene_symbol | gene_symbol, Gene, Gene Symbol, GENE_SYMBOL |
| volume | Volume_Requested, Volume, Transfer Volume |

---

## 4. LayoutService（布局生成服务）

**职责**: 调用约束求解器生成布局，生成 Picklist

### 核心方法

```python
class LayoutService:
    """布局生成服务"""
    
    def __init__(self):
        self.solver = ConstraintSolver()
    
    async def generate(
        self,
        source_data: SourcePlate,
        parameters: DesignParameters
    ) -> PlateLayout:
        """
        生成优化布局
        
        流程:
        1. 配置约束求解器
        2. 添加样品和对照
        3. 求解
        4. 转换为 PlateLayout
        """
    
    def validate(self, layout: PlateLayout) -> ValidationResult:
        """验证布局是否满足约束"""
    
    def update(
        self,
        layout: PlateLayout,
        changes: List[WellChange]
    ) -> PlateLayout:
        """应用用户修改（拖拽）"""
    
    def generate_picklist(
        self,
        layout: PlateLayout,
        source_data: SourcePlate
    ) -> List[PicklistEntry]:
        """生成 Echo Picklist"""
```

---

## 服务交互流程

### 典型对话流程

```
1. 用户: "我有10个基因要研究，随机分布在96孔板，外圈留空，每个6个重复"

2. AgentOrchestrator:
   - 调用 AgentService.detect_intent() → DESIGN_PLATE
   - 调用 AgentService.extract_parameters() → {plate_type: 96, replicates: 6, ...}
   - 检查是否有源板数据 → 无
   - 返回: "请先上传源板文件"

3. 用户: [上传 Excel 文件]

4. AgentOrchestrator:
   - 调用 FileService.parse() → SourcePlate
   - 返回: "已解析源板，包含10个基因..."

5. 用户: "生成布局"

6. AgentOrchestrator:
   - 调用 LayoutService.generate() → PlateLayout
   - 返回: 布局数据 + 可视化

7. 用户: [拖拽调整基因位置]

8. AgentOrchestrator:
   - 调用 LayoutService.update() → 更新后的 PlateLayout
   - 调用 LayoutService.validate() → 检查约束

9. 用户: "生成 Picklist"

10. AgentOrchestrator:
    - 调用 LayoutService.generate_picklist() → CSV 数据
    - 返回: 下载链接
```
