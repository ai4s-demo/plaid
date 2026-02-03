# Backend 领域实体模型

## 实体关系图

```
┌─────────────────┐       ┌─────────────────┐
│   SourcePlate   │       │ DesignParameters│
│                 │       │                 │
│ - barcode       │       │ - plate_type    │
│ - wells[]       │       │ - replicates    │
└────────┬────────┘       │ - edge_empty    │
         │                │ - distribution  │
         │                │ - controls[]    │
         │                └────────┬────────┘
         │                         │
         ▼                         ▼
┌─────────────────────────────────────────────┐
│              ConstraintSolver               │
│                                             │
│  solve(source, params) -> SolveResult       │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│               SolveResult                   │
│                                             │
│  - status: SUCCESS | PARTIAL | FAILED       │
│  - layout: PlateLayout                      │
│  - violations: List[Violation]              │
│  - relaxed_constraints: List[str]           │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────┐       ┌─────────────────┐
│   PlateLayout   │       │  EchoPicklist   │
│                 │       │                 │
│ - barcode       │ ────→ │ - entries[]     │
│ - plate_type    │       │                 │
│ - wells[]       │       └─────────────────┘
└─────────────────┘
```

---

## 核心实体定义

### 1. SourcePlate（源板）

```python
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SourceWell(BaseModel):
    """源板孔位"""
    position: str           # 孔位置，如 "A01"
    gene_symbol: str        # 基因/化合物名称
    volume: Optional[float] = None  # 可用体积 (µL)
    concentration: Optional[float] = None  # 浓度

class SourcePlate(BaseModel):
    """源板"""
    barcode: str            # 源板条码
    plate_type: str = "384PP_AQ_BP"  # 源板类型
    wells: List[SourceWell] # 孔位列表
    
    def get_genes(self) -> List[str]:
        """获取所有基因名称（去重）"""
        return list(set(w.gene_symbol for w in self.wells))
    
    def find_well(self, gene_symbol: str) -> Optional[SourceWell]:
        """根据基因名称查找孔位"""
        for well in self.wells:
            if well.gene_symbol == gene_symbol:
                return well
        return None
```

### 2. DesignParameters（设计参数）

```python
class PlateType(int, Enum):
    """板类型"""
    PLATE_96 = 96
    PLATE_384 = 384
    PLATE_1536 = 1536

class Distribution(str, Enum):
    """分布方式"""
    RANDOM = "random"
    COLUMN = "column"
    ROW = "row"
    UNIFORM = "uniform"

class ControlType(str, Enum):
    """对照类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    BLANK = "blank"

class Control(BaseModel):
    """对照配置"""
    type: ControlType
    name: str               # 对照名称
    count: int              # 数量
    source_well: Optional[str] = None  # 源孔位（如果来自源板）

class DesignParameters(BaseModel):
    """设计参数"""
    plate_type: PlateType = PlateType.PLATE_96
    replicates: int = 6
    edge_empty_layers: int = 1
    distribution: Distribution = Distribution.UNIFORM
    controls: List[Control] = []
    
    # 默认值
    @classmethod
    def default(cls) -> "DesignParameters":
        return cls(
            plate_type=PlateType.PLATE_96,
            replicates=6,
            edge_empty_layers=1,
            distribution=Distribution.UNIFORM
        )
    
    def get_plate_dimensions(self) -> tuple[int, int]:
        """获取板尺寸 (rows, cols)"""
        dimensions = {
            PlateType.PLATE_96: (8, 12),
            PlateType.PLATE_384: (16, 24),
            PlateType.PLATE_1536: (32, 48),
        }
        return dimensions[self.plate_type]
    
    def get_available_wells(self) -> int:
        """获取可用孔位数（排除边缘）"""
        rows, cols = self.get_plate_dimensions()
        edge = self.edge_empty_layers
        return (rows - 2 * edge) * (cols - 2 * edge)
```

### 3. PlateLayout（板布局）

