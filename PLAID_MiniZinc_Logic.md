# PLAID MiniZinc 模型逻辑详解

## 1. 概述

PLAID (Plate Layouts using Artificial Intelligence Design) 使用约束编程 (Constraint Programming) 来生成高质量的微孔板布局。核心思想是将布局设计问题建模为约束满足问题 (CSP)，由求解器自动找到满足所有约束的解。

## 2. Smart Campaign Designer 输入参数

### 2.1 文件输入：Source List（源板列表）

用户上传 Excel 文件（如 `REQ_source list_barcode.xlsx`），包含以下字段：

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| plate_barcode | string | 源板条码 | SRCPALT1 |
| well_alpha | string | 源孔位置 | A01, B02 |
| gene_symbol | string | 基因名称 | Gene1, PLK1 |
| nnc_substance | string | 物质编号 | nncd1 |
| sequence | string | 序列信息 | Sequence1 |
| Volume_Requested | float | 请求体积 (µL) | 45 |
| Quantity_Requested | float | 请求量 (nmol) | 0.45 |

**从文件自动提取**：
- 基因/化合物列表
- 源板信息
- 可用体积/浓度

### 2.2 用户交互输入：实验设计参数

用户通过自然语言或表单指定：

```
示例: "I have a new experiment to investigate 10 genes. I want these 10 genes 
distributing randomly in a 96-well plate and leave the one outer layer empty. 
Each gene has 6 replicates."
```

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| plate_type | enum | 目标板类型 | 96 |
| replicates | int | 每个基因/化合物的重复数 | 3 |
| edge_empty_layers | int | 边缘空白层数 | 1 |
| distribution | enum | 分布方式 (random/column-based/row-based) | random |
| transfer_volume | float | 转移体积 (nmol 或 µL) | 1 |

### 2.3 对照配置（用户指定）

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| positive_control | string | 阳性对照名称 | PLK1, KIF11 |
| positive_count | int | 阳性对照数量 | 6 |
| negative_control | string | 阴性对照名称 | scramble, NC |
| negative_count | int | 阴性对照数量 | 6 |
| blank_count | int | 空白对照数量 | 0 |

### 2.4 多层设计（高级选项）

支持多层实验设计，每层可有不同分布策略：

```json
{
  "layers": [
    {"name": "gene", "distribution": "random", "needs_picklist": true},
    {"name": "treatment", "distribution": "column-based", "needs_picklist": false}
  ]
}
```

### 2.5 约束开关

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| allow_empty_wells | bool | 是否允许空孔 | true |
| concentrations_on_different_rows | bool | 浓度在不同行 | true |
| concentrations_on_different_columns | bool | 浓度在不同列 | true |
| spread_controls | bool | 分散对照 | true |
| no_adjacent_same_type | bool | 同类型不相邻 | true |

### 2.6 完整输入参数结构

```python
input_params = {
    # === 文件输入 ===
    "source_file": "REQ_source list_barcode.xlsx",  # 上传文件
    
    # === 从文件自动提取 ===
    "genes": ["Gene1", "Gene2", ...],  # 自动解析
    "source_plates": {
        "SRCPALT1": {"Gene1": "A01", "Gene2": "A02", ...}
    },
    
    # === 用户指定：板配置 ===
    "plate_type": "96",           # 96, 384, 1536
    "edge_empty_layers": 1,       # 边缘空白层数
    
    # === 用户指定：实验设计 ===
    "replicates": 6,              # 每个基因重复数
    "distribution": "random",     # random, column-based, row-based
    "transfer_volume": 1,         # nmol
    
    # === 用户指定：对照 ===
    "controls": [
        {"name": "positive", "count": 6, "source": "user_specified"},
        {"name": "negative", "count": 6, "source": "user_specified"}
    ],
    
    # === 用户指定：多层设计（可选）===
    "layers": [
        {"name": "gene", "distribution": "random"},
        {"name": "treatment", "distribution": "column-based"}
    ],
    
    # === 约束配置 ===
    "constraints": {
        "spread_controls": True,
        "different_rows": True,
        "different_cols": True,
        "no_adjacent": True
    }
}
```

