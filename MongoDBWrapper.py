from bson import ObjectId
import motor.motor_asyncio
from pymongo.server_api import ServerApi
from DataModel import Notice
from Config import connection_string
from fastapi_pagination.ext.motor import paginate


class MongoDBWrapper:
    def __init__(self, client) -> None:
        self.client:motor.motor_asyncio.AsyncIOMotorClient = client

    @classmethod
    async def create(cls):
        uri = connection_string
        client = motor.motor_asyncio.AsyncIOMotorClient(uri, server_api=ServerApi('1'))
        try:
            await client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return cls(client)
        except Exception as e:
            print(type(e), e)

    async def _check_duplicate(self, data :Notice):
        db = self.client["inha_notice"]
        collection = db["notice"]
        return await collection.find_one({"url": data.url}) is not None

    async def insert(self, data :Notice):
            # Get the database
            db = self.client["inha_notice"]
            # Get the collection
            collection = db["notice"]
            # Insert the data
            if await self.need_update(data) == None:
                await collection.insert_one(data.to_dict())
                return True
            return False
                
        
    async def need_update(self, data :Notice):
        db = self.client["inha_notice"]
        collection = db["notice"]
        e = await collection.find_one({"url": data.url}) 
        if e is not None:
            item = Notice.from_dict(e)
            if item.published_date != data.published_date:
                return item
            return False
        return None
    
    async def update(self, data :Notice):
        if data._id is None:
            raise ValueError("The data must have an id to update")
        db = self.client["inha_notice"]
        collection = db["notice"]

        result = await collection.update_one({"_id": data._id}, {"$set": data.to_dict()})
        return result.modified_count > 0

    async def get_notices_by_filter(self, skip:int, limit:int, filters = {}) -> list:
        db = self.client["inha_notice"]
        collection = db["notice"]
        
        filt = {}
        if "id" in filters:
            filt["_id"] = ObjectId(filters["id"])
        if "title" in filters:
            filt["title"] = {"$regex": filters["title"], "$options": "i"}
        if "content" in filters:
            filt["content"] = {"$regex": filters["content"], "$options": "i"}
        if "category" in filters:
            filt["category"] = filters["category"]
        if "source" in filters:
            filt["source"] = filters["source"]

        
        cursor = collection.find(filt).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    def get_collection(self):
        return self.client["inha_notice"]["notice"]


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
    
    async def delete(self, id):
        db = self.client["inha_notice"]
        collection = db["notice"]

        filt = {}
        filt["_id"] = ObjectId(id)

        result = await collection.delete_one(filt)
        return result.deleted_count > 0


if __name__ == "__main__":
    import asyncio
    async def test():
        db = await MongoDBWrapper.create()
        result = await db.get_notices_by_filter(skip = 0, limit = 20, filters={"source" : "학교공지"})
        for notice in result:
            print(Notice.from_dict(notice))

    asyncio.run(test())
        