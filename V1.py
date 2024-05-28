from fastapi import APIRouter, HTTPException, Query
from DataModel import Notice, NoticeLight
from MongoDBWrapper import MongoDBWrapper
from fastapi_pagination import Page, add_pagination
from typing import Any, Dict, Optional

from fastapi_pagination.api import apply_items_transformer, create_page
from fastapi_pagination.bases import AbstractParams
from fastapi_pagination.types import AdditionalData, AsyncItemsTransformer
from fastapi_pagination.utils import verify_params

router = APIRouter()

async def paginate(
    collection,
    query_filter: Optional[Dict[Any, Any]] = None,
    projection: Optional[Dict[Any, Any]] = None,
    params: Optional[AbstractParams] = None,
    sort: Optional[Any] = None,
    *,
    transformer: Optional[AsyncItemsTransformer] = None,
    additional_data: Optional[AdditionalData] = None,
    **kwargs: Any,
) -> Any:
    params, raw_params = verify_params(params, "limit-offset")
    query_filter = query_filter or {}

    total = await collection.count_documents(query_filter) if raw_params.include_total else None
    cursor = collection.find(query_filter, projection, skip=raw_params.offset, limit=raw_params.limit, **kwargs)
    if sort is not None:
        cursor = cursor.sort(*sort) if isinstance(sort, tuple) else cursor.sort(sort)

    items = await cursor.to_list(length=raw_params.limit)
    t_items = await apply_items_transformer(items, transformer, async_=True)

    return create_page(
        t_items,
        total=total,
        params=params,
        **(additional_data or {}),
    )


@router.on_event("startup")
async def startup_event():
    global db
    db = await MongoDBWrapper.create()

@router.get("/notices")
async def get_notices( keyword : Optional[str] = Query(None), category : Optional[str] = Query(None), source : Optional[str] = Query(None)) ->Page[NoticeLight]:
    filt = {}
    if keyword is not None:
        filt["$or"] = [{"title": {"$regex": keyword}}, {"content": {"$regex": keyword}}]
    if category is not None:
        filt["category"] = category
    if source is not None:
        filt["source"] = source
    return await paginate(db.get_collection(), query_filter=filt, projection={"content": 0, "images": 0, "attached": 0, "is_sent_notification": 0, "scraped_date": 0})

@router.get("/notices/{notice_id}")
async def get_notice(notice_id: str):
    raw_res = await db.get_notices_by_filter(skip = 0, limit= 1,filters={"id" : notice_id})
    if len(raw_res) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    f = ['id','title', 'content','url', 'category', 'source', 'published_date', 'scraped_date']
    temp = Notice.from_dict(raw_res[0])
    return temp.to_dict_with_fields(*f)


@router.post("/notices")
async def post_notice(notice: Notice):
    res = await db.insert(notice)
    if not res:
        raise HTTPException(status_code=409, detail="중복된 데이터가 존재합니다.")
    return {"message" : "데이터가 성공적으로 저장되었습니다."}

@router.put("/notices/{notice_id}")
async def put_notice(notice_id: str, notice: Notice, force:bool = False):
    notice._id = notice_id
    before = await db.get_notices_by_filter(0,1,{"id" : notice._id})
    if len(before) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    before = Notice.from_dict(before[0])
    if not force and await db.need_update(notice) is False:
        raise HTTPException(status_code=409, detail="데이터가 이미 최신입니다.")
    await db.update(notice)
    return {"message" : "데이터가 성공적으로 수정되었습니다.", "before" : before.to_dict(), "after" : notice.to_dict()}

@router.delete("/notices/{notice_id}")
async def delete_notice(notice_id: str):
    before = await db.get_notices_by_filter(0,1,{"id" : notice_id})
    if len(before) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    before = Notice.from_dict(before[0])
    res = await db.delete(notice_id)
    if not res:
        raise HTTPException(status_code=500)
    return {"message" : "데이터가 성공적으로 삭제되었습니다.", "before" : before.to_dict()}

add_pagination(router)