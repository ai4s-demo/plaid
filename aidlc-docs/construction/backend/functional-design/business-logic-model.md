# Backend 业务逻辑模型

## 1. 约束求解器核心算法

### 1.1 算法概述

```
输入: SourcePlate + DesignParameters
  ↓
预处理: 计算所需孔位数、板数
  ↓
建模: 创建 OR-Tools CP-SAT 模型
  ↓
添加约束: 按优先级添加硬约束和软约束
  ↓
求解: 执行求解器（超时30秒）
  ↓
后处理: 转换为 PlateLayout
  ↓
输出: PlateLayout 或 PartialSolution + Violations
```

### 1.2 求解流程

```python
def solve_layout(source_plate: SourcePlate, params: DesignParameters) -> SolveResult:
    """
    主求解流程
    
    1. 预处理
       - 计算总样品数 = len(genes) * replicates + controls
       - 计算可用孔位 = (rows - 2*edge) * (cols - 2*edge)
       - 计算所需板数 = ceil(总样品数 / 可用孔位)
    
    2. 创建模型
       - 决策变量: plates[p][r][c] ∈ {0, 1, ..., max_id}
       - 0 = 空孔, 1..n = 样品, n+1..m = 对照
    
    3. 添加硬约束（优先级1，不可放宽）
       - 数量精确约束
       - 同类型不相邻约束
    
    4. 添加软约束（可放宽）
       - 对照分散约束（优先级2）
       - 象限平衡约束（优先级3）
       - 边缘空白约束（优先级4）
    
    5. 求解
       - 设置超时 30 秒
       - 如果有解，返回完整布局
       - 如果无解，逐步放宽软约束重试
    
    6. 返回结果
       - 成功: PlateLayout
       - 部分成功: PartialSolution + 违反的约束列表
       - 失败: 错误信息
    """
```

### 1.3 约束实现

#### 硬约束（不可放宽）

```python
# 1. 数量精确约束
def add_cardinality_constraint(model, plates, expected_counts):
    """确保每种元素的数量精确正确"""
    for element_id, count in expected_counts.items():
        model.Add(sum(plates[p][r][c] == element_id 
                      for p, r, c in all_positions) == count)

# 2. 同类型不相邻约束（8方向）
def add_no_adjacent_constraint(model, plates, control_ids):
    """同类型对照不能在8个方向上相邻"""
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for ctrl_id in control_ids:
        for p, r, c in inner_positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # 如果当前位置是 ctrl_id，则相邻位置不能是 ctrl_id
                model.AddImplication(
                    plates[p][r][c] == ctrl_id,
                    plates[p][nr][nc] != ctrl_id
                )
```

#### 软约束（可放宽）

```python
# 3. 对照分散约束（优先级2）
def add_control_spread_constraint(model, plates, control_ids, min_gap=1):
    """对照之间至少间隔 min_gap 个孔"""
    # 使用软约束，允许违反但有惩罚
    violations = []
    for row in each_row:
        for i, j in adjacent_pairs:
            if both_are_controls:
                v = model.NewBoolVar(f'spread_violation_{i}_{j}')
                violations.append(v)
    return violations

# 4. 象限平衡约束（优先级3）
def add_quadrant_balance_constraint(model, plates, max_diff=1):
    """四个象限的样品数量差异不超过 max_diff"""
    for plate in plates:
        q1 = count_in_quadrant(plate, 'upper_left')
        q2 = count_in_quadrant(plate, 'upper_right')
        q3 = count_in_quadrant(plate, 'lower_left')
        q4 = count_in_quadrant(plate, 'lower_right')
        # 软约束：最大差异
        model.Add(max(q1,q2,q3,q4) - min(q1,q2,q3,q4) <= max_diff)

# 5. 边缘空白约束（优先级4）
def add_edge_empty_constraint(model, plates, edge_layers=1):
    """外圈 edge_layers 层留空"""
    for p in range(num_plates):
        for r in range(edge_layers):
            for c in range(cols):
                model.Add(plates[p][r][c] == 0)  # 顶部
                model.Add(plates[p][rows-1-r][c] == 0)  # 底部
        for c in range(edge_layers):
            for r in range(rows):
                model.Add(plates[p][r][c] == 0)  # 左侧
                model.Add(plates[p][r][cols-1-c] == 0)  # 右侧
```

