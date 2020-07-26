# 极客大学第一周问题1
# 安装并使用 requests、bs4 库，爬取猫眼电影（）的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
# https://maoyan.com/films?showType=3


import requests
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'

header = {}
cookie = {}

# 猫眼会校验cookie，所以f12可以看到uuid

header['user-agent'] = user_agent
cookie['uuid'] = '2284CDE0CDCD11EAAE7D95D379FC6A67FFFABC48469A4C8DBFE56AB64A0A7EE0'

url = 'https://maoyan.com/films?showType=3'

mylist = []

def get_movie_top10(myurl):
    response = requests.get(myurl, headers=header, cookies=cookie)

    print(f'Status code: {response.status_code}')

    bs_info = bs(response.text, 'html.parser')

    for tags in bs_info.find_all('div', attrs={'class': 'movie-item'}, limit=10):
        print('------------------------------')
        titleTag = tags.find_next('div', attrs={'class': 'movie-hover-title'})
        title = titleTag.find('span', attrs={'class': 'name'}).get_text()
        print(f'电影名称: {title}')

        categoryTag = titleTag.find_next_sibling('div')
        category = categoryTag.contents[2].strip()
        print(f'电影类型: {category}')

        releaseTag = categoryTag.find_next_sibling('div').find_next_sibling('div')
        release = releaseTag.contents[2].strip()
        print(f'上映时间: {release}')

        mylist.append([title, category, release])

get_movie_top10(url)



# 写到csv里
import pandas as pd
import os 
movie = pd.DataFrame(data = mylist)
dir_path = os.path.dirname(os.path.realpath(__file__))

movie.to_csv(f'{dir_path}/my.csv', encoding='utf8', index=False, header=['title', 'category', 'release'])