## 3. 输出格式：Echo Picklist

输出 CSV 文件（如 `ExpID_EchoPicklist.csv`）：

| 字段 | 说明 |
|------|------|
| Source Plate Barcode | 源板条码 |
| Source Well | 源孔位置 |
| Destination Plate Type | 目标板类型 |
| Destination Plate Barcode | 目标板条码 |
| Destination Well | 目标孔位置 |
| Transfer Volume | 转移体积 |
| Gene Symbol | 基因名称 |
| Compound Label | 化合物标签 |

---

## 4. MiniZinc 原始参数（参考）

以下是 MiniZinc 模型的原始参数定义，供实现参考：

### 4.1 板尺寸参数
```
num_rows: 板的行数 (如 96孔板=8, 384孔板=16)
num_cols: 板的列数 (如 96孔板=12, 384孔板=24)
size_empty_edge: 边缘空白行/列数 (通常=1，减少边缘效应)
horizontal_cell_lines: 水平细胞系数量 (通常=1)
vertical_cell_lines: 垂直细胞系数量 (通常=1)
```

### 4.2 化合物参数
```
compounds: 化合物数量
compound_concentrations[1..compounds]: 每个化合物的浓度数
compound_replicates[1..compounds]: 每个化合物的重复数
compound_names[1..compounds]: 化合物名称
```

### 4.3 对照参数
```
num_controls: 对照类型数量
control_replicates[1..num_controls]: 每种对照的重复数
control_concentrations[1..num_controls]: 每种对照的浓度数
control_names[1..num_controls]: 对照名称
```

## 5. 决策变量

### 3.1 主布局矩阵
```
plates[Plates, Rows, Columns]: 3D数组
  - 值 = 0: 空孔
  - 值 = 1..experiments: 化合物/实验
  - 值 > experiments: 对照
```

### 3.2 辅助变量（用于约束传播）
```
experiment_plate[1..experiments]: 每个实验在哪个板
experiment_row[1..experiments]: 每个实验在哪行
experiment_column[1..experiments]: 每个实验在哪列
```

### 3.3 统计变量
```
experiments_in_plate_row[Plates, Rows]: 每板每行的实验数
experiments_in_plate_column[Plates, Columns]: 每板每列的实验数
controls_in_plate_row[Plates, Rows]: 每板每行的对照数
ul_half_plates[Plates, {upper,lower}]: 上下半板的实验数
lr_half_plates[Plates, {left,right}]: 左右半板的实验数
```

## 6. 核心约束

### 4.1 数量精确约束 (Global Cardinality)
确保每种元素的数量精确正确。

```minizinc
% 每种化合物/对照的数量必须精确
constraint global_cardinality(plates, 
    [i | i in 0..max_id],
    [expected_count[i] | i in 0..max_id]);
```

**Python 等价实现**:
```python
from collections import Counter
counts = Counter(layout.flatten())
for element_id, expected in expected_counts.items():
    assert counts[element_id] == expected
```

### 4.2 浓度分散约束 (All Different)
同一化合物的不同浓度必须在不同行/列。

```minizinc
% 浓度在不同行
constraint if concentrations_on_different_rows then
    forall(compound in 1..compounds, rep in 0..replicates-1)(
        alldifferent([experiment_row[concentration_index] | 
                      concentration_index in compound_concentrations])
    )
endif;
```

**Python 等价实现**:
```python
def check_concentrations_different_rows(compound_positions):
    rows = [pos[0] for pos in compound_positions]
    return len(rows) == len(set(rows))  # 所有行都不同
```

### 4.3 对照分散约束 (Regular Constraint)
同类型对照之间必须有间隔。

