import requests
from bs4 import BeautifulSoup
import json
import time
import pandas


#单页
def game (url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit\
        /537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'lxml')

    main_html = soup.select('.file_block')[0]
    td_total = main_html.find_all('td')
    game_list = []
    for i in td_total:
        game = {}
        game['title'] = i.select('.link')[0].text
        game['link'] = i.select('.link')[0]('a')[0]['href']
        for i in i.text.split('\n'):
            if 'B' in i:
                game['size'] = i.split(' ')[0]
            if 'Uploaded' in i:
                game['uploaded'] = i.split(' ')[1]
            if 'Views:' in i:
                game['views'] = i.split(' ')[1]
            if 'Downloads' in i:
                game['downloads'] = i.split(' ')[0]
        game_list.append(game)
    return game_list

# #多页
# game_total = []
# for i in range(1, 486):
#     url = 'https://www.big4shared.com/users/Razorback?fld_id\
#     =&fld=&usr_login=Razorback&op=user_public&page={}'.format(i)
#     game_total.extend(game(url))
#     print('第{}页完成'.format(i))
#     time.sleep(1)  # 限制爬取时间
# print(len(game_total))
#
# #保存json
# with open('game_tatal.json', 'w') as f:
#     json.dump(game_total, f)

#打开
with open('game_tatal.json', 'r') as f:
    game_total = json.load(f)
    df = pandas.DataFrame(game_total)
    df.to_excel('game_total.xlsx')