from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
import pytz
from DataModel import Notice, NoticeCreate, NoticeGet, NoticeUpdate
from MongoDBWrapper import MongoDBWrapper
from fastapi_pagination import Page, add_pagination
from typing import Any, Dict, Optional

from fastapi_pagination.api import apply_items_transformer, create_page
from fastapi_pagination.bases import AbstractParams
from fastapi_pagination.types import AdditionalData, AsyncItemsTransformer
from fastapi_pagination.utils import verify_params

from Univutil.UnivFactory import InhaUnivFactory

router = APIRouter()
local_timezone = pytz.timezone('Asia/Seoul')
#대학 변경시 변경
univFunction = InhaUnivFactory().get_univutil()

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

@router.get("/notices", description="필터링된 공지사항 목록을 반환합니다.")
async def get_notices( keyword : Optional[str] = Query(None), category : Optional[str] = Query(None), sourcefilter : Optional[int] = Query(0), major : Optional[str] = Query(None) ,date:Optional[str] = Query(None),url : Optional[str] = Query(None)) ->Page[NoticeGet]:
    mainfilter = univFunction.deserializesource(sourcefilter)
    majorfilter = univFunction.deserializemajor(major)
    sfilt = []
    filt = {"$and" : []}
    if keyword is not None:
        filt["$and"].append({"$or" : [{"title": {"$regex": keyword}}, {"content": {"$regex": keyword}}]})
    if category is not None:
        filt["$and"].append({"category":category})
    if mainfilter != []:
        sfilt.extend([{"source": i} for i in mainfilter])
    if url is not None:
        filt["$and"].append({"url":url})
    if date is not None:
        dates = date.split(',')
        filt["$and"].append({"published_date" : {"$gte" : datetime.fromisoformat(dates[0]), "$lte" : datetime.fromisoformat(dates[1])}})
    if majorfilter != []:
        sfilt.extend([{"source": i} for i in majorfilter])

    if sfilt != []:
        filt["$and"].append({"$or" : sfilt})


    if filt["$and"] == []:
        filt = {}
    return await paginate(db.get_collection(), query_filter=filt, sort={"published_date" : -1}, projection={"content": 0, "images": 0, "attached": 0, "is_sent_notification": 0, "scraped_date": 0})

@router.get("/notices/{notice_id}" , description="특정 id에 대한 공지사항을 반환합니다.")
async def get_notice(notice_id: str) -> Notice:
    raw_res = await db.get_notices_by_filter(skip = 0, limit= 1,filters={"id" : notice_id})
    if len(raw_res) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    f = ('_id','title', 'content','url', 'category', 'source', 'published_date', 'scraped_date', 'images', 'attached')
    temp = Notice.model_validate(raw_res[0])
    return temp


@router.post("/notices", description="새로운 공지사항을 저장합니다. 기존 공지사항을 업데이트 하기 위해선 PUT를 사용해야합니다.")
async def post_notice(notice: NoticeCreate):
    notice = notice.model_dump()
    notice['scraped_date'] = datetime.now().astimezone(local_timezone).isoformat()
    res = await db.insert(notice)
    if not res:
        raise HTTPException(status_code=409, detail="중복된 데이터가 존재합니다.")
    return {"message" : "데이터가 성공적으로 저장되었습니다."}

@router.put("/notices/{notice_id}" , description="특정 id에 대한 공지사항을 수정합니다. 제공되지 않은 필드는 수정되지 않습니다. force가 True일 경우 데이터가 최신이 아니더라도 수정합니다.")
async def put_notice(notice_id: str, notice: NoticeUpdate, force:Optional[bool] = False):
    notice._id = notice_id
    before = await db.get_notices_by_filter(0,1,{"id" : notice_id})
    if len(before) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    before = Notice.model_validate(before[0])
    if not force and await db.need_update(notice.model_dump()) is False:
        raise HTTPException(status_code=409, detail="데이터가 이미 최신입니다.")
    await db.update(notice_id, notice)
    return {"message" : "데이터가 성공적으로 수정되었습니다.", "before" : before.model_dump(), "after" : notice.model_dump()}

@router.delete("/notices/{notice_id}", description="특정 id에 대한 공지사항을 삭제 후 삭제한 공지사항을 반환합니다.")
async def delete_notice(notice_id: str):
    before = await db.get_notices_by_filter(0,1,{"id" : notice_id})
    if len(before) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    before = Notice.model_validate(before[0])
    res = await db.delete(notice_id)
    if not res:
        raise HTTPException(status_code=500)
    return {"message" : "데이터가 성공적으로 삭제되었습니다.", "before" : before.model_dump()}

add_pagination(router)