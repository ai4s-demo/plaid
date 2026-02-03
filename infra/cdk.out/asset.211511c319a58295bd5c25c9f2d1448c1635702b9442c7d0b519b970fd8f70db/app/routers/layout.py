"""Layout generation API."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List, Optional

from app.services import LayoutService
from app.models import (
    SourcePlate, DesignParameters, PlateLayout, 
    SolveResult, EchoPicklist
)

router = APIRouter()
layout_service = LayoutService()


class LayoutRequest(BaseModel):
    """Request for layout generation."""
    source_plate: SourcePlate
    parameters: DesignParameters


class UpdateRequest(BaseModel):
    """Request for layout update."""
    layout: PlateLayout
    from_position: str
    to_position: str


class PicklistRequest(BaseModel):
    """Request for picklist generation."""
    layouts: List[PlateLayout]
    source_plate: SourcePlate
    transfer_volume: float = 375.0


@router.post("/generate", response_model=SolveResult)
async def generate_layout(request: LayoutRequest):
    """
    Generate optimized plate layout.
    
    Uses PLAID constraints to create an optimal layout.
    """
    try:
        result = layout_service.generate_layout(
            source_plate=request.source_plate,
            params=request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"布局生成失败: {str(e)}")


@router.post("/validate")
async def validate_layout(layout: PlateLayout):
    """
    Validate layout against PLAID constraints.
    """
    issues = layout_service.validate_layout(layout)
    return {
        "valid": len([i for i in issues if i["type"] == "error"]) == 0,
        "issues": issues
    }


@router.put("/update", response_model=PlateLayout)
async def update_layout(request: UpdateRequest):
    """
    Update layout by swapping two wells.
    """
    updated = layout_service.update_layout(
        layout=request.layout,
        from_position=request.from_position,
        to_position=request.to_position
    )
    return updated


@router.post("/picklist", response_model=EchoPicklist)
async def generate_picklist(request: PicklistRequest):
    """
    Generate Echo picklist from layouts.
    """
    picklist = layout_service.generate_picklist(
        layouts=request.layouts,
        source_plate=request.source_plate,
        transfer_volume=request.transfer_volume
    )
    return picklist


@router.post("/picklist/csv")
async def generate_picklist_csv(request: PicklistRequest):
    """
    Generate Echo picklist as CSV.
    """
    picklist = layout_service.generate_picklist(
        layouts=request.layouts,
        source_plate=request.source_plate,
        transfer_volume=request.transfer_volume
    )
    return PlainTextResponse(
        content=picklist.to_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=picklist.csv"}
    )
