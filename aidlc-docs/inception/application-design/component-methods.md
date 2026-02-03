# Smart Campaign Designer 组件方法设计

## 前端组件接口

### ChatPanel

```typescript
interface ChatPanelProps {
  onSendMessage: (message: string) => void;
  onFileUpload: (file: File) => void;
}

// 方法
sendMessage(content: string): void
  // 发送用户消息到后端，触发 SSE 流

subscribeToStream(sessionId: string): EventSource
  // 订阅 SSE 流式响应

saveHistory(): void
  // 保存对话历史到 localStorage

loadHistory(): Message[]
  // 从 localStorage 加载对话历史

clearHistory(): void
  // 清空对话历史
```

### FileUpload

```typescript
interface FileUploadProps {
  onFileSelected: (file: File) => void;
  onParseComplete: (data: SourcePlate) => void;
  onError: (error: string) => void;
}

// 方法
validateFile(file: File): ValidationResult
  // 验证文件类型和大小

uploadFile(file: File): Promise<SourcePlate>
  // 上传文件并返回解析结果
```

### PlateView

```typescript
interface PlateViewProps {
  layout: PlateLayout;
  onWellClick: (well: LayoutWell) => void;
  onWellDrag: (from: string, to: string) => void;
  editable: boolean;
}

// 方法
renderPlate(layout: PlateLayout): SVGElement
  // 渲染板布局 SVG

handleDragStart(wellId: string): void
  // 开始拖拽

handleDragEnd(wellId: string, targetId: string): void
  // 结束拖拽，触发位置交换

highlightWells(geneSymbol: string): void
  // 高亮指定基因的所有孔位

exportAsSVG(): string
  // 导出 SVG 字符串（用于 PDF）
```

### DownloadPanel

```typescript
interface DownloadPanelProps {
  layout: PlateLayout;
  sourceData: SourcePlate;
  parameters: DesignParameters;
}

// 方法
generatePicklistCSV(): Blob
  // 生成 Echo Picklist CSV 文件

generatePDFReport(): Blob
  // 使用 jsPDF 生成 PDF 报告

downloadFile(blob: Blob, filename: string): void
  // 触发文件下载
```

---

## 后端 API 端点

### AgentService

```python
# POST /api/chat
async def chat(request: ChatRequest) -> StreamingResponse:
    """
    处理用户消息，返回 SSE 流式响应
    
    Input:
      - message: str - 用户消息
      - history: List[Message] - 对话历史
      - source_data: Optional[SourcePlate] - 已上传的源板数据
      - current_layout: Optional[PlateLayout] - 当前布局（如有）
    
    Output:
      - SSE 流，包含 Agent 响应和工具调用结果
    """

# POST /api/chat/extract-parameters
async def extract_parameters(request: ExtractRequest) -> DesignParameters:
    """
    从对话中提取设计参数
    
    Input:
      - message: str - 用户消息
      - history: List[Message] - 对话历史
    
    Output:
      - DesignParameters - 提取的设计参数
    """
```

### FileService

```python
# POST /api/file/parse
async def parse_file(file: UploadFile) -> SourcePlate:
    """
    解析上传的源板文件
    
    Input:
      - file: UploadFile - Excel 或 CSV 文件
    
    Output:
      - SourcePlate - 解析后的源板数据
    
    Errors:
      - 400: 不支持的文件格式
      - 422: 文件解析失败
    """

# POST /api/file/validate
async def validate_file(file: UploadFile) -> ValidationResult:
    """
    验证文件格式和内容
    
    Input:
      - file: UploadFile
    
    Output:
      - ValidationResult - 验证结果（valid, errors, warnings）
    """
```

### LayoutService

```python
# POST /api/layout/generate
async def generate_layout(request: LayoutRequest) -> PlateLayout:
    """
    生成优化的板布局
    
    Input:
      - source_plate: SourcePlate - 源板数据
      - parameters: DesignParameters - 设计参数
    
    Output:
      - PlateLayout - 生成的布局
    
    Errors:
      - 400: 参数无效
      - 422: 无法满足约束
    """

# POST /api/layout/validate
async def validate_layout(layout: PlateLayout) -> ValidationResult:
    """
    验证布局是否满足 PLAID 约束
    
    Input:
      - layout: PlateLayout
    
    Output:
      - ValidationResult - 约束检查结果
    """

# PUT /api/layout/update
async def update_layout(request: UpdateRequest) -> PlateLayout:
    """
    更新布局（用户拖拽调整后）
    
    Input:
      - layout: PlateLayout - 当前布局
      - changes: List[WellChange] - 变更列表
    
    Output:
      - PlateLayout - 更新后的布局
    """

# POST /api/layout/picklist
async def generate_picklist(layout: PlateLayout) -> List[PicklistEntry]:
    """
    生成 Echo Picklist
    
    Input:
      - layout: PlateLayout
    
    Output:
      - List[PicklistEntry] - Picklist 条目列表
    """
```

---

## ConstraintSolver 接口

```python
class ConstraintSolver:
    """OR-Tools 约束求解器封装"""
    
    def __init__(self, parameters: DesignParameters):
        """初始化求解器，设置板尺寸和约束参数"""
    
    def add_samples(self, samples: List[Sample]) -> None:
        """添加样品（基因/化合物）"""
    
    def add_controls(self, controls: List[Control]) -> None:
        """添加对照"""
    
    def solve(self, timeout_seconds: int = 30) -> Optional[PlateLayout]:
        """
        求解约束满足问题
        
        Returns:
          - PlateLayout if solution found
          - None if no solution or timeout
        """
    
    def validate(self, layout: PlateLayout) -> List[ConstraintViolation]:
        """验证布局是否满足所有约束"""
```

### 约束方法（详细业务逻辑在功能设计阶段定义）

```python
# 约束类型（高层接口）
def add_quadrant_balance_constraint() -> None
    """象限平衡约束"""

def add_row_column_balance_constraint() -> None
    """行列平衡约束"""

def add_no_adjacent_same_type_constraint() -> None
    """同类型不相邻约束"""

def add_control_spread_constraint() -> None
    """对照分散约束"""

def add_replicate_spread_constraint() -> None
    """复制品分散约束"""
```
