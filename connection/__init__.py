from pymongo import MongoClient
import dns
# myc = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
myc = MongoClient('mongodb+srv://therealrahulsahu:rahulsahu1_@'
                  'democluster-2u6fb.gcp.mongodb.net/test?retryWrites=true', serverSelectionTimeoutMS=5000)
