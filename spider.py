import os
import time
import random
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

class Spider591:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }
    
    def get_house_post_ids(self, filter_params=None, sort_params=None, want_page=1):
        """
        :filter_params: 篩選參數
        :param sort_params: 排序參數
        :param want_page: 想要抓幾頁
        
        :return total_count: 搜尋條件下共找到幾筆
        :house_post_ids: 只搜集post_id 
        """
        total_count = 0
        house_post_ids = []
        page = 0
        
        # 紀錄 Cookie 取得 X-CSRF-TOKEN
        s = requests.Session()
        url = 'https://rent.591.com.tw/'
        r = s.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_item = soup.select_one('meta[name="csrf-token"]')

        headers = self.headers.copy()
        headers['X-CSRF-TOKEN'] = token_item.get('content')

        # 搜尋房屋
        url = 'https://rent.591.com.tw/home/search/rsList'
        params = 'is_format_data=1&is_new_list=1&type=1'
        # param 加入篩選參數
        if filter_params:
            params += ''.join([f'&{key}={val}' for key, val in filter_params.items()])
        else:
            params += '&region=1&kind=0'
        # 在 cookie 設定地區縣市，避免某些條件無法取得資料
        s.cookies.set('urlJumpIp', filter_params.get('region', '1') if filter_params else '1', domain='.591.com.tw')

        # 排序參數
        if sort_params:
            params += ''.join([f'&{key}={val}' for key, val, in sort_params.items()])
        
        while page < want_page:
            params += f'&firstRow={page*30}'
            r = s.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('request failed', r.status_code)
                break
            page+=1
            
            data = r.json()
            total_count = data['records']
            house_post_ids.extend([house_info['post_id'] for house_info in data['data']['data']])
            
            # 隨機暫停一段時間
            time.sleep(random.uniform(1, 2))
        
        return total_count, house_post_ids
    
    def get_house_detail(self, house_id):
        """ 房屋詳情
        :param house_id: 房屋ID
        :return house_detail: requests 房屋詳細資料
        """
        house_detail = {}
        
        # 紀錄 Cookie 取得 X-CSRF-TOKEN, deviceid
        s = requests.Session()
        url = f'https://rent.591.com.tw/home/{house_id}'
        r = s.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_item = soup.select_one('meta[name="csrf-token"]')

        headers = self.headers.copy()
        headers['X-CSRF-TOKEN'] = token_item.get('content')
        headers['deviceid'] = s.cookies.get_dict()['T591_TOKEN']
        headers['device'] = 'pc'

        url = f'https://bff.591.com.tw/v1/house/rent/detail?id={house_id}'
        r = s.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('request failed', r.status_code)
            return
        
        data = r.json()['data']
        price_str = data['price']  # '20,000'
        house_detail['title'] = data['title'] # title
        house_detail['region'] = data['breadcrumb'][0]['name'] # 縣市 region
        house_detail['section'] = data['breadcrumb'][1]['name'] # 區域 section
        house_detail['house_kind'] = data['info'][0]['value'] # 類型 house_kind
        house_detail['house_shape'] = data['info'][3]['value'] # 型態 house_shape
        house_detail['price'] = int(''.join(price_str.split(','))) # 價格 price
        house_detail['roleName'] = data['linkInfo']['roleName']  # 出租者身份
        house_detail['imName'] = data['linkInfo']['imName']  # 出租者
        house_detail['mobile'] = data['linkInfo']['mobile'] # mobile
        house_detail['phone'] = data['linkInfo']['phone'] # phone
        house_detail['rule'] = data['service']['rule']  # rule
        house_detail['post_id'] = str(house_id)
        
        return house_detail


if __name__ == "__main__":
    spider_591 = Spider591()
    # 篩選條件
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

    # 先確定需要抓幾頁
    total_count, test = spider_591.get_house_post_ids(filter_params, sort_params, want_page=1)
    want_page = int(''.join(total_count.split(','))) // 30 + 1
    # 搜集 post_id清單
    _, house_post_ids = spider_591.get_house_post_ids(filter_params, sort_params, want_page=want_page)

    # 逐一取得房屋詳細資料
    house_detail_list = []
    for house_id in tqdm(house_post_ids):
        try:
            house_detail = spider_591.get_house_detail(house_id)
            if house_detail is not None:
                house_detail_list.append(house_detail)
                time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f'house_post_ids:{house_id}, Error message: {e}')

    # save as json file
    json_format = {'data': house_detail_list}   
    with open(os.path.join('data', 'new_taipei_city_houses.json'), 'w') as f:
        json.dump(json_format, f)