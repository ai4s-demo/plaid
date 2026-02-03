# Backend 业务规则

## 1. PLAID 约束规则

### 1.1 约束优先级

| 优先级 | 约束名称 | 类型 | 说明 |
|--------|----------|------|------|
| 1 | 数量精确 | 硬约束 | 每个基因的重复数必须精确正确 |
| 1 | 同类型不相邻 | 硬约束 | 同类型对照不能在8方向相邻 |
| 2 | 对照分散 | 软约束 | 对照之间至少间隔1个孔 |
| 3 | 象限平衡 | 软约束 | 四个象限的样品数量差异≤1 |
| 4 | 边缘空白 | 软约束 | 外圈指定层数留空 |

### 1.2 约束详细规则

#### R1: 数量精确约束 (Cardinality)
```
规则: 每种元素在布局中的数量必须等于预期数量
公式: count(element_id) == expected_count[element_id]
示例: 如果基因A需要6个重复，则布局中基因A必须恰好出现6次
违反处理: 不可放宽，必须满足
```

#### R2: 同类型不相邻约束 (No Adjacent)
```
规则: 同类型对照不能在8个方向上相邻
方向: 上、下、左、右、左上、右上、左下、右下
公式: ∀ (r,c), (r',c') ∈ 8邻域: plates[r][c] == ctrl_id → plates[r'][c'] ≠ ctrl_id
示例: 如果 A01 是阳性对照，则 A02, B01, B02 都不能是阳性对照
违反处理: 不可放宽，必须满足
```

#### R3: 对照分散约束 (Control Spread)
```
规则: 同一行/列中，对照之间至少间隔1个孔
公式: ∀ 对照位置 i, j 在同一行: |col(i) - col(j)| > 1
示例: 如果 A01 是对照，则 A02 不能是对照，但 A03 可以
违反处理: 可放宽，返回警告
```

#### R4: 象限平衡约束 (Quadrant Balance)
```
规则: 四个象限的样品数量差异不超过1
象限定义:
  - 上左: row < rows/2, col < cols/2
  - 上右: row < rows/2, col >= cols/2
  - 下左: row >= rows/2, col < cols/2
  - 下右: row >= rows/2, col >= cols/2
公式: max(Q1,Q2,Q3,Q4) - min(Q1,Q2,Q3,Q4) <= 1
违反处理: 可放宽，返回警告
```

#### R5: 边缘空白约束 (Edge Empty)
```
规则: 外圈指定层数的孔位必须为空
公式: ∀ r < edge 或 r >= rows-edge 或 c < edge 或 c >= cols-edge: plates[r][c] == 0
示例: edge=1 时，第一行、最后一行、第一列、最后一列都为空
违反处理: 可放宽，返回警告
```

---

## 2. 输入验证规则

### 2.1 文件验证

| 规则ID | 规则 | 错误消息 |
|--------|------|----------|
| V-F01 | 文件类型必须是 .xlsx, .xls, .csv | "不支持的文件格式，请上传 Excel 或 CSV 文件" |
| V-F02 | 文件大小不超过 10MB | "文件过大，请上传小于 10MB 的文件" |
| V-F03 | 文件必须包含必填列 | "缺少必填列: {missing_columns}" |
| V-F04 | 孔位格式必须正确 (A01-P24) | "无效的孔位格式: {invalid_wells}" |

### 2.2 参数验证

| 规则ID | 规则 | 错误消息 |
|--------|------|----------|
| V-P01 | plate_type ∈ {96, 384, 1536} | "无效的板类型，支持 96, 384, 1536" |
| V-P02 | replicates >= 1 | "重复数必须至少为 1" |
| V-P03 | edge_empty_layers >= 0 | "边缘空白层数不能为负" |
| V-P04 | edge_empty_layers < rows/2 | "边缘空白层数过大，没有可用孔位" |
| V-P05 | 总样品数 <= 可用孔位数 | "样品数量超过板容量，需要 {required} 个孔位，但只有 {available} 个可用" |

### 2.3 布局验证

| 规则ID | 规则 | 错误消息 |
|--------|------|----------|
| V-L01 | 孔位不能重复 | "孔位 {position} 被重复分配" |
| V-L02 | 孔位必须在板范围内 | "孔位 {position} 超出板范围" |
| V-L03 | 所有样品必须有源孔位 | "样品 {gene} 在源板中找不到" |

