import os
import requests

os.chdir('update')
PikGK = ['rustaveli', 'kolskaya8', 'bo2', 'amur', '2ngt', 'kron9', 'kvb51', 'kron14', 'mtvpark', 'volp', 'mpark',
         'apavlova', 'ba85', 'port', 'gp', 'kk15', 'ilmen', 'bpark']
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36'
      }
for i in PikGK:
    url = 'https://www.pik.ru/search/' + i +\
          '/three-room?status=free&areaFrom=72&floorFrom=10&areaKitchenFrom=12&sortBy=price&currentBenefit=\
          semejnaya-1-99&flatsOnly=1'
    r = requests.get(url, headers=headers)
    with open(i+'_1-99.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)
    url = 'https://www.pik.ru/search/' + i +\
          '/three-room?status=free&areaFrom=72&floorFrom=10&areaKitchenFrom=12&sortBy=price&flatsOnly=1'
    r = requests.get(url, headers=headers)
    with open(i + '_cash.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)
