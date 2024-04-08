import asyncio
from typing import Optional
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from DataModel import Notice
from MongoDBWrapper import MongoDBWrapper

router = APIRouter()
@router.on_event("startup")
async def startup_event():
    global db
    db = await MongoDBWrapper.create()

@router.get("/notices")
async def get_notices(skip : int = Query(0, ge = 0), limit : int = Query(20, ge = 1), keyword : Optional[str] = None, category : Optional[str] = None, source : Optional[str] = None):
    filt = {}
    if keyword is not None:
        filt["title"] = keyword
        filt["content"] = keyword
    if category is not None:
        filt["category"] = category
    if source is not None:
        filt["source"] = source

    raw_res = await db.get_notices_by_filter(skip, limit, filters=filt)
    if len(raw_res) == 0:
        return JSONResponse(content = {"message" : "필터에 일치하는 데이터가 없습니다."}, status_code = 404)
    
    #데이터는 있는 상황
    total_count = await db.count_notice()
    f = ['id','title', 'url', 'category', 'source', 'published_date', 'scraped_date']
    res = [Notice.from_dict(i).to_dict_with_fields(*f) for i in raw_res]
    respose = {
        "total_count" : total_count,
        "page" : skip // limit + 1,
        "page_size" : limit,
        "total_page" : (total_count - 1) // limit + 1,
        "notices" : res,
    }
    return respose

@router.get("/notices/{notice_id}")
async def get_notice(notice_id: str):
    raw_res = await db.get_notices_by_filter(skip = 0, limit= 1,id = notice_id)
    f = ['id','title', 'content','url', 'category', 'source', 'published_date', 'scraped_date']
    temp = Notice.from_dict(raw_res[0])
    return temp.to_dict_with_fields(*f)
    