---

## 3. 错误处理规则

### 3.1 错误分类

| 类型 | 说明 | 处理方式 |
|------|------|----------|
| ValidationError | 输入验证失败 | 返回 400，显示具体错误 |
| SolveError | 约束求解失败 | 返回部分解 + 违反列表 |
| FileParseError | 文件解析失败 | 返回 422，显示解析错误 |
| ServiceError | 外部服务错误 | 返回 503，建议重试 |

### 3.2 错误响应格式

```python
class ErrorResponse(BaseModel):
    error_code: str         # 错误代码
    message: str            # 用户友好的错误消息
    details: Optional[dict] # 详细信息
    suggestions: List[str]  # 建议的解决方案

# 示例
{
    "error_code": "CONSTRAINT_UNSATISFIABLE",
    "message": "无法满足所有约束条件",
    "details": {
        "violated_constraints": ["quadrant_balance", "control_spread"],
        "partial_solution_available": true
    },
    "suggestions": [
        "减少重复数",
        "使用更大的板类型",
        "减少边缘空白层数"
    ]
}
```

### 3.3 约束违反处理

```python
def handle_constraint_violation(violations: List[ConstraintViolation]) -> SolveResult:
    """
    处理约束违反
    
    1. 分类违反（硬约束 vs 软约束）
    2. 如果只有软约束违反，返回部分解
    3. 如果有硬约束违反，返回失败
    4. 生成用户友好的违反描述
    """
    
    hard_violations = [v for v in violations if v.severity == "error"]
    soft_violations = [v for v in violations if v.severity == "warning"]
    
    if hard_violations:
        return SolveResult(
            status=SolveStatus.FAILED,
            violations=violations,
            message="无法满足硬约束: " + ", ".join(v.constraint_name for v in hard_violations)
        )
    
    return SolveResult(
        status=SolveStatus.PARTIAL,
        layouts=partial_layouts,
        violations=soft_violations,
        relaxed_constraints=[v.constraint_name for v in soft_violations],
        message="已生成布局，但以下约束被放宽: " + ", ".join(v.constraint_name for v in soft_violations)
    )
```

---

## 4. 业务流程规则

### 4.1 对话流程规则

```
R-C01: 必须先上传源板文件才能生成布局
R-C02: 参数不完整时，Agent 必须主动询问
R-C03: 生成布局前必须确认所有参数
R-C04: 用户修改布局后必须重新验证约束
```

### 4.2 多板处理规则

```
R-M01: 当样品数超过单板容量时，自动分配到多个板
R-M02: 每个样品的所有重复尽量在同一板
R-M03: 对照在每个板上均匀分布
R-M04: 板编号从 1 开始，格式为 plate_1, plate_2, ...
```

### 4.3 Picklist 生成规则

```
R-P01: 孔位格式必须是 A01 格式（字母+两位数字）
R-P02: 转移体积单位为 nL（纳升）
R-P03: 每个目标孔位只能有一个源孔位
R-P04: 空孔位不生成 Picklist 条目
```

---

## 5. 约束解释文本

用于 Agent 向用户解释约束原理：

```python
CONSTRAINT_EXPLANATIONS = {
    "cardinality": """
        **数量精确约束**
        确保每个基因/化合物的重复数量精确正确。
        这是最基本的约束，保证实验设计的准确性。
    """,
    
    "no_adjacent": """
        **同类型不相邻约束**
        同类型的对照样品不能放在相邻的孔位（包括对角线方向）。
        这样可以避免局部区域的系统误差影响所有对照，提高数据质量。
    """,
    
    "control_spread": """
        **对照分散约束**
        对照样品应该均匀分散在整个板上，而不是集中在某个区域。
        这有助于检测和校正板效应（如边缘效应、温度梯度等）。
    """,
    
    "quadrant_balance": """
        **象限平衡约束**
        样品在板的四个象限中均匀分布。
        这可以减少系统性偏差对实验结果的影响。
    """,
    
    "edge_empty": """
        **边缘空白约束**
        板的外圈孔位留空，不放置样品。
        边缘孔位容易受到蒸发、温度变化等因素影响，留空可以提高数据质量。
    """
}
```
