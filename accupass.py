import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
import requests
import time
import json
import pandas as pd

def scrap_accupass():

    '''
    Part 1 用selenium在搜尋頁面中動態往下拉到最底，再爬取資訊
    '''
    option = webdriver.ChromeOptions()
    option.add_argument("--no-sandbox")
    option.add_argument("--headless")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--disable-gpu")
    option.add_argument("--window-size=1920,1080")
    # option.add_experimental_option('excludeSwitches', ['enable-automation']) # 開發者模式。可以避開某些防爬機制，有開有保佑
    driver = webdriver.Chrome(options=option)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    url = 'https://www.accupass.com/search?c=music&q=演唱會&s=relevance'
    driver.get(url)
    driver.implicitly_wait(10) # 等待伺服器反應最多 10 秒，如果在時間到之前反應就提早結束等待

    # 捲動到底三次
    for i in range(3):
        driver.find_element('css selector', 'html').send_keys(Keys.END)
        time.sleep(3)

    # 找活動時間（使用者看的格式），並儲存至串列
    event_user_time = []

    event_div = driver.find_elements('css selector','#content > div > div.SearchPage-d3ff7972-container > main > section > div > div')
    for div in event_div:
        # 確保非空值
        if len(div.text.split('\n')) >=2:
            # 將日期.換成/顯示
            event_user_time.append(div.text.split('\n')[0].replace('.', '/'))

    # 找活動網址、活動ID並儲存至串列
    event_link = []
    event_id = []
    event_len = len(event_user_time)
    for i in range(1,event_len+1):
        # 活動網頁
        event_url = driver.find_element('css selector',f'#content > div > div.SearchPage-d3ff7972-container > main > section > div > div:nth-child({i}) > div > div > div > div > a')
        event_link.append(event_url.get_attribute('href'))
        # 活動ID（用來放在api link中）
        link = event_url.get_attribute('href')
        link_id = link.split('event/')[1].split('?')[0]
        event_id.append(link_id)

    driver.quit()

    '''
    Part 2 取到活動ID之後用requests,json進api爬取資訊
    '''
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

    # 用accupass本身的api取活動名稱、圖片網址、地址、表演者、展演空間、系統顯示時間
    event_name = []
    img_link = []
    address = []
    artists = []
    venue = []
    start_time = []
    end_time = []
    for ID in event_id:
        # print(ID)
        url = f"https://api.accupass.com/v3/events/{ID}"
        response = requests.get(url, headers=header)
        response.encoding = 'UTF-8' # 指定編碼方式，utf-8、UTF-8、UTF8、utf8 都一樣

        data = json.loads(response.text)
        event_name.append(data['title'])
        img_link.append(data['image200'])
        address.append(data['address'])
        venue.append(data['addressRemark'])
        start_time.append(data['eventTimeObj']['startDateTime'])
        end_time.append(data['eventTimeObj']['endDateTime'])

        guests_len = len(data['guests'])
        guests_per_event = []
        for i in range(guests_len):
            guests_per_event.append(data['guests'][i]['name'])
        # 若演出者為空值，則預設加入此字串
        if guests_per_event == []:
            artists.append('請參考活動網頁')
        elif guests_per_event != []:
            guests_per_event = '、'.join(guests_per_event)
            artists.append(guests_per_event)


    accupass_df = pd.DataFrame(list(zip(event_name,event_user_time,venue,address,artists,img_link,event_link,start_time,end_time)), columns = ['Name', 'Time', 'Venue', 'Address', 'Artists', 'ImageURL', 'PageURL', 'StartTime', 'EndTime'])
    # print(accupass_df)

    # 篩選活動名稱
    filter_name = ['演唱會','音樂會','音樂之夜','巡迴','獨奏會','演出','派對']

    # "|" means OR in pandas
    filter_df = accupass_df.query(f'Name.str.contains("|".join({filter_name}))', engine = 'python')

    return filter_df