```minizinc
% 对照间隔至少1个孔 (使用正则表达式约束)
constraint if spread_controls then
    forall(plate in Plates, row in Rows)(
        regular(controls_layout[plate, row, ..], "(0|(1 0))* (1?)")
    )
endif;

% 对照间隔至少2个孔
constraint if force_spread_controls then
    forall(plate in Plates, row in Rows)(
        regular(controls_layout[plate, row, ..], "(0|(1 0 0))* (1|(1 0))?")
    )
endif;
```

**Python 等价实现**:
```python
def check_control_spacing(row_layout, min_spacing=1):
    """检查一行中对照的间隔"""
    control_positions = [i for i, v in enumerate(row_layout) if v > 0]
    for i in range(len(control_positions) - 1):
        if control_positions[i+1] - control_positions[i] <= min_spacing:
            return False
    return True
```

### 4.4 8方向相邻约束
同类型对照不能在8个方向上相邻。

```minizinc
% 同类型对照不相邻
constraint forall(ctrl in 1..num_controls)(
    forall(plate in Plates, j in 2..rows-1, k in 2..cols-1)(
        plates[plate,j,k] == ctrl_id -> (
            plates[plate,j-1,k-1] != ctrl_id /\
            plates[plate,j-1,k]   != ctrl_id /\
            plates[plate,j-1,k+1] != ctrl_id /\
            plates[plate,j,k-1]   != ctrl_id /\
            plates[plate,j,k+1]   != ctrl_id /\
            plates[plate,j+1,k-1] != ctrl_id /\
            plates[plate,j+1,k]   != ctrl_id /\
            plates[plate,j+1,k+1] != ctrl_id
        )
    )
);
```

**Python 等价实现**:
```python
def check_no_adjacent_same_type(layout, row, col, value):
    """检查8方向是否有相同值"""
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < layout.shape[0] and 0 <= nc < layout.shape[1]:
            if layout[nr, nc] == value:
                return False
    return True
```

### 4.5 象限平衡约束
对照和化合物在四个象限均匀分布。

```minizinc
% 上下半板实验数差异 <= 1
constraint forall(plate in Plates)(
    abs(ul_half_plates[plate, upper] - ul_half_plates[plate, lower]) <= 1
);

% 左右半板实验数差异 <= 1
constraint forall(plate in Plates)(
    abs(lr_half_plates[plate, left] - lr_half_plates[plate, right]) <= 1
);

% 对照在上下半板均衡
constraint forall(plate in Plates)(
    abs(sum(controls_ul_plates[plate, upper, ..]) - 
        sum(controls_ul_plates[plate, lower, ..])) <= 1
);
```

**Python 等价实现**:
```python
def check_quadrant_balance(positions, rows, cols, max_diff=1):
    """检查四个象限的平衡性"""
    mid_r, mid_c = rows // 2, cols // 2
    quadrants = [0, 0, 0, 0]  # [上左, 上右, 下左, 下右]
    
    for r, c in positions:
        q = (0 if r < mid_r else 2) + (0 if c < mid_c else 1)
        quadrants[q] += 1
    
    return max(quadrants) - min(quadrants) <= max_diff
```

### 4.6 板间平衡约束
化合物和对照在多个板之间均匀分布。

```minizinc
% 每种对照在每板的数量差异 <= 1
constraint forall(plate in Plates)(
    global_cardinality_low_up(
        plates[plate, .., ..],
        [ctrl_id | ctrl in 1..num_controls],
        [floor(ctrl_count/numplates) | ctrl in 1..num_controls],
        [ceil(ctrl_count/numplates) | ctrl in 1..num_controls]
    )
);
```

**Python 等价实现**:
```python
def distribute_evenly(total_count, num_plates):
    """计算每板的最小/最大数量"""
    base = total_count // num_plates
    remainder = total_count % num_plates
    return base, base + (1 if remainder > 0 else 0)
```

### 4.7 复制品约束
控制复制品是在同一板还是不同板。

