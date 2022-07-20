from typing import List

from fastapi import HTTPException

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema):
    summary = TextSummary(url=payload.url, summary="Dummy..")
    await summary.save()
    return summary.id


async def get(summary_id: int) -> dict | None:
    summary = await TextSummary.filter(id=summary_id).first().values()
    if not summary:
        raise HTTPException(status_code=404, detail=f"Summary {summary_id} not found!")
    return summary


async def get_all() -> List:
    all_summaries = await TextSummary.all().values()

    return all_summaries