### 1.4 无解处理策略

```python
def solve_with_relaxation(model, constraints_by_priority):
    """
    渐进式放宽约束求解
    
    1. 尝试满足所有约束
    2. 如果无解，按优先级从低到高放宽：
       - 先放宽优先级4（边缘空白）
       - 再放宽优先级3（象限平衡）
       - 再放宽优先级2（对照分散）
    3. 硬约束（优先级1）永不放宽
    4. 返回解 + 被放宽的约束列表
    """
    
    result = solver.Solve(model)
    if result == OPTIMAL or result == FEASIBLE:
        return Solution(layout, relaxed_constraints=[])
    
    # 逐步放宽
    for priority in [4, 3, 2]:
        relax_constraints(model, priority)
        result = solver.Solve(model)
        if result == OPTIMAL or result == FEASIBLE:
            return PartialSolution(
                layout=extract_layout(solver),
                relaxed_constraints=get_relaxed(priority),
                violations=check_violations(layout)
            )
    
    return NoSolution(reason="无法满足硬约束")
```

---

## 2. Agent 对话流程

### 2.1 意图识别

```python
INTENTS = {
    'UPLOAD_FILE': ['上传', 'upload', '文件', 'file', 'excel', 'csv'],
    'DESIGN_PLATE': ['设计', 'design', '布局', 'layout', '基因', 'gene', '重复', 'replicate'],
    'MODIFY_LAYOUT': ['修改', 'modify', '调整', 'adjust', '移动', 'move'],
    'GENERATE_PICKLIST': ['生成', 'generate', 'picklist', '清单'],
    'EXPLAIN': ['解释', 'explain', '为什么', 'why', '约束', 'constraint'],
    'VALIDATE': ['验证', 'validate', '检查', 'check'],
}

def detect_intent(message: str, history: List[Message]) -> Intent:
    """
    基于关键词和上下文识别意图
    
    1. 关键词匹配
    2. 上下文推断（如果刚上传文件，下一步可能是设计）
    3. LLM 辅助（复杂情况）
    """
```

### 2.2 参数提取

```python
def extract_parameters(message: str) -> DesignParameters:
    """
    从自然语言中提取设计参数
    
    示例输入: "10个基因，随机分布在96孔板，外圈留空，每个6个重复"
    
    提取:
    - genes: 10 (从 "10个基因")
    - plate_type: 96 (从 "96孔板")
    - edge_empty: 1 (从 "外圈留空")
    - replicates: 6 (从 "每个6个重复")
    - distribution: random (从 "随机分布")
    """
    
    # 使用 LLM 提取结构化参数
    prompt = f"""
    从以下描述中提取实验设计参数:
    "{message}"
    
    返回 JSON 格式:
    {{
        "plate_type": 96 或 384 或 1536,
        "replicates": 数字,
        "edge_empty_layers": 数字,
        "distribution": "random" 或 "column" 或 "row" 或 "uniform"
    }}
    
    如果某参数未提及，返回 null
    """
```

### 2.3 Agent 工具定义

```python
AGENT_TOOLS = [
    {
        "name": "parse_source_file",
        "description": "解析上传的源板文件（Excel/CSV），提取基因和孔位信息",
        "parameters": {"file_content": "bytes"}
    },
    {
        "name": "generate_layout",
        "description": "根据设计参数生成优化的板布局",
        "parameters": {"source_plate": "SourcePlate", "params": "DesignParameters"}
    },
    {
        "name": "validate_layout",
        "description": "验证布局是否满足 PLAID 约束",
        "parameters": {"layout": "PlateLayout"}
    },
    {
        "name": "generate_picklist",
        "description": "生成 Echo Picklist 文件",
        "parameters": {"layout": "PlateLayout", "source": "SourcePlate"}
    },
    {
        "name": "explain_constraint",
        "description": "解释特定约束的原理和作用",
        "parameters": {"constraint_name": "str"}
    },
    {
        "name": "suggest_optimization",
        "description": "根据当前设计提供优化建议",
        "parameters": {"layout": "PlateLayout", "params": "DesignParameters"}
    }
]
```

