from typing import List

from fastapi import APIRouter

from app.models import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)
    response_object = {"id": summary_id, "url": payload.url}

    return SummaryResponseSchema(**response_object)


@router.get("/{summary_id}", response_model=SummaryResponseSchema)
async def get_summary(summary_id: int) -> SummarySchema:
    summary = await crud.get(summary_id)

    return summary


@router.get("/", response_model=List[SummarySchema])
async def get_all_summaries() -> List[SummarySchema]:
    all_summaries = await crud.get_all()

    return all_summaries