```minizinc
% 复制品在不同板
constraint if replicates_on_different_plates then
    forall(compound in 1..compounds)(
        nvalue(min(numplates, replicates), 
               [experiment_plate[rep_index] | rep in 1..replicates])
    )
endif;

% 复制品在同一板
constraint if replicates_on_same_plate then
    forall(compound in 1..compounds)(
        all_equal([experiment_plate[rep_index] | rep in 1..replicates])
    )
endif;
```

### 4.8 行列平衡约束
每行/列的对照数量均衡。

```minizinc
% 每行对照数量在范围内
constraint forall(plate in Plates, row in Rows)(
    controls_in_plate_row[plate, row] >= floor(total_controls/numplates/num_rows)
);
constraint forall(plate in Plates, row in Rows)(
    controls_in_plate_row[plate, row] <= ceil(total_controls/numplates/num_rows)
);
```

## 7. 搜索策略

```minizinc
solve :: seq_search([
    % 1. 先决定每个实验在哪个板
    int_search(experiment_plate, first_fail, indomain_random),
    % 2. 再决定每个实验在哪行
    int_search(experiment_row, first_fail, indomain_random),
    % 3. 最后填充具体位置
    int_search(plates, random, indomain_max)
]) satisfy;
```

**搜索策略解释**:
- `first_fail`: 优先选择域最小的变量（最受约束的）
- `indomain_random`: 随机选择值（增加解的多样性）
- `seq_search`: 按顺序执行多个搜索

## 8. 约束优先级

1. **硬约束** (必须满足):
   - 数量精确
   - 浓度在不同行/列
   - 同类型对照不相邻

2. **软约束** (尽量满足):
   - 象限平衡
   - 行列平衡
   - 对照间隔最大化

## 9. 复杂度分析

| 板类型 | 变量数 | 约束数 | 典型求解时间 |
|--------|--------|--------|--------------|
| 96孔   | ~1000  | ~5000  | 1-10秒       |
| 384孔  | ~5000  | ~30000 | 10秒-5分钟   |
| 1536孔 | ~20000 | ~150000| 分钟-小时级  |

## 10. Python 实现方案

### 方案 A: 使用 OR-Tools CP-SAT 求解器
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
# 定义变量和约束...
solver = cp_model.CpSolver()
status = solver.Solve(model)
```

### 方案 B: 使用 python-constraint 库
```python
from constraint import Problem, AllDifferentConstraint

problem = Problem()
# 定义变量和约束...
solutions = problem.getSolutions()
```

### 方案 C: 使用 MiniZinc Python 接口
```python
import minizinc

model = minizinc.Model("plate-design.mzn")
solver = minizinc.Solver.lookup("gecode")
instance = minizinc.Instance(solver, model)
result = instance.solve()
```

## 11. 关键算法伪代码

```
算法: PLAID 布局生成

输入: 化合物列表, 对照列表, 板尺寸, 约束配置
输出: 满足所有约束的布局

1. 初始化:
   - 计算所需板数 = ceil(总孔数 / 内部孔数)
   - 创建决策变量 plates[板][行][列]
   
2. 添加约束:
   2.1 数量约束: global_cardinality(plates, 元素ID, 期望数量)
   2.2 浓度约束: alldifferent(同化合物不同浓度的行/列)
   2.3 对照约束: regular(对照布局, 间隔模式)
   2.4 相邻约束: 8方向检查
   2.5 平衡约束: 象限/行列/板间平衡
   
3. 搜索:
   3.1 选择最受约束的变量 (first_fail)
   3.2 随机选择值 (indomain_random)
   3.3 传播约束
   3.4 如果冲突则回溯
   
4. 输出:
   - 如果找到解: 返回布局
   - 如果无解: 报告不可满足
```

## 12. 参考资料

- [PLAID 论文](https://doi.org/10.1016/j.ailsci.2023.100073)
- [MiniZinc 文档](https://www.minizinc.org/doc-2.5.5/en/index.html)
- [Gecode 约束求解器](https://www.gecode.org/)
- [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver)
