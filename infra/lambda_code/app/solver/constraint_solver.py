"""PLAID constraint solver using MiniZinc + Gecode (no heuristic fallback)."""
import math
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from typing import List, Optional, Dict

import minizinc

from app.models import (
    SourcePlate, DesignParameters, PlateLayout, LayoutWell,
    ContentType, SolveResult, SolveStatus, ConstraintViolation,
    PlateType, PLATE_DIMENSIONS
)
from app.solver.constraints import CONSTRAINT_PRIORITY, is_hard_constraint

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Path to the MiniZinc model file (next to this module)
MZN_MODEL_PATH = Path(__file__).parent / "plate_design.mzn"


class ConstraintSolver:
    """PLAID constraint solver — MiniZinc + Gecode only."""

    def __init__(self, params: DesignParameters):
        self.params = params
        self.rows, self.cols = params.get_plate_dimensions()
        self.edge = params.edge_empty_layers

        self.inner_rows = self.rows - 2 * self.edge
        self.inner_cols = self.cols - 2 * self.edge
        self.available_wells = self.inner_rows * self.inner_cols

    def solve(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        timeout_seconds: int = 180,
    ) -> SolveResult:
        """Solve the plate layout problem using MiniZinc.

        No heuristic fallback — returns FAILED on any error.
        """
        start_time = time.time()

        total_samples = sum(self.params.get_replicates_for_gene(gene) for gene in genes)
        total_controls = sum(c.count for c in self.params.controls)
        total_needed = total_samples + total_controls

        num_plates = math.ceil(total_needed / self.available_wells)

        if num_plates > 10:
            return SolveResult(
                status=SolveStatus.FAILED,
                message=f"需要 {num_plates} 个板，超过最大限制 (10)",
            )

        try:
            layouts = self._solve_with_minizinc(
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
                        message="布局生成完成，但存在约束违反",
                    )

                return SolveResult(
                    status=SolveStatus.SUCCESS,
                    layouts=layouts,
                    violations=violations,
                    solve_time_ms=solve_time,
                    message="MiniZinc 布局生成成功",
                )
            else:
                return SolveResult(
                    status=SolveStatus.FAILED,
                    solve_time_ms=solve_time,
                    message="MiniZinc 无法找到满足约束的布局",
                )

        except Exception as e:
            solve_time = int((time.time() - start_time) * 1000)
            logger.exception("MiniZinc solver error")
            return SolveResult(
                status=SolveStatus.FAILED,
                solve_time_ms=solve_time,
                message=f"MiniZinc 求解器错误: {e}",
            )

    # ------------------------------------------------------------------ #
    # MiniZinc solver
    # ------------------------------------------------------------------ #

    def _solve_with_minizinc(
        self,
        genes: List[str],
        source_plate: SourcePlate,
        num_plates: int,
        timeout_seconds: int,
    ) -> Optional[List[PlateLayout]]:
        """Solve using MiniZinc + Gecode."""

        data = self._build_mzn_data(genes, num_plates)

        logger.info("=== MiniZinc 求解开始 ===")
        logger.info(
            f"板类型: {self.params.plate_type}, "
            f"{self.rows}x{self.cols}, edge={self.edge}, "
            f"plates={num_plates}, experiments={data['num_experiments']}"
        )

        model = minizinc.Model(str(MZN_MODEL_PATH))
        solver = minizinc.Solver.lookup("gecode")
        instance = minizinc.Instance(solver, model)

        # Assign all data parameters
        for key, value in data.items():
            instance[key] = value

        # MiniZinc sync solve() cannot run inside an asyncio event loop
        # (FastAPI), so run it in a thread pool.
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                instance.solve, timeout=timedelta(seconds=timeout_seconds)
            )
            result = future.result(timeout=timeout_seconds + 30)

        logger.info(f"MiniZinc result status: {result.status}")

        if result.status in (
            minizinc.Status.OPTIMAL_SOLUTION,
            minizinc.Status.SATISFIED,
            minizinc.Status.ALL_SOLUTIONS,
        ):
            logger.info(f"MiniZinc 求解成功, status={result.status}")
            return self._extract_solution(result, genes, source_plate, num_plates, data)
        else:
            logger.error(f"MiniZinc 求解失败, status={result.status}")
            return None

    def _build_mzn_data(self, genes: List[str], num_plates: int) -> dict:
        """Build the data dictionary to pass into the MiniZinc model."""

        num_compounds = len(genes)
        compound_replicates = [self.params.get_replicates_for_gene(g) for g in genes]

        num_controls = len(self.params.controls)
        control_replicates = [c.count for c in self.params.controls]

        # Build experiment -> compound_id mapping
        # Compounds use IDs 1..num_compounds, controls use num_compounds+1..
        experiment_compound_id: List[int] = []
        for c_idx, reps in enumerate(compound_replicates, start=1):
            experiment_compound_id.extend([c_idx] * reps)
        for ctrl_idx, reps in enumerate(control_replicates, start=num_compounds + 1):
            experiment_compound_id.extend([ctrl_idx] * reps)

        return {
            "num_plates": num_plates,
            "num_rows": self.rows,
            "num_cols": self.cols,
            "size_empty_edge": self.edge,
            "num_compounds": num_compounds,
            "compound_replicates": compound_replicates,
            "num_controls": num_controls,
            "control_replicates": control_replicates if num_controls > 0 else [],
            "num_experiments": len(experiment_compound_id),
            "experiment_compound_id": experiment_compound_id,
            # Constraint toggles
            "enable_no_adjacent": True,
            "enable_spread_rows": True,
            "enable_spread_cols": True,
            "enable_quadrant_balance": True,
            "enable_row_col_balance": True,
            "enable_control_spread": num_controls > 0,
        }

    def _extract_solution(
        self,
        result,
        genes: List[str],
        source_plate: SourcePlate,
        num_plates: int,
        data: dict,
    ) -> List[PlateLayout]:
        """Extract PlateLayout objects from a MiniZinc result."""

        exp_plate = result["experiment_plate"]   # 1-indexed plates
        exp_row = result["experiment_row"]
        exp_col = result["experiment_col"]

        # Rebuild samples list matching experiment_compound_id order
        samples: List[dict] = []
        for c_idx, gene in enumerate(genes):
            reps = self.params.get_replicates_for_gene(gene)
            for rep in range(reps):
                samples.append({"gene": gene, "rep": rep, "type": "sample"})
        for ctrl in self.params.controls:
            for rep in range(ctrl.count):
                samples.append({"name": ctrl.name, "ctrl_type": ctrl.type, "rep": rep, "type": "control"})

        # Group by plate
        plates_data: Dict[int, List] = {p: [] for p in range(num_plates)}
        for e_idx in range(len(samples)):
            p = exp_plate[e_idx] - 1  # convert to 0-indexed
            r = exp_row[e_idx]
            c = exp_col[e_idx]
            plates_data[p].append((r, c, samples[e_idx]))

        layouts = []
        for plate_idx in range(num_plates):
            wells = []
            placement = set()

            # Edge wells
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r < self.edge or r >= self.rows - self.edge
                            or c < self.edge or c >= self.cols - self.edge):
                        wells.append(LayoutWell(
                            position=self._format_position(r, c),
                            row=r, col=c,
                            content_type=ContentType.EMPTY,
                        ))

            # Placed experiments
            for r, c, sample in plates_data.get(plate_idx, []):
                placement.add((r, c))
                if sample["type"] == "sample":
                    gene = sample["gene"]
                    source_well = source_plate.find_well(gene)
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r, col=c,
                        content_type=ContentType.SAMPLE,
                        gene_symbol=gene,
                        replicate_index=sample["rep"],
                        source_plate=source_plate.barcode,
                        source_well=source_well.position if source_well else None,
                    ))
                else:
                    from app.models import ControlType
                    ct_map = {
                        ControlType.POSITIVE: ContentType.POSITIVE_CONTROL,
                        ControlType.NEGATIVE: ContentType.NEGATIVE_CONTROL,
                        ControlType.BLANK: ContentType.BLANK,
                    }
                    wells.append(LayoutWell(
                        position=self._format_position(r, c),
                        row=r, col=c,
                        content_type=ct_map.get(sample["ctrl_type"], ContentType.POSITIVE_CONTROL),
                        gene_symbol=sample.get("name"),
                        replicate_index=sample["rep"],
                    ))

            # Empty inner wells
            for r in range(self.edge, self.rows - self.edge):
                for c in range(self.edge, self.cols - self.edge):
                    if (r, c) not in placement:
                        wells.append(LayoutWell(
                            position=self._format_position(r, c),
                            row=r, col=c,
                            content_type=ContentType.EMPTY,
                        ))

            layouts.append(PlateLayout(
                plate_barcode=f"plate_{plate_idx + 1}",
                plate_type=self.params.plate_type,
                plate_index=plate_idx,
                wells=wells,
            ))

        return layouts

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

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
                for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    neighbor = pos_map.get((well.row + dr, well.col + dc))
                    if (neighbor and neighbor.content_type == ContentType.SAMPLE
                            and neighbor.gene_symbol == well.gene_symbol):
                        pair = tuple(sorted([well.position, neighbor.position]))
                        if pair not in checked:
                            checked.add(pair)
                            violations.append(ConstraintViolation(
                                constraint_name="no_adjacent_same_gene",
                                description=f"同一基因 {well.gene_symbol} 相邻: {pair[0]}, {pair[1]}",
                                severity="warning",
                                affected_wells=list(pair),
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
                    affected_wells=[],
                )]
        return []
