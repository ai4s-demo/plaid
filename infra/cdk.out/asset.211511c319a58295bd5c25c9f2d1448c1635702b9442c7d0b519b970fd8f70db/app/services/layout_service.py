"""Layout generation service."""
from typing import List, Optional

from app.models import (
    SourcePlate, DesignParameters, PlateLayout, 
    SolveResult, PicklistEntry, EchoPicklist,
    ContentType, PLATE_TYPE_NAMES
)
from app.solver import ConstraintSolver
from app.config import settings


class LayoutService:
    """Service for generating and managing plate layouts."""
    
    def generate_layout(
        self,
        source_plate: SourcePlate,
        params: DesignParameters
    ) -> SolveResult:
        """
        Generate optimized plate layout.
        
        Args:
            source_plate: Source plate with samples
            params: Design parameters
            
        Returns:
            SolveResult with layout(s) or error
        """
        # Get genes from source plate
        genes = source_plate.get_genes()
        
        if not genes:
            return SolveResult(
                status="failed",
                message="源板中没有找到基因"
            )
        
        # Create solver and solve
        solver = ConstraintSolver(params)
        result = solver.solve(
            genes=genes,
            source_plate=source_plate,
            timeout_seconds=settings.solver_timeout_seconds
        )
        
        return result
    
    def validate_layout(self, layout: PlateLayout) -> List[dict]:
        """
        Validate layout against PLAID constraints.
        
        Args:
            layout: Layout to validate
            
        Returns:
            List of validation issues
        """
        issues = []
        
        # Check for duplicate positions
        positions = [w.position for w in layout.wells]
        duplicates = set([p for p in positions if positions.count(p) > 1])
        if duplicates:
            issues.append({
                "type": "error",
                "message": f"重复的孔位: {', '.join(duplicates)}"
            })
        
        # Check edge constraint
        params = DesignParameters(plate_type=layout.plate_type)
        rows, cols = params.get_plate_dimensions()
        edge = params.edge_empty_layers
        
        for well in layout.wells:
            if well.content_type != ContentType.EMPTY:
                if (well.row < edge or well.row >= rows - edge or
                    well.col < edge or well.col >= cols - edge):
                    issues.append({
                        "type": "warning",
                        "message": f"孔位 {well.position} 在边缘区域"
                    })
        
        return issues
    
    def generate_picklist(
        self,
        layouts: List[PlateLayout],
        source_plate: SourcePlate,
        transfer_volume: float = 375.0  # nL
    ) -> EchoPicklist:
        """
        Generate Echo picklist from layouts.
        
        Args:
            layouts: List of plate layouts
            source_plate: Source plate
            transfer_volume: Transfer volume in nL
            
        Returns:
            EchoPicklist with all entries
        """
        entries = []
        
        for layout in layouts:
            dest_plate_type = PLATE_TYPE_NAMES.get(
                layout.plate_type.value, 
                "Corning_96_Uplate"
            )
            
            for well in layout.wells:
                if well.content_type == ContentType.EMPTY:
                    continue
                
                # Find source well
                source_well = None
                if well.source_well:
                    source_well = well.source_well
                elif well.gene_symbol:
                    sw = source_plate.find_well(well.gene_symbol)
                    if sw:
                        source_well = sw.position
                
                if not source_well:
                    continue
                
                entry = PicklistEntry(
                    source_plate_barcode=source_plate.barcode,
                    source_well=source_well,
                    source_plate_type=source_plate.plate_type,
                    destination_plate_barcode=layout.plate_barcode,
                    destination_plate_type=dest_plate_type,
                    destination_well=well.position,
                    transfer_volume=transfer_volume,
                    gene_symbol=well.gene_symbol or well.content_type.value
                )
                entries.append(entry)
        
        return EchoPicklist(entries=entries)
    
    def update_layout(
        self,
        layout: PlateLayout,
        from_position: str,
        to_position: str
    ) -> PlateLayout:
        """
        Update layout by swapping two wells.
        
        Args:
            layout: Current layout
            from_position: Source position
            to_position: Target position
            
        Returns:
            Updated layout
        """
        # Find wells
        from_well = layout.get_well(from_position)
        to_well = layout.get_well(to_position)
        
        if not from_well or not to_well:
            return layout
        
        # Swap content
        new_wells = []
        for well in layout.wells:
            if well.position == from_position:
                new_wells.append(LayoutWell(
                    position=from_position,
                    row=from_well.row,
                    col=from_well.col,
                    content_type=to_well.content_type,
                    gene_symbol=to_well.gene_symbol,
                    replicate_index=to_well.replicate_index,
                    source_plate=to_well.source_plate,
                    source_well=to_well.source_well
                ))
            elif well.position == to_position:
                new_wells.append(LayoutWell(
                    position=to_position,
                    row=to_well.row,
                    col=to_well.col,
                    content_type=from_well.content_type,
                    gene_symbol=from_well.gene_symbol,
                    replicate_index=from_well.replicate_index,
                    source_plate=from_well.source_plate,
                    source_well=from_well.source_well
                ))
            else:
                new_wells.append(well)
        
        return PlateLayout(
            plate_barcode=layout.plate_barcode,
            plate_type=layout.plate_type,
            plate_index=layout.plate_index,
            wells=new_wells
        )
