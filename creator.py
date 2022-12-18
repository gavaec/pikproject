import json
import os
import time


def getnumbers(numstring):
    res = ''
    my_is_float = False
    for c in numstring:
        if c.isdigit() and c != '²':
            res += c
        elif c == ",":
            res += "."
            my_is_float = True
    if my_is_float:
        res = float(res)
    else:
        res = int(res)
    return res


def getprice199(filename_199, compare_id, frame199, item199, price199):
    from bs4 import BeautifulSoup
    with open(filename_199, 'r', encoding='utf-8') as input_file:
        text_199 = input_file.read()
        soup_199 = BeautifulSoup(text_199, "lxml")
        flat_list_199 = flat_list_199 = soup_199.find('div', {'class': frame199})
        items_199 = flat_list_199.find_all('a', {'class': [item199]})
        for item_199 in items_199:
            tmp_id199 = int(item_199.get('data-id'))
            if tmp_id199 == compare_id:
                tmp_a = item_199.find('div', {'class': price199}).find('span').text
                tmp_a = getnumbers(tmp_a)
                return tmp_a


def myfunc(filename, flats):
    from bs4 import BeautifulSoup
    filename_cash = filename + '_cash.html'
    cr_time = os.path.getmtime(filename_cash)
    cr_time = time.localtime(cr_time)
    cr_time = time.strftime("%Y%m%d", cr_time)
    with open(filename_cash, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
    soup = BeautifulSoup(text, "lxml")
    fl_frame = 'styles__BlockBulks-sc-prgbmx-2 kbJguq'  # вся таблица квартир
    fl_item = 'sc-lgsldV koVTrg'  # класс квартиры: берет id и url
    fl_plan = 'sc-hfLElm kohHQf'  # класс схемы плана: img url
    fl_sqr = 'sc-lmrgJh hsQRBi'  # класс комнатности и площади: текст
    fl_sect = 'sc-eXsVQl flYVjW'  # класс харакеристик секции, брать на уровень выше: текст
    fl_datefin = 'sc-hAnkBK givBns'  # класс даты окончания, брать на уровень выше: текст
    fl_cond = 'sc-hAnkBK givBns'  # класс отделки, брать на уровень выше: текст
    fl_price = 'sc-kQZOhr dVrreD'  # класс цены, брать на уровень выше: текст
    fl_noresult = 'styles__NoResults-sc-1m93mro-5 bpcnXl' # класс нет данных, брать уровень где NoResults: текст

    if text.find(fl_noresult) == -1:
        flat_list = flat_list = soup.find('div', {'class': fl_frame})
        items = flat_list.find_all('a', {'class': [fl_item]})
        for item in items:
            flat_exist = False
            tmp_id = int(item.get('data-id'))
            for i in flats:
                if i["id"] == tmp_id:
                    flat_exist = True
                    i["status"] = "free"
                    # сравниваем цены
                    tmp = item.find('div', {'class': fl_price}).find('span').text
                    tmp_cash = getnumbers(tmp)
                    if tmp_cash != i["prices"][-1]["cash"]:
                        tmp = getprice199(filename + '_1-99.html', tmp_id, fl_frame, fl_item, fl_price)
                        new_prices = {"date_file": cr_time, "cash": tmp_cash, "1.99": tmp}
                        i["prices"].append(new_prices)
            if not flat_exist:
                # если квартиры нет, то добавим ее
                flat = {"id": tmp_id, "gk": filename, "status": "free",
                        "sqr": getnumbers(item.find('div', {'class': fl_sqr}).find('p').text), "korpus": "",
                        "section": "", "floor": 0, "date_fin": "",
                        "cond": item.find('div', {'class': fl_cond}).find('span').text, "prices": [],
                        "url": 'https://www.pik.ru' + item.get('href'),
                        "plan": item.find('div', {'class': fl_plan}).find('img').get('src')}
                tmp = item.find('div', {'class': fl_sect}).find('span').text
                tmp = tmp.split(' · ')
                tmp1 = tmp[0].split()
                flat["korpus"] = tmp1[1]
                tmp1 = tmp[1].split()
                flat["section"] = tmp1[1]
                tmp1 = tmp[2].split()
                flat["floor"] = int(tmp1[1])
                tmp = item.find('div', {'class': fl_datefin}).find('span').text
                flat["date_fin"] = tmp.replace("Заселение до ", "")
                new_prices = {"date_file": cr_time,
                              "cash": getnumbers(item.find('div', {'class': fl_price}).find('span').text),
                              "1.99": getprice199(filename + '_1-99.html', tmp_id, fl_frame, fl_item, fl_price)}
                flat["prices"].append(new_prices)
                flats.append(flat)
        return


myDataFile = 'data_file.json'
os.system('copy data_file.json data_file_bckup.json')
with open(myDataFile, "r") as read_file:
    flats = json.load(read_file)
    read_file.close()
for i in flats:
    i["status"] = "sold"
os.chdir('update')
PikGK = ['rustaveli', 'kolskaya8', 'bo2', 'amur', '2ngt', 'kron9', 'kvb51', 'kron14', 'mtvpark', 'volp', 'mpark',
         'apavlova', 'ba85', 'port', 'gp', 'kk15', 'ilmen', 'bpark']
for k in PikGK:
    myfunc(k, flats)
with open(myDataFile, "w", encoding='utf-8') as write_file:
    json.dump(flats, write_file, indent=4, separators=(',', ':'))
    write_file.close()
