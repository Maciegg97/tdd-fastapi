from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    response_object = {
        "id": summary_id,
        "url": payload.url
    }
    return response_object


@router.get("/{_id}/", response_model=SummarySchema, status_code=200)
async def read_summary(_id: int) -> SummarySchema:
    summary = await crud.get(_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=list[SummarySchema], status_code=200)
async def read_all_summaries() -> list[SummarySchema]:
    summaries = await crud.get_all()
    return summaries
