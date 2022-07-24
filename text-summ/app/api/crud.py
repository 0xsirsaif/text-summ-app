from typing import List

from fastapi import HTTPException

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary

from app.models.pydantic import SummaryUpdatePayloadSchema  # isort: skip


async def post(payload: SummaryPayloadSchema):
    summary = TextSummary(url=payload.url, summary="")
    await summary.save()
    return summary.id


async def get(summary_id: int) -> dict | None:
    summary = await TextSummary.filter(id=summary_id).first().values()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


async def get_all() -> List:
    all_summaries = await TextSummary.all().values()

    return all_summaries


async def delete(summary_id: int) -> int:
    summary = await TextSummary.filter(id=summary_id).delete()
    return summary


async def put(id: int, payload: SummaryUpdatePayloadSchema) -> dict | None:
    summary = await TextSummary.filter(id=id).update(
        url=payload.url, summary=payload.summary
    )
    if summary:
        updated_summary = await TextSummary.filter(id=id).first().values()
        return updated_summary
    return None
