"""PLAID constraint solver using OR-Tools CP-SAT."""
import math
import time
import logging
from typing import List, Optional, Tuple, Dict
from ortools.sat.python import cp_model

from app.models import (
    SourcePlate, DesignParameters, PlateLayout, LayoutWell,
    ContentType, SolveResult, SolveStatus, ConstraintViolation,
    PlateType, PLATE_DIMENSIONS
)
from app.solver.constraints import CONSTRAINT_PRIORITY, is_hard_constraint

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ConstraintSolver:
    """PLAID constraint solver using OR-Tools CP-SAT."""
    
    def __init__(self, params: DesignParameters):
        self.params = params
        self.rows, self.cols = params.get_plate_dimensions()
        self.edge = params.edge_empty_layers
        
        # Calculate inner dimensions (excluding edge)
        self.inner_rows = self.rows - 2 * self.edge
        self.inner_cols = self.cols - 2 * self.edge
        self.available_wells = self.inner_rows * self.inner_cols
        
    def solve(
        self, 
        genes: List[str],
        source_plate: SourcePlate,
        timeout_seconds: int = 30
    ) -> SolveResult:
        """Solve the plate layout problem using CP-SAT."""
        start_time = time.time()
        
        # Calculate requirements - 支持每个基因不同的重复数
        total_samples = sum(self.params.get_replicates_for_gene(gene) for gene in genes)
        total_controls = sum(c.count for c in self.params.controls)
        total_needed = total_samples + total_controls
        
        # Check if we need multiple plates
        num_plates = math.ceil(total_needed / self.available_wells)
        
        if num_plates > 10:
            return SolveResult(
                status=SolveStatus.FAILED,
                message=f"需要 {num_plates} 个板，超过最大限制 (10)"
            )
        
        try:
            layouts = self._solve_with_cpsat(
                genes, source_plate, num_plates, timeout_seconds
            )
            
            solve_time = int((time.time() - start_time) * 1000)
            
            if layouts:
                violations = self._validate_layouts(layouts)
                
                if any(v.severity == "error" for v in violations):
                    return SolveResult(
                        status=SolveStatus.PARTIAL,
                        layouts=layouts,
                        violations=violations,
                        solve_time_ms=solve_time,
                        message="布局生成完成，但存在约束违反"
                    )
                
                return SolveResult(
                    status=SolveStatus.SUCCESS,
                    layouts=layouts,
                    violations=violations,
                    solve_time_ms=solve_time,
                    message="布局生成成功"
                )
            else:
                return SolveResult(
                    status=SolveStatus.FAILED,
                    solve_time_ms=solve_time,
                    message="无法找到满足约束的布局"
                )
                
        except Exception as e:
            return SolveResult(
                status=SolveStatus.FAILED,
                message=f"求解器错误: {str(e)}"
            )
    
    def _solve_with_cpsat(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        num_plates: int,
        timeout_seconds: int
    ) -> Optional[List[PlateLayout]]:
        """Solve using OR-Tools CP-SAT solver."""
        
        # For single plate, use full CP-SAT model
        if num_plates == 1:
            return [self._solve_single_plate_cpsat(genes, source_plate, 0, timeout_seconds)]
        
        # For multiple plates, distribute genes and solve each
        layouts = []
        genes_per_plate = math.ceil(len(genes) / num_plates)
        
        for plate_idx in range(num_plates):
            start = plate_idx * genes_per_plate
            end = min(start + genes_per_plate, len(genes))
            plate_genes = genes[start:end]
            
            if plate_genes:
                layout = self._solve_single_plate_cpsat(
                    plate_genes, source_plate, plate_idx, timeout_seconds // num_plates
                )
                layouts.append(layout)
        
        return layouts
    
    def _solve_single_plate_cpsat(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        plate_idx: int,
        timeout_seconds: int
    ) -> PlateLayout:
        """Solve single plate layout using CP-SAT with full constraints."""
        
        logger.info(f"=== CP-SAT 求解开始 ===")
        logger.info(f"板类型: {self.params.plate_type}, 行数: {self.rows}, 列数: {self.cols}")
        logger.info(f"边缘层数: {self.edge}")
        logger.info(f"基因数: {len(genes)}, 默认重复数: {self.params.replicates}")
        
        model = cp_model.CpModel()
        
        # Get inner positions (excluding edge)
        inner_rows = self.rows - 2 * self.edge
        inner_cols = self.cols - 2 * self.edge
        inner_positions = [
            (r, c) 
            for r in range(self.edge, self.rows - self.edge)
            for c in range(self.edge, self.cols - self.edge)
        ]
        num_positions = len(inner_positions)
        
        logger.info(f"内部可用位置数: {num_positions} ({inner_rows}行 x {inner_cols}列)")
        
        # Create sample list - 支持每个基因不同的重复数
        samples = []
        for g_idx, gene in enumerate(genes):
            gene_reps = self.params.get_replicates_for_gene(gene)
            for rep in range(gene_reps):
                samples.append((g_idx, rep, gene))
        
        num_samples = len(samples)
        num_genes = len(genes)
        
        logger.info(f"总样本数: {num_samples}")
        
        if num_samples > num_positions:
            logger.error(f"样本数 {num_samples} > 可用位置 {num_positions}")
            return self._solve_heuristic_improved(genes, source_plate, plate_idx)
        
        # ========== 决策变量 ==========
        # 方法：为每个样本分配一个行变量和列变量
        # sample_row[s] = 样本s的行位置
        # sample_col[s] = 样本s的列位置
        
        sample_row = {}
        sample_col = {}
        
        for s in range(num_samples):
            sample_row[s] = model.NewIntVar(self.edge, self.rows - self.edge - 1, f'row_{s}')
            sample_col[s] = model.NewIntVar(self.edge, self.cols - self.edge - 1, f'col_{s}')
        
        logger.info(f"创建位置变量: {num_samples * 2}")
        
        # ========== 约束1: 每个位置最多一个样本 ==========
        # 使用 AllDifferent 约束：将 (row, col) 编码为单个整数
        position_vars = []
        for s in range(num_samples):
            pos_var = model.NewIntVar(0, self.rows * self.cols - 1, f'pos_{s}')
            model.Add(pos_var == sample_row[s] * self.cols + sample_col[s])
            position_vars.append(pos_var)
        
        model.AddAllDifferent(position_vars)
        logger.info("添加位置唯一约束: AllDifferent")
        
        # ========== 约束2: 同基因不相邻 (8-connected) ==========
        adjacent_constraints = 0
        
        for g_idx in range(num_genes):
            # 获取该基因的所有样本索引
            gene_samples = [s for s in range(num_samples) if samples[s][0] == g_idx]
            
            # 对于同基因的每对样本
            for i, s1 in enumerate(gene_samples):
                for s2 in gene_samples[i+1:]:
                    # 行差的绝对值
                    row_diff = model.NewIntVar(-self.rows, self.rows, f'rd_{s1}_{s2}')
                    model.Add(row_diff == sample_row[s1] - sample_row[s2])
                    abs_row_diff = model.NewIntVar(0, self.rows, f'ard_{s1}_{s2}')
                    model.AddAbsEquality(abs_row_diff, row_diff)
                    
                    # 列差的绝对值
                    col_diff = model.NewIntVar(-self.cols, self.cols, f'cd_{s1}_{s2}')
                    model.Add(col_diff == sample_col[s1] - sample_col[s2])
                    abs_col_diff = model.NewIntVar(0, self.cols, f'acd_{s1}_{s2}')
                    model.AddAbsEquality(abs_col_diff, col_diff)
                    
                    # 不相邻: 不能同时 abs_row_diff <= 1 AND abs_col_diff <= 1
                    # 等价于: abs_row_diff >= 2 OR abs_col_diff >= 2
                    not_adjacent = model.NewBoolVar(f'na_{s1}_{s2}')
                    
                    # 如果 abs_row_diff >= 2，则 not_adjacent 可以为 true
                    row_far = model.NewBoolVar(f'rf_{s1}_{s2}')
                    model.Add(abs_row_diff >= 2).OnlyEnforceIf(row_far)
                    model.Add(abs_row_diff <= 1).OnlyEnforceIf(row_far.Not())
                    
                    # 如果 abs_col_diff >= 2，则 not_adjacent 可以为 true
                    col_far = model.NewBoolVar(f'cf_{s1}_{s2}')
                    model.Add(abs_col_diff >= 2).OnlyEnforceIf(col_far)
                    model.Add(abs_col_diff <= 1).OnlyEnforceIf(col_far.Not())
                    
                    # 至少一个为 true
                    model.AddBoolOr([row_far, col_far])
                    
                    adjacent_constraints += 1
        
        logger.info(f"添加相邻约束数: {adjacent_constraints}")
        
        # ========== 约束3: 分散约束 - 同基因的重复分布在不同行/列 ==========
        # 对于每个基因，其重复应该尽量分散
        
        spread_constraints = 0
        for g_idx in range(num_genes):
            gene_samples = [s for s in range(num_samples) if samples[s][0] == g_idx]
            gene_reps = len(gene_samples)
            
            if gene_reps <= 1:
                continue
            
            # 软约束：同基因的样本尽量不在同一行
            # 使用 AllDifferent 作为软约束（通过目标函数）
            gene_rows = [sample_row[s] for s in gene_samples]
            gene_cols = [sample_col[s] for s in gene_samples]
            
            # 如果该基因的重复数 <= 可用行数，可以强制不同行
            if gene_reps <= inner_rows:
                model.AddAllDifferent(gene_rows)
                spread_constraints += 1
            
            # 如果该基因的重复数 <= 可用列数，可以强制不同列
            if gene_reps <= inner_cols:
                model.AddAllDifferent(gene_cols)
                spread_constraints += 1
        
        logger.info(f"添加分散约束数: {spread_constraints}")
        
        # ========== 目标函数: 均匀分布 ==========
        # 不再最大化距离（会导致聚集在角落）
        # 改为：让样本均匀填充整个区域
        
        # 方法：将板子分成网格区域，每个区域应该有相似数量的样本
        # 使用软约束鼓励均匀分布
        
        # 计算理想的行/列分布
        # 每行应该有 num_samples / inner_rows 个样本
        # 每列应该有 num_samples / inner_cols 个样本
        
        ideal_per_row = num_samples / inner_rows
        ideal_per_col = num_samples / inner_cols
        
        logger.info(f"理想分布: 每行 {ideal_per_row:.1f} 个, 每列 {ideal_per_col:.1f} 个")
        
        # 为每行创建计数变量
        row_counts = {}
        for r in range(self.edge, self.rows - self.edge):
            row_counts[r] = model.NewIntVar(0, num_samples, f'row_count_{r}')
            # 计算该行有多少样本
            row_indicators = []
            for s in range(num_samples):
                is_in_row = model.NewBoolVar(f'in_row_{s}_{r}')
                model.Add(sample_row[s] == r).OnlyEnforceIf(is_in_row)
                model.Add(sample_row[s] != r).OnlyEnforceIf(is_in_row.Not())
                row_indicators.append(is_in_row)
            model.Add(row_counts[r] == sum(row_indicators))
        
        # 为每列创建计数变量
        col_counts = {}
        for c in range(self.edge, self.cols - self.edge):
            col_counts[c] = model.NewIntVar(0, num_samples, f'col_count_{c}')
            col_indicators = []
            for s in range(num_samples):
                is_in_col = model.NewBoolVar(f'in_col_{s}_{c}')
                model.Add(sample_col[s] == c).OnlyEnforceIf(is_in_col)
                model.Add(sample_col[s] != c).OnlyEnforceIf(is_in_col.Not())
                col_indicators.append(is_in_col)
            model.Add(col_counts[c] == sum(col_indicators))
        
        # 目标：最小化行/列计数与理想值的偏差
        # 使用平方偏差的近似
        deviation_vars = []
        
        ideal_row = int(round(ideal_per_row))
        ideal_col = int(round(ideal_per_col))
        
        for r in range(self.edge, self.rows - self.edge):
            # |row_counts[r] - ideal_row|
            diff = model.NewIntVar(-num_samples, num_samples, f'row_diff_{r}')
            model.Add(diff == row_counts[r] - ideal_row)
            abs_diff = model.NewIntVar(0, num_samples, f'row_abs_{r}')
            model.AddAbsEquality(abs_diff, diff)
            deviation_vars.append(abs_diff)
        
        for c in range(self.edge, self.cols - self.edge):
            diff = model.NewIntVar(-num_samples, num_samples, f'col_diff_{c}')
            model.Add(diff == col_counts[c] - ideal_col)
            abs_diff = model.NewIntVar(0, num_samples, f'col_abs_{c}')
            model.AddAbsEquality(abs_diff, diff)
            deviation_vars.append(abs_diff)
        
        # 最小化总偏差
        logger.info(f"目标函数: 最小化 {len(deviation_vars)} 个行/列偏差")
        model.Minimize(sum(deviation_vars))
        
        # ========== 求解 ==========
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = timeout_seconds
        solver.parameters.num_search_workers = 8
        solver.parameters.log_search_progress = True
        
        logger.info(f"开始求解，超时时间: {timeout_seconds}秒")
        start_time = time.time()
        status = solver.Solve(model)
        solve_time = time.time() - start_time
        
        status_names = {
            cp_model.OPTIMAL: "OPTIMAL",
            cp_model.FEASIBLE: "FEASIBLE", 
            cp_model.INFEASIBLE: "INFEASIBLE",
            cp_model.MODEL_INVALID: "MODEL_INVALID",
            cp_model.UNKNOWN: "UNKNOWN"
        }
        logger.info(f"求解完成，状态: {status_names.get(status, status)}, 耗时: {solve_time:.2f}秒")
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            logger.info(f"目标值 (总偏差): {solver.ObjectiveValue()}")
            
            # 提取解
            return self._extract_solution_from_vars(
                solver, sample_row, sample_col, samples,
                source_plate, plate_idx, genes
            )
        else:
            logger.error(f"CP-SAT 求解失败，状态: {status}")
            # 放宽约束重试
            return self._solve_relaxed(genes, source_plate, plate_idx, timeout_seconds)
    
    def _extract_solution_from_vars(
        self,
        solver: cp_model.CpSolver,
        sample_row: Dict,
        sample_col: Dict,
        samples: List[Tuple[int, int, str]],
        source_plate: SourcePlate,
        plate_idx: int,
        genes: List[str]
    ) -> PlateLayout:
        """Extract solution from row/col variables."""
        
        wells = []
        placement = {}
        
        # Add edge wells
        for r in range(self.rows):
            for c in range(self.cols):
                if (r < self.edge or r >= self.rows - self.edge or
                    c < self.edge or c >= self.cols - self.edge):
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r,
                        col=c,
                        content_type=ContentType.EMPTY
                    ))
        
        # Extract sample placements
        for s, (g_idx, rep, gene) in enumerate(samples):
            r = solver.Value(sample_row[s])
            c = solver.Value(sample_col[s])
            placement[(r, c)] = (gene, rep)
            
            source_well = source_plate.find_well(gene)
            wells.append(LayoutWell(
                position=self._format_position(r, c),
                row=r,
                col=c,
                content_type=ContentType.SAMPLE,
                gene_symbol=gene,
                replicate_index=rep,
                source_plate=source_plate.barcode,
                source_well=source_well.position if source_well else None
            ))
        
        # 统计分布
        row_counts = {}
        for (r, c) in placement:
            row_counts[r] = row_counts.get(r, 0) + 1
        logger.info(f"每行样本数: {dict(sorted(row_counts.items()))}")
        
        # Fill remaining with empty
        for r in range(self.edge, self.rows - self.edge):
            for c in range(self.edge, self.cols - self.edge):
                if (r, c) not in placement:
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r,
                        col=c,
                        content_type=ContentType.EMPTY
                    ))
        
        return PlateLayout(
            plate_barcode=f"plate_{plate_idx + 1}",
            plate_type=self.params.plate_type,
            plate_index=plate_idx,
            wells=wells
        )
    
    def _solve_relaxed(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        plate_idx: int,
        timeout_seconds: int
    ) -> PlateLayout:
        """Solve with relaxed constraints (remove AllDifferent for rows/cols)."""
        
        logger.info("=== 放宽约束重试 ===")
        
        model = cp_model.CpModel()
        
        inner_rows = self.rows - 2 * self.edge
        inner_cols = self.cols - 2 * self.edge
        
        samples = []
        for g_idx, gene in enumerate(genes):
            gene_reps = self.params.get_replicates_for_gene(gene)
            for rep in range(gene_reps):
                samples.append((g_idx, rep, gene))
        
        num_samples = len(samples)
        num_genes = len(genes)
        
        # 决策变量
        sample_row = {}
        sample_col = {}
        
        for s in range(num_samples):
            sample_row[s] = model.NewIntVar(self.edge, self.rows - self.edge - 1, f'row_{s}')
            sample_col[s] = model.NewIntVar(self.edge, self.cols - self.edge - 1, f'col_{s}')
        
        # 位置唯一约束
        position_vars = []
        for s in range(num_samples):
            pos_var = model.NewIntVar(0, self.rows * self.cols - 1, f'pos_{s}')
            model.Add(pos_var == sample_row[s] * self.cols + sample_col[s])
            position_vars.append(pos_var)
        
        model.AddAllDifferent(position_vars)
        
        # 只保留不相邻约束（硬约束）
        for g_idx in range(num_genes):
            gene_samples = [s for s in range(num_samples) if samples[s][0] == g_idx]
            
            for i, s1 in enumerate(gene_samples):
                for s2 in gene_samples[i+1:]:
                    row_diff = model.NewIntVar(-self.rows, self.rows, f'rd_{s1}_{s2}')
                    model.Add(row_diff == sample_row[s1] - sample_row[s2])
                    abs_row_diff = model.NewIntVar(0, self.rows, f'ard_{s1}_{s2}')
                    model.AddAbsEquality(abs_row_diff, row_diff)
                    
                    col_diff = model.NewIntVar(-self.cols, self.cols, f'cd_{s1}_{s2}')
                    model.Add(col_diff == sample_col[s1] - sample_col[s2])
                    abs_col_diff = model.NewIntVar(0, self.cols, f'acd_{s1}_{s2}')
                    model.AddAbsEquality(abs_col_diff, col_diff)
                    
                    row_far = model.NewBoolVar(f'rf_{s1}_{s2}')
                    model.Add(abs_row_diff >= 2).OnlyEnforceIf(row_far)
                    model.Add(abs_row_diff <= 1).OnlyEnforceIf(row_far.Not())
                    
                    col_far = model.NewBoolVar(f'cf_{s1}_{s2}')
                    model.Add(abs_col_diff >= 2).OnlyEnforceIf(col_far)
                    model.Add(abs_col_diff <= 1).OnlyEnforceIf(col_far.Not())
                    
                    model.AddBoolOr([row_far, col_far])
        
        # 目标函数: 均匀分布
        ideal_per_row = num_samples / inner_rows
        ideal_per_col = num_samples / inner_cols
        ideal_row = int(round(ideal_per_row))
        ideal_col = int(round(ideal_per_col))
        
        # 行计数
        row_counts = {}
        for r in range(self.edge, self.rows - self.edge):
            row_counts[r] = model.NewIntVar(0, num_samples, f'row_count_{r}')
            row_indicators = []
            for s in range(num_samples):
                is_in_row = model.NewBoolVar(f'in_row_{s}_{r}')
                model.Add(sample_row[s] == r).OnlyEnforceIf(is_in_row)
                model.Add(sample_row[s] != r).OnlyEnforceIf(is_in_row.Not())
                row_indicators.append(is_in_row)
            model.Add(row_counts[r] == sum(row_indicators))
        
        # 列计数
        col_counts = {}
        for c in range(self.edge, self.cols - self.edge):
            col_counts[c] = model.NewIntVar(0, num_samples, f'col_count_{c}')
            col_indicators = []
            for s in range(num_samples):
                is_in_col = model.NewBoolVar(f'in_col_{s}_{c}')
                model.Add(sample_col[s] == c).OnlyEnforceIf(is_in_col)
                model.Add(sample_col[s] != c).OnlyEnforceIf(is_in_col.Not())
                col_indicators.append(is_in_col)
            model.Add(col_counts[c] == sum(col_indicators))
        
        # 偏差
        deviation_vars = []
        for r in range(self.edge, self.rows - self.edge):
            diff = model.NewIntVar(-num_samples, num_samples, f'row_diff_{r}')
            model.Add(diff == row_counts[r] - ideal_row)
            abs_diff = model.NewIntVar(0, num_samples, f'row_abs_{r}')
            model.AddAbsEquality(abs_diff, diff)
            deviation_vars.append(abs_diff)
        
        for c in range(self.edge, self.cols - self.edge):
            diff = model.NewIntVar(-num_samples, num_samples, f'col_diff_{c}')
            model.Add(diff == col_counts[c] - ideal_col)
            abs_diff = model.NewIntVar(0, num_samples, f'col_abs_{c}')
            model.AddAbsEquality(abs_diff, diff)
            deviation_vars.append(abs_diff)
        
        model.Minimize(sum(deviation_vars))
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = timeout_seconds
        solver.parameters.num_search_workers = 8
        
        status = solver.Solve(model)
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            logger.info(f"放宽约束求解成功")
            return self._extract_solution_from_vars(
                solver, sample_row, sample_col, samples,
                source_plate, plate_idx, genes
            )
        else:
            logger.error("放宽约束仍然失败，使用启发式")
            return self._solve_heuristic_improved(genes, source_plate, plate_idx)
    
    def _extract_solution(
        self,
        solver: cp_model.CpSolver,
        x: Dict,
        samples: List[Tuple[int, int, str]],
        positions: List[Tuple[int, int]],
        source_plate: SourcePlate,
        plate_idx: int,
        genes: List[str]
    ) -> PlateLayout:
        """Extract solution from CP-SAT solver."""
        
        wells = []
        
        # Add edge wells
        for r in range(self.rows):
            for c in range(self.cols):
                if (r < self.edge or r >= self.rows - self.edge or
                    c < self.edge or c >= self.cols - self.edge):
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r,
                        col=c,
                        content_type=ContentType.EMPTY
                    ))
        
        # Extract sample placements
        placed_positions = set()
        for s, (g_idx, rep, gene) in enumerate(samples):
            for p, (r, c) in enumerate(positions):
                if solver.Value(x[s, p]) == 1:
                    source_well = source_plate.find_well(gene)
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r,
                        col=c,
                        content_type=ContentType.SAMPLE,
                        gene_symbol=gene,
                        replicate_index=rep,
                        source_plate=source_plate.barcode,
                        source_well=source_well.position if source_well else None
                    ))
                    placed_positions.add((r, c))
                    break
        
        # Fill remaining with empty
        for r, c in positions:
            if (r, c) not in placed_positions:
                wells.append(LayoutWell(
                    position=self._format_position(r, c),
                    row=r,
                    col=c,
                    content_type=ContentType.EMPTY
                ))
        
        return PlateLayout(
            plate_barcode=f"plate_{plate_idx + 1}",
            plate_type=self.params.plate_type,
            plate_index=plate_idx,
            wells=wells
        )
    
    def _solve_heuristic(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        plate_idx: int
    ) -> PlateLayout:
        """Fallback heuristic solver."""
        logger.info("使用基础启发式算法")
        return self._solve_heuristic_improved(genes, source_plate, plate_idx)
    
    def _solve_heuristic_improved(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        plate_idx: int
    ) -> PlateLayout:
        """Improved heuristic solver with better distribution."""
        
        logger.info("=== 改进启发式算法开始 ===")
        
        wells = []
        
        # Add edge wells
        for r in range(self.rows):
            for c in range(self.cols):
                if (r < self.edge or r >= self.rows - self.edge or
                    c < self.edge or c >= self.cols - self.edge):
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r,
                        col=c,
                        content_type=ContentType.EMPTY
                    ))
        
        # 获取内部位置
        inner_rows = self.rows - 2 * self.edge
        inner_cols = self.cols - 2 * self.edge
        
        logger.info(f"内部区域: {inner_rows} 行 x {inner_cols} 列")
        
        # 创建样本列表 - 支持每个基因不同的重复数
        samples = []
        for g_idx, gene in enumerate(genes):
            gene_reps = self.params.get_replicates_for_gene(gene)
            for rep in range(gene_reps):
                samples.append((gene, rep, g_idx))
        
        logger.info(f"总样本数: {len(samples)}")
        
        # 使用拉丁方阵思想分配位置
        # 将板子分成多个区块，每个基因的重复分散到不同区块
        num_genes = len(genes)
        
        # 计算区块大小
        # 目标：每个基因的重复尽量分散到不同的行和列
        placement = {}
        
        # 按照交错模式放置
        # 对于每个基因的每个重复，计算其目标位置
        for g_idx, gene in enumerate(genes):
            gene_reps = self.params.get_replicates_for_gene(gene)
            for rep in range(gene_reps):
                # 使用黄金比例来分散位置
                golden_ratio = 1.618033988749895
                
                # 计算目标行和列（使用不同的偏移确保分散）
                row_offset = int((g_idx * golden_ratio + rep * golden_ratio * golden_ratio) * inner_rows) % inner_rows
                col_offset = int((g_idx * golden_ratio * golden_ratio + rep * golden_ratio) * inner_cols) % inner_cols
                
                target_r = self.edge + row_offset
                target_c = self.edge + col_offset
                
                # 在目标位置附近找一个空位，同时避免相邻同基因
                placed = False
                
                # 螺旋搜索
                for radius in range(max(inner_rows, inner_cols)):
                    if placed:
                        break
                    for dr in range(-radius, radius + 1):
                        if placed:
                            break
                        for dc in range(-radius, radius + 1):
                            if abs(dr) != radius and abs(dc) != radius:
                                continue  # 只检查边界
                            
                            r = target_r + dr
                            c = target_c + dc
                            
                            # 检查边界
                            if r < self.edge or r >= self.rows - self.edge:
                                continue
                            if c < self.edge or c >= self.cols - self.edge:
                                continue
                            
                            # 检查是否已占用
                            if (r, c) in placement:
                                continue
                            
                            # 检查相邻是否有同基因
                            if not self._has_adjacent_same_gene(r, c, gene, placement):
                                placement[(r, c)] = (gene, rep)
                                placed = True
                                break
                
                # 如果还没放置，强制放置
                if not placed:
                    for r in range(self.edge, self.rows - self.edge):
                        if placed:
                            break
                        for c in range(self.edge, self.cols - self.edge):
                            if (r, c) not in placement:
                                placement[(r, c)] = (gene, rep)
                                placed = True
                                break
        
        logger.info(f"放置样本数: {len(placement)}")
        
        # 统计每行的样本数
        row_counts = {}
        for (r, c), (gene, rep) in placement.items():
            row_counts[r] = row_counts.get(r, 0) + 1
        logger.info(f"每行样本数: {dict(sorted(row_counts.items()))}")
        
        # Create wells from placement
        for (r, c), (gene, rep) in placement.items():
            source_well = source_plate.find_well(gene)
            wells.append(LayoutWell(
                position=self._format_position(r, c),
                row=r,
                col=c,
                content_type=ContentType.SAMPLE,
                gene_symbol=gene,
                replicate_index=rep,
                source_plate=source_plate.barcode,
                source_well=source_well.position if source_well else None
            ))
        
        # Fill remaining with empty
        for r in range(self.edge, self.rows - self.edge):
            for c in range(self.edge, self.cols - self.edge):
                if (r, c) not in placement:
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r,
                        col=c,
                        content_type=ContentType.EMPTY
                    ))
        
        logger.info("=== 改进启发式算法完成 ===")
        
        return PlateLayout(
            plate_barcode=f"plate_{plate_idx + 1}",
            plate_type=self.params.plate_type,
            plate_index=plate_idx,
            wells=wells
        )
    
    def _get_spread_positions(self) -> List[Tuple[int, int]]:
        """Get positions in spread pattern (checkerboard)."""
        positions = []
        for offset in [0, 1]:
            for r in range(self.edge, self.rows - self.edge):
                for c in range(self.edge, self.cols - self.edge):
                    if (r + c) % 2 == offset:
                        positions.append((r, c))
        return positions
    
    def _has_adjacent_same_gene(self, r: int, c: int, gene: str, placement: Dict) -> bool:
        """Check if position has adjacent same gene."""
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            if (r + dr, c + dc) in placement:
                if placement[(r + dr, c + dc)][0] == gene:
                    return True
        return False
    
    def _format_position(self, row: int, col: int) -> str:
        return f"{chr(ord('A') + row)}{col + 1:02d}"
    
    def _validate_layouts(self, layouts: List[PlateLayout]) -> List[ConstraintViolation]:
        violations = []
        for layout in layouts:
            violations.extend(self._check_no_adjacent(layout))
            violations.extend(self._check_quadrant_balance(layout))
        return violations
    
    def _check_no_adjacent(self, layout: PlateLayout) -> List[ConstraintViolation]:
        violations = []
        pos_map = {(w.row, w.col): w for w in layout.wells}
        checked = set()
        
        for well in layout.wells:
            if well.content_type == ContentType.SAMPLE and well.gene_symbol:
                for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                    neighbor = pos_map.get((well.row + dr, well.col + dc))
                    if (neighbor and neighbor.content_type == ContentType.SAMPLE and
                        neighbor.gene_symbol == well.gene_symbol):
                        pair = tuple(sorted([well.position, neighbor.position]))
                        if pair not in checked:
                            checked.add(pair)
                            violations.append(ConstraintViolation(
                                constraint_name="no_adjacent_same_gene",
                                description=f"同一基因 {well.gene_symbol} 相邻: {pair[0]}, {pair[1]}",
                                severity="warning",
                                affected_wells=list(pair)
                            ))
        return violations
    
    def _check_quadrant_balance(self, layout: PlateLayout) -> List[ConstraintViolation]:
        mid_r, mid_c = self.rows // 2, self.cols // 2
        quadrants = [0, 0, 0, 0]
        
        for well in layout.wells:
            if well.content_type == ContentType.SAMPLE:
                q = (0 if well.row < mid_r else 2) + (0 if well.col < mid_c else 1)
                quadrants[q] += 1
        
        if min(quadrants) > 0:
            max_diff = max(quadrants) - min(quadrants)
            if max_diff > 5:
                return [ConstraintViolation(
                    constraint_name="quadrant_balance",
                    description=f"象限不平衡: {quadrants}",
                    severity="warning",
                    affected_wells=[]
                )]
        return []
