"""Plate layout data models."""
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from app.models.design_parameters import PlateType, PLATE_DIMENSIONS


class ContentType(str, Enum):
    """Well content type."""
    EMPTY = "empty"
    SAMPLE = "sample"
    POSITIVE_CONTROL = "positive_control"
    NEGATIVE_CONTROL = "negative_control"
    BLANK = "blank"


class LayoutWell(BaseModel):
    """Layout well definition."""
    position: str  # e.g., "A01"
    row: int  # 0-based
    col: int  # 0-based
    content_type: ContentType
    gene_symbol: Optional[str] = None
    replicate_index: Optional[int] = None
    source_plate: Optional[str] = None
    source_well: Optional[str] = None


class PlateLayout(BaseModel):
    """Plate layout definition."""
    plate_barcode: str
    plate_type: PlateType
    plate_index: int = 0
    wells: List[LayoutWell]
    
    def get_well(self, position: str) -> Optional[LayoutWell]:
        """Get well by position."""
        for well in self.wells:
            if well.position == position:
                return well
        return None
    
    def get_wells_by_gene(self, gene_symbol: str) -> List[LayoutWell]:
        """Get all wells for a gene."""
        return [w for w in self.wells if w.gene_symbol == gene_symbol]
    
    def to_matrix(self) -> List[List[Optional[str]]]:
        """Convert to 2D matrix for visualization."""
        rows, cols = PLATE_DIMENSIONS[self.plate_type.value]
        matrix = [[None for _ in range(cols)] for _ in range(rows)]
        for well in self.wells:
            if well.content_type != ContentType.EMPTY:
                matrix[well.row][well.col] = well.gene_symbol or well.content_type.value
        return matrix


class SolveStatus(str, Enum):
    """Solve status enumeration."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class ConstraintViolation(BaseModel):
    """Constraint violation details."""
    constraint_name: str
    description: str
    severity: str  # "error" or "warning"
    affected_wells: List[str] = []


class SolveResult(BaseModel):
    """Constraint solver result."""
    status: SolveStatus
    layouts: List[PlateLayout] = []
    violations: List[ConstraintViolation] = []
    relaxed_constraints: List[str] = []
    solve_time_ms: int = 0
    message: Optional[str] = None
