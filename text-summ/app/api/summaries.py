from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.tortoise import SummarySchema

from app.models.pydantic import (  # isort: skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)

router = APIRouter()


@router.get("/", response_model=List[SummarySchema])
async def get_all_summaries() -> List[SummarySchema]:
    all_summaries = await crud.get_all()

    return all_summaries


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)
    response_object = {"id": summary_id, "url": payload.url}

    return SummaryResponseSchema(**response_object)


@router.get("/{summary_id}/", response_model=SummarySchema)
async def read_summary(summary_id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.delete("/{summary_id}/", response_model=SummaryResponseSchema)
async def delete_summary(summary_id: int = Path(..., gt=0)) -> SummaryResponseSchema:
    summary = await crud.get(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(summary_id)

    return summary


@router.put("/{summary_id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema, summary_id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.put(summary_id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary
