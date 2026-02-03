"""Source plate data models."""
from pydantic import BaseModel
from typing import List, Optional


class SourceWell(BaseModel):
    """Source plate well."""
    position: str  # e.g., "A01"
    gene_symbol: str
    volume: Optional[float] = None  # µL
    concentration: Optional[float] = None


class SourcePlate(BaseModel):
    """Source plate containing samples."""
    barcode: str
    plate_type: str = "384PP_AQ_BP"
    wells: List[SourceWell]
    
    def get_genes(self) -> List[str]:
        """Get unique gene symbols."""
        return list(set(w.gene_symbol for w in self.wells))
    
    def find_well(self, gene_symbol: str) -> Optional[SourceWell]:
        """Find well by gene symbol."""
        for well in self.wells:
            if well.gene_symbol == gene_symbol:
                return well
        return None
    
    def get_wells_by_gene(self, gene_symbol: str) -> List[SourceWell]:
        """Get all wells for a gene."""
        return [w for w in self.wells if w.gene_symbol == gene_symbol]
