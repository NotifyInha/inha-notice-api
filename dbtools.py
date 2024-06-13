import datetime
import pymongo
import dateutil.parser
import pytz
from Config import connection_string
from app.Summarizer.Summarizer import Summarizer
current_tz = pytz.timezone('UTC')
local_timezone = pytz.timezone('Asia/Seoul')
def getDatetimeFromISO(s):
    if type(s) == datetime.datetime:
        s = current_tz.localize(s)
        s = s.astimezone(local_timezone)
        return s
    d = dateutil.parser.parse(s)
    d = current_tz.localize(d)
    d = d.astimezone(local_timezone)
    return d

client = pymongo.MongoClient(connection_string)

db = client["inha_notice"]
collection = db["notice"]

for i in collection.find():
    # i["published_date"] = getDatetimeFromISO(i["published_date"])
    # i["scraped_date"] = getDatetimeFromISO(i["scraped_date"])
    
    if 'summary' not in i.keys() and len(i['content']) > 100:
        i["content"] = i["content"].replace(u'\xa0', u' ')
        i["content"] = i["content"].replace(u'\r', u'')
        try:
            summary = Summarizer.summarize(i['title'], i['content'])
        except Exception as e:
            summary = ""
    else:
        summary = i['content']
    i['summary'] = summary
    collection.update_one({"_id": i["_id"]}, {"$set": i})