```python
class ContentType(str, Enum):
    """孔位内容类型"""
    EMPTY = "empty"
    SAMPLE = "sample"
    POSITIVE_CONTROL = "positive_control"
    NEGATIVE_CONTROL = "negative_control"
    BLANK = "blank"

class LayoutWell(BaseModel):
    """布局孔位"""
    position: str           # 孔位置，如 "A01"
    row: int                # 行索引 (0-based)
    col: int                # 列索引 (0-based)
    content_type: ContentType
    gene_symbol: Optional[str] = None  # 基因名称（样品时）
    replicate_index: Optional[int] = None  # 重复索引
    source_plate: Optional[str] = None  # 源板条码
    source_well: Optional[str] = None   # 源孔位置

class PlateLayout(BaseModel):
    """板布局"""
    plate_barcode: str      # 目标板条码
    plate_type: PlateType
    plate_index: int = 0    # 多板时的板索引
    wells: List[LayoutWell]
    
    def get_well(self, position: str) -> Optional[LayoutWell]:
        """根据位置获取孔位"""
        for well in self.wells:
            if well.position == position:
                return well
        return None
    
    def get_wells_by_gene(self, gene_symbol: str) -> List[LayoutWell]:
        """获取指定基因的所有孔位"""
        return [w for w in self.wells if w.gene_symbol == gene_symbol]
    
    def to_matrix(self) -> List[List[Optional[str]]]:
        """转换为二维矩阵（用于可视化）"""
        rows, cols = DesignParameters(plate_type=self.plate_type).get_plate_dimensions()
        matrix = [[None for _ in range(cols)] for _ in range(rows)]
        for well in self.wells:
            matrix[well.row][well.col] = well.gene_symbol or well.content_type.value
        return matrix
```

### 4. SolveResult（求解结果）

```python
class SolveStatus(str, Enum):
    """求解状态"""
    SUCCESS = "success"         # 完全满足所有约束
    PARTIAL = "partial"         # 部分满足，有约束被放宽
    FAILED = "failed"           # 无法求解

class ConstraintViolation(BaseModel):
    """约束违反"""
    constraint_name: str        # 约束名称
    description: str            # 违反描述
    severity: str               # 严重程度: "error" | "warning"
    affected_wells: List[str]   # 受影响的孔位

class SolveResult(BaseModel):
    """求解结果"""
    status: SolveStatus
    layouts: List[PlateLayout] = []  # 可能有多个板
    violations: List[ConstraintViolation] = []
    relaxed_constraints: List[str] = []
    solve_time_ms: int = 0
    message: Optional[str] = None
```

### 5. EchoPicklist（转移清单）

```python
class PicklistEntry(BaseModel):
    """Picklist 条目"""
    source_plate_barcode: str
    source_well: str            # 格式: A01
    source_plate_type: str
    destination_plate_barcode: str
    destination_plate_type: str
    destination_well: str       # 格式: A01
    transfer_volume: float      # 转移体积 (nL)
    gene_symbol: str
    compound_label: Optional[str] = None
    ensembl_id: Optional[str] = None

class EchoPicklist(BaseModel):
    """Echo Picklist"""
    entries: List[PicklistEntry]
    
    def to_csv(self) -> str:
        """导出为 CSV 格式"""
        headers = [
            "Source Plate Barcode", "Source Well", "Source Plate Type",
            "Destination Plate Barcode", "Destination Plate Type", 
            "Destination Well", "Transfer Volume", "GENE_SYMBOL"
        ]
        lines = [",".join(headers)]
        for entry in self.entries:
            line = ",".join([
                entry.source_plate_barcode,
                entry.source_well,
                entry.source_plate_type,
                entry.destination_plate_barcode,
                entry.destination_plate_type,
                entry.destination_well,
                str(entry.transfer_volume),
                entry.gene_symbol
            ])
            lines.append(line)
        return "\n".join(lines)
```

---

## 枚举和常量

```python
# 板尺寸常量
PLATE_DIMENSIONS = {
    96: (8, 12),
    384: (16, 24),
    1536: (32, 48),
}

# 板类型名称映射
PLATE_TYPE_NAMES = {
    96: "Corning_96_Uplate",
    384: "384PP_AQ_BP",
    1536: "1536LDV_AQ_B2",
}

# 约束优先级
CONSTRAINT_PRIORITY = {
    "cardinality": 1,           # 数量精确 - 硬约束
    "no_adjacent": 1,           # 不相邻 - 硬约束
    "control_spread": 2,        # 对照分散 - 软约束
    "quadrant_balance": 3,      # 象限平衡 - 软约束
    "edge_empty": 4,            # 边缘空白 - 软约束
}

# 默认参数
DEFAULT_PARAMS = {
    "plate_type": 96,
    "replicates": 6,
    "edge_empty_layers": 1,
    "distribution": "uniform",
}
```
