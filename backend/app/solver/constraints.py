"""PLAID constraint definitions."""

# Constraint priority levels
# 1 = Hard constraint (cannot be relaxed)
# 2-4 = Soft constraints (can be relaxed in order)
CONSTRAINT_PRIORITY = {
    "cardinality": 1,        # Exact count - hard
    "no_adjacent": 1,        # No adjacent same type - hard
    "control_spread": 2,     # Control spacing - soft
    "quadrant_balance": 3,   # Quadrant balance - soft
    "edge_empty": 4,         # Edge empty - soft
}

# Constraint explanations for Agent
CONSTRAINT_EXPLANATIONS = {
    "cardinality": """
**数量精确约束 (Cardinality)**
确保每个基因/化合物的重复数量精确正确。
这是最基本的约束，保证实验设计的准确性。
""",
    
    "no_adjacent": """
**同类型不相邻约束 (No Adjacent)**
同类型的对照样品不能放在相邻的孔位（包括对角线方向）。
这样可以避免局部区域的系统误差影响所有对照，提高数据质量。
""",
    
    "control_spread": """
**对照分散约束 (Control Spread)**
对照样品应该均匀分散在整个板上，而不是集中在某个区域。
这有助于检测和校正板效应（如边缘效应、温度梯度等）。
""",
    
    "quadrant_balance": """
**象限平衡约束 (Quadrant Balance)**
样品在板的四个象限中均匀分布。
这可以减少系统性偏差对实验结果的影响。
""",
    
    "edge_empty": """
**边缘空白约束 (Edge Empty)**
板的外圈孔位留空，不放置样品。
边缘孔位容易受到蒸发、温度变化等因素影响，留空可以提高数据质量。
"""
}


def get_constraint_explanation(constraint_name: str) -> str:
    """Get explanation for a constraint."""
    return CONSTRAINT_EXPLANATIONS.get(
        constraint_name, 
        f"未知约束: {constraint_name}"
    )


def is_hard_constraint(constraint_name: str) -> bool:
    """Check if constraint is hard (cannot be relaxed)."""
    return CONSTRAINT_PRIORITY.get(constraint_name, 1) == 1