---

## 3. 文件解析逻辑

### 3.1 Excel 解析

```python
def parse_excel(content: bytes) -> SourcePlate:
    """
    解析 Excel 文件
    
    1. 读取所有工作表
    2. 自动检测包含源板信息的工作表
    3. 自动映射列名
    4. 验证必填字段
    5. 返回结构化数据
    """
    
    # 列名映射
    COLUMN_MAPPING = {
        'plate_barcode': ['plate_barcode', 'Plate Barcode', 'Source Plate', 'barcode'],
        'well_alpha': ['well_alpha', 'Well', 'Position', 'Source Well', 'well'],
        'gene_symbol': ['gene_symbol', 'Gene', 'Gene Symbol', 'GENE_SYMBOL', 'gene'],
        'volume': ['Volume_Requested', 'Volume', 'Transfer Volume', 'volume'],
    }
```

### 3.2 CSV 解析

```python
def parse_csv(content: bytes) -> SourcePlate:
    """
    解析 CSV 文件
    
    1. 自动检测分隔符（逗号、制表符、分号）
    2. 自动检测编码（UTF-8、GBK）
    3. 映射列名
    4. 验证数据
    """
```

---

## 4. Picklist 生成逻辑

### 4.1 生成算法

```python
def generate_picklist(layout: PlateLayout, source: SourcePlate) -> List[PicklistEntry]:
    """
    生成 Echo Picklist
    
    对于布局中的每个非空孔位:
    1. 查找对应的源板孔位
    2. 计算转移体积
    3. 生成 Picklist 条目
    """
    
    entries = []
    for well in layout.wells:
        if well.content_type == 'empty':
            continue
        
        source_well = find_source_well(source, well.gene_symbol)
        
        entry = PicklistEntry(
            source_plate_barcode=source_well.plate_barcode,
            source_well=source_well.position,
            source_plate_type="384PP_AQ_BP",  # 默认源板类型
            destination_plate_barcode=layout.plate_barcode,
            destination_plate_type=get_plate_type_name(layout.plate_type),
            destination_well=well.position,  # 格式: A01, B02
            transfer_volume=calculate_volume(well, source_well),
            gene_symbol=well.gene_symbol
        )
        entries.append(entry)
    
    return entries
```

### 4.2 孔位格式转换

```python
def format_well_position(row: int, col: int) -> str:
    """
    转换为 A01 格式
    
    row=0, col=0 -> A01
    row=1, col=5 -> B06
    """
    letter = chr(ord('A') + row)
    number = f"{col + 1:02d}"
    return f"{letter}{number}"
```

---

## 5. 多板处理逻辑

### 5.1 自动分配算法

```python
def allocate_to_plates(samples: List[Sample], params: DesignParameters) -> List[PlateLayout]:
    """
    自动分配样品到多个板
    
    1. 计算单板可用孔位
    2. 计算所需板数
    3. 均匀分配样品到各板
    4. 确保每个样品的所有重复在同一板（可选）
    """
    
    rows, cols = get_plate_dimensions(params.plate_type)
    edge = params.edge_empty_layers
    available_wells = (rows - 2*edge) * (cols - 2*edge)
    
    total_samples = len(samples) * params.replicates + count_controls(params)
    num_plates = math.ceil(total_samples / available_wells)
    
    # 分配策略：均匀分配
    plates = []
    for i in range(num_plates):
        plate_samples = samples[i::num_plates]  # 交错分配
        plates.append(create_plate(plate_samples, params, plate_index=i))
    
    return plates
```
