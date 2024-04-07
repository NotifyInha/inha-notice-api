import motor.motor_asyncio
from DataModel import Notice
from Config import connection_string

class MongoDBWrapper:
    def __init__(self, client) -> None:
        self.client = client

    @classmethod
    async def create(cls):
        uri = connection_string
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        try:
            await client.admin.command("ping")
            return cls(client)
        except Exception as e:
            print(type(e), e)
       


    async def get_notices_by_filter(self, skip:int, limit:int, **kwargs) -> list:
        db = self.client["inha_notice"]
        collection = db["notice"]
        
        filt = {}
        if "title" in kwargs:
            filt["title"] = {"$regex": kwargs["title"], "$options": "i"}
        if "content" in kwargs:
            filt["content"] = {"$regex": kwargs["content"], "$options": "i"}
        if "category" in kwargs:
            filt["category"] = kwargs["category"]
        if "source" in kwargs:
            filt["source"] = kwargs["source"]

        
        cursor = collection.find(filt).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def count_notice(self, **kwargs) -> int:
        db = self.client["inha_notice"]
        collection = db["notice"]
        
        filt = {}
        if "title" in kwargs:
            filt["title"] = {"$regex": kwargs["title"], "$options": "i"}
        if "content" in kwargs:
            filt["content"] = {"$regex": kwargs["content"], "$options": "i"}
        if "category" in kwargs:
            filt["category"] = kwargs["category"]
        if "source" in kwargs:
            filt["source"] = kwargs["source"]
        
        return await collection.count_documents(filt)

if __name__ == "__main__":
    import asyncio
    async def test():
        db = await MongoDBWrapper.create()
        result = await db.get_notices_by_filter(skip = 0, limit = 20, source = "학교공지")
        for notice in result:
            print(Notice.from_dict(notice))

    asyncio.run(test())
        