import motor.motor_asyncio
from pymongo.server_api import ServerApi
from DataModel import Notice_B
from Config import connection_string

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
       
    def insert(self, data :Notice_B):
            # Get the database
            db = self.client["inha_notice"]
            # Get the collection
            collection = db["notice"]
            # Insert the data
            if not self._check_duplicate(data):
                collection.insert_one(data.to_dict())
        
    def need_update(self, data :Notice_B):
        db = self.client["inha_notice"]
        collection = db["notice"]
        e = collection.find_one({"url": data.url}) 
        if e is not None:
            item = Notice_B.from_dict(e)
            if item.published_date != data.published_date:
                return item
            return False
        return None
    
    async def update(self, data :Notice_B):
        if data.id is None:
            raise ValueError("The data must have an id to update")
        db = self.client["inha_notice"]
        collection = db["notice"]

        result = await collection.update_one({"_id": data.id}, {"$set": data.to_dict()})
        return result.modified_count > 0

    async def get_notices_by_filter(self, skip:int, limit:int, filters = {}) -> list:
        db = self.client["inha_notice"]
        collection = db["notice"]
        
        filt = {}
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
        result = await db.get_notices_by_filter(skip = 0, limit = 20, filters={"source" : "학교공지"})
        for notice in result:
            print(Notice_B.from_dict(notice))

    asyncio.run(test())
        