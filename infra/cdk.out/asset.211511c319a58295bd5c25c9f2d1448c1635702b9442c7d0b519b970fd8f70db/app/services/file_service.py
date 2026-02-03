"""File parsing service."""
import io
from typing import Optional
import pandas as pd

from app.models import SourcePlate, SourceWell


class FileService:
    """Service for parsing source plate files."""
    
    # Column name mappings
    COLUMN_MAPPING = {
        'plate_barcode': ['plate_barcode', 'Plate Barcode', 'Source Plate', 'barcode', 'Barcode'],
        'well_alpha': ['well_alpha', 'Well', 'Position', 'Source Well', 'well', 'Well Position'],
        'gene_symbol': ['gene_symbol', 'Gene', 'Gene Symbol', 'GENE_SYMBOL', 'gene', 'Gene_Symbol'],
        'volume': ['Volume_Requested', 'Volume', 'Transfer Volume', 'volume', 'Vol'],
        'concentration': ['Concentration', 'concentration', 'Conc'],
    }
    
    def parse_file(self, content: bytes, filename: str) -> SourcePlate:
        """
        Parse uploaded file and return SourcePlate.
        
        Args:
            content: File content as bytes
            filename: Original filename
            
        Returns:
            SourcePlate with parsed data
        """
        # Determine file type
        if filename.endswith('.csv'):
            df = self._parse_csv(content)
        elif filename.endswith(('.xlsx', '.xls')):
            df = self._parse_excel(content)
        else:
            raise ValueError(f"不支持的文件格式: {filename}")
        
        # Map columns
        column_map = self._detect_columns(df)
        
        # Extract data
        wells = []
        barcode = None
        
        for _, row in df.iterrows():
            # Get barcode (use first non-null value)
            if barcode is None and 'plate_barcode' in column_map:
                barcode = str(row[column_map['plate_barcode']])
            
            # Get well position
            position = str(row[column_map['well_alpha']]) if 'well_alpha' in column_map else None
            if not position:
                continue
            
            # Normalize position format (A1 -> A01)
            position = self._normalize_position(position)
            
            # Get gene symbol
            gene = str(row[column_map['gene_symbol']]) if 'gene_symbol' in column_map else None
            if not gene or gene == 'nan':
                continue
            
            # Get optional fields
            volume = None
            if 'volume' in column_map:
                try:
                    volume = float(row[column_map['volume']])
                except (ValueError, TypeError):
                    pass
            
            concentration = None
            if 'concentration' in column_map:
                try:
                    concentration = float(row[column_map['concentration']])
                except (ValueError, TypeError):
                    pass
            
            wells.append(SourceWell(
                position=position,
                gene_symbol=gene,
                volume=volume,
                concentration=concentration
            ))
        
        if not wells:
            raise ValueError("文件中没有找到有效的孔位数据")
        
        return SourcePlate(
            barcode=barcode or "UNKNOWN",
            wells=wells
        )
    
    def _parse_csv(self, content: bytes) -> pd.DataFrame:
        """Parse CSV file."""
        # Try different encodings
        for encoding in ['utf-8', 'gbk', 'latin1']:
            try:
                return pd.read_csv(io.BytesIO(content), encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError("无法解析 CSV 文件编码")
    
    def _parse_excel(self, content: bytes) -> pd.DataFrame:
        """Parse Excel file."""
        # Read all sheets and find the one with source data
        xl = pd.ExcelFile(io.BytesIO(content))
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name)
            # Check if this sheet has the expected columns
            if self._has_required_columns(df):
                return df
        
        # If no sheet matches, return the first one
        return pd.read_excel(io.BytesIO(content))
    
    def _has_required_columns(self, df: pd.DataFrame) -> bool:
        """Check if dataframe has required columns."""
        columns_lower = [c.lower() for c in df.columns]
        
        # Must have well position and gene symbol
        has_well = any(
            alias.lower() in columns_lower 
            for alias in self.COLUMN_MAPPING['well_alpha']
        )
        has_gene = any(
            alias.lower() in columns_lower 
            for alias in self.COLUMN_MAPPING['gene_symbol']
        )
        
        return has_well and has_gene
    
    def _detect_columns(self, df: pd.DataFrame) -> dict:
        """Detect column mappings."""
        column_map = {}
        
        for standard_name, aliases in self.COLUMN_MAPPING.items():
            for col in df.columns:
                if col in aliases or col.lower() in [a.lower() for a in aliases]:
                    column_map[standard_name] = col
                    break
        
        # Validate required columns
        if 'well_alpha' not in column_map:
            raise ValueError("缺少必填列: 孔位置 (Well)")
        if 'gene_symbol' not in column_map:
            raise ValueError("缺少必填列: 基因名称 (Gene Symbol)")
        
        return column_map
    
    def _normalize_position(self, position: str) -> str:
        """Normalize well position to A01 format."""
        position = position.strip().upper()
        
        # Handle A1 -> A01
        if len(position) == 2 and position[0].isalpha() and position[1].isdigit():
            return f"{position[0]}0{position[1]}"
        
        # Handle A01 format
        if len(position) == 3 and position[0].isalpha():
            return position
        
        return position
