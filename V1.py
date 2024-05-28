import asyncio
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from DataModel import Notice, Notice_B
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
    res = [Notice_B.from_dict(i).to_dict_with_fields(*f) for i in raw_res]
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


@router.post("/notices")
async def post_notice(notice: Notice):
    await db.insert_notice(notice)
    return {"message" : "데이터가 성공적으로 저장되었습니다."}

@router.put("/notices/{notice_id}")
async def put_notice(notice_id: str, notice: Notice, force:bool = False):
    notice.id = notice_id
    before = await db.get_notices_by_filter(0,1,{"id" : notice.id})
    if len(before) == 0:
        raise HTTPException(status_code=404, detail="해당 id에 대한 데이터가 없습니다.")
    before = Notice_B.from_dict(before[0])
    if not force and await db.need_update(notice) is False:
        raise HTTPException(status_code=409, detail="데이터가 이미 최신입니다.")
    await db.update(notice)
    return {"message" : "데이터가 성공적으로 수정되었습니다.", "before" : before.to_dict(), "after" : notice.to_dict()}