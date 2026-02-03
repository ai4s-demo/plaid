"""File upload and parsing API."""
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services import FileService
from app.models import SourcePlate
from app.config import settings

router = APIRouter()
file_service = FileService()


@router.post("/parse", response_model=SourcePlate)
async def parse_file(file: UploadFile = File(...)):
    """
    Parse uploaded source plate file.
    
    Supports Excel (.xlsx, .xls) and CSV (.csv) formats.
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    allowed_extensions = ['.xlsx', '.xls', '.csv']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件格式，请上传 Excel 或 CSV 文件"
        )
    
    # Check file size
    content = await file.read()
    if len(content) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，请上传小于 {settings.max_file_size_mb}MB 的文件"
        )
    
    # Parse file
    try:
        source_plate = file_service.parse_file(content, file.filename)
        return source_plate
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件解析失败: {str(e)}")


@router.post("/validate")
async def validate_file(file: UploadFile = File(...)):
    """
    Validate file format without full parsing.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    allowed_extensions = ['.xlsx', '.xls', '.csv']
    is_valid = any(file.filename.lower().endswith(ext) for ext in allowed_extensions)
    
    return {
        "valid": is_valid,
        "filename": file.filename,
        "message": "文件格式有效" if is_valid else "不支持的文件格式"
    }
