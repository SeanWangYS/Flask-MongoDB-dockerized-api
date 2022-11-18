# Flask-MongoDB-api

## Description
此專案利用爬蟲技術取得[591租屋網](https://rent.591.com.tw/)中，位於台北及新北的所有租屋物件資料。將租屋資料存放置MongoDB中，
再利用Flask實作Restful CRUD API，對資料庫的租屋物件資料做新增、讀取、更新、刪除

## Flow 
### Spider 
- 以**篩選條件**與**排序依據**爬取對應的租屋物件
``` py3
filter_params = {
    'region': '3', # (地區) 新北市
    # 'searchtype': '4',  # (位置1) 按捷運搜尋
    # 'mrtline': '125',  # (位置2) 淡水信義線
    # 'mrtcoods': '4163,4164,4165,4166,4167',  # (位置3) 淡水, 紅樹林, 竹圍, 關渡, 忠義
}

# 排序依據
sort_params = {
    # 租金由小到大
    'order': 'money',  # posttime, area
    'orderType': 'acs',  # asc
    'other': 'near_subway', # 特色：近捷運
}
```  

### MongoDB
- document 格式設計如下
``` py3
{
    "_id" : ObjectId("5f572f6f771ff988c1794832"),
    "title":"大直全新裝潢~一層一戶",
    "region": "台北市", 
    "section": "大同區", 
    "house_kind": "3房2廳2衛", 
    "house_shape": "電梯大樓", 
    "price": 32000, 
    "roleName": "屋主", 
    "imName": "黃先生", 
    "mobile": "0933-123-456", 
    "phone": "02-8201-1234", 
    "rule": "此房屋限女生租住", 
    "post_id": "13107688"
}
``` 
### Flask restful api
- http-get方法, paylaod 格式設計如下
    - query：對 MongoDB collection 的搜尋條件
    - projection: 篩選回傳fields
``` py3
{
    "query": {"region":"新北市", "price":{"$lt":20000}, "rule":{"$regex":"限男"}},
    "projection": {"price":1 , "roleName":1, "imName":1, "mobile":1, "title":1, "rule":1, "_id":0}
}
```

