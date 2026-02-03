"""Design parameters data models."""
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum


class PlateType(int, Enum):
    """Plate type enumeration."""
    PLATE_96 = 96
    PLATE_384 = 384
    PLATE_1536 = 1536


class Distribution(str, Enum):
    """Sample distribution method."""
    RANDOM = "random"
    COLUMN = "column"
    ROW = "row"
    UNIFORM = "uniform"


class ControlType(str, Enum):
    """Control type enumeration."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    BLANK = "blank"


class Control(BaseModel):
    """Control configuration."""
    type: ControlType
    name: str
    count: int
    source_well: Optional[str] = None


class GeneConfig(BaseModel):
    """Per-gene configuration."""
    gene_symbol: str
    replicates: int
    transfer_volume: float = 2.5  # nL, default 2.5nL


class DesignParameters(BaseModel):
    """Plate design parameters."""
    plate_type: PlateType = PlateType.PLATE_96
    replicates: int = 6  # 默认重复数（当没有指定per-gene配置时使用）
    edge_empty_layers: int = 1
    distribution: Distribution = Distribution.UNIFORM
    controls: List[Control] = []
    transfer_volume: float = 2.5  # 默认转移体积 (nL)
    gene_configs: Dict[str, GeneConfig] = {}  # 每个基因的特定配置
    
    @classmethod
    def default(cls) -> "DesignParameters":
        """Create default parameters."""
        return cls(
            plate_type=PlateType.PLATE_96,
            replicates=6,
            edge_empty_layers=1,
            distribution=Distribution.UNIFORM,
            transfer_volume=2.5
        )
    
    def get_replicates_for_gene(self, gene: str) -> int:
        """Get replicate count for a specific gene."""
        if gene in self.gene_configs:
            return self.gene_configs[gene].replicates
        return self.replicates
    
    def get_volume_for_gene(self, gene: str) -> float:
        """Get transfer volume for a specific gene."""
        if gene in self.gene_configs:
            return self.gene_configs[gene].transfer_volume
        return self.transfer_volume
    
    def get_plate_dimensions(self) -> tuple:
        """Get plate dimensions (rows, cols)."""
        dimensions = {
            PlateType.PLATE_96: (8, 12),
            PlateType.PLATE_384: (16, 24),
            PlateType.PLATE_1536: (32, 48),
        }
        return dimensions[self.plate_type]
    
    def get_available_wells(self) -> int:
        """Get number of available wells (excluding edge)."""
        rows, cols = self.get_plate_dimensions()
        edge = self.edge_empty_layers
        return (rows - 2 * edge) * (cols - 2 * edge)


# Plate dimensions constant
PLATE_DIMENSIONS = {
    96: (8, 12),
    384: (16, 24),
    1536: (32, 48),
}

# Plate type names for Echo
PLATE_TYPE_NAMES = {
    96: "Corning_96_Uplate",
    384: "384PP_AQ_BP",
    1536: "1536LDV_AQ_B2",
}
