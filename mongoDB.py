from pymongo import MongoClient
import json
import os

house_json_files = ['taipei_city_houses.json', 'new_taipei_city_houses.json']
# clinet = MongoClient("mongodb://localhost:27017/")
clinet = MongoClient("mongodb://mongodb:27017/")  # when we use docker-compose

# 創建資料庫與collection
db = clinet['database591']
col = db['houses']

# 資料新增至collection
for file_name in house_json_files:
    try:
        with open(os.path.join('data', file_name), 'r') as f:
            houses = json.load(f)

        # 資料新增至collection
        col.insert_many(houses['data'])
    except Exception as e:
        print(f'insert failed, error msg: {e}')