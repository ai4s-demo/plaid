"""Echo picklist data models."""
from pydantic import BaseModel
from typing import List, Optional


class PicklistEntry(BaseModel):
    """Single picklist entry for Echo."""
    source_plate_barcode: str
    source_well: str  # A01 format
    source_plate_type: str
    destination_plate_barcode: str
    destination_plate_type: str
    destination_well: str  # A01 format
    transfer_volume: float  # nL
    gene_symbol: str
    compound_label: Optional[str] = None
    ensembl_id: Optional[str] = None


class EchoPicklist(BaseModel):
    """Echo picklist containing all transfer entries."""
    entries: List[PicklistEntry]
    
    def to_csv(self) -> str:
        """Export to CSV format."""
        headers = [
            "Source Plate Barcode",
            "Source Well",
            "Source Plate Type",
            "Destination Plate Barcode",
            "Destination Plate Type",
            "Destination Well",
            "Transfer Volume",
            "GENE_SYMBOL",
            "COMPOUND_LABEL",
            "ENSEMBL_ID"
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
                entry.gene_symbol,
                entry.compound_label or "N/A",
                entry.ensembl_id or "N/A"
            ])
            lines.append(line)
        
        return "\n".join(lines)
