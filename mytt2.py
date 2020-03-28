def xiecheng(dcode, acode, date):

    city = {'阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'MFM',
            '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
            '北京': 'BJS', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
            '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
            '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
            '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
            '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
            '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
            '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
            '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
            '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
            '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU', '九寨沟': 'JZH', '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
            '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
            '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
            '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
            '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
            '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
            '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
            '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
            '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
            '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
            '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL',
            '香格里拉(迪庆)': 'DIG',
            '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY', '延吉': 'YNJ', '盐城': 'YNZ',
            '伊春': 'LDS',
            '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF', '榆林': 'UYN',
            '玉树': 'YUS',
            '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO', '中卫': 'ZHY',
            '舟山': 'HSN',
            '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}
    dcity = list(city.keys())[list(city.values()).index(dcode.upper())]
    acity = list(city.keys())[list(city.values()).index(acode.upper())]
    url_ = "https://flights.ctrip.com/itinerary/oneway/"+dcode+"-"+acode+"?date="+ date
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Content-Type": "application/json",  # 声明文本类型为 json 格式
        "referer": r"" + url_ + ""
    }

    print("开始")
    url = 'http://flights.ctrip.com/itinerary/api/12808/products'
    request_payload = {"flightWay": "Oneway",
                       "classType": "ALL",
                       "hasChild": 'false',
                       "hasBaby": 'false',
                       "searchIndex": 1,
                       "airportParams": [
                           {"dcity": city.get(dcity), "acity": city.get(acity), "dcityname": dcity, "acityname": acity,
                            "date": date}]}

    s = requests.session()
    s.keep_alive = False
    while True:
        try:
            print("fetching")
            response = s.post(url, data=json.dumps(request_payload), headers=headers, timeout=10)
            time.sleep(2)
            result = json.loads(response.text)
            routeList = result.get('data').get('routeList')
            if routeList is not None:
                break
            else:
                s.close()
                time.sleep(3)
        except Exception as e:
            print(e)
            s.close()
    s.close()
    print('写数据')
    folder_name = "数据_" + date
    if not os.path.exists(folder_name + "/" + acity):
        os.makedirs(folder_name + "/" + acity)
    filename = folder_name + "/" + acity + "/" + dcity + "--" + acity + ".xlsx"
    workbook = xlsxwriter.Workbook(filename)  # 创建一个Excel文件
    worksheet = workbook.add_worksheet()  # 创建一个sheet
    style = workbook.add_format({
        "fg_color": "red"  # 单元格的背景颜色
    })
    worksheet.write(0, 0, "出发国家")
    worksheet.write(0, 1, "出发城市")
    worksheet.write(0, 2, "到达城市")
    worksheet.write(0, 3, "航班号")
    worksheet.write(0, 4, "机型")
    worksheet.write(0, 5, "最大载客量")
    worksheet.write(0, 6, "价格")

    row = 1
    for route in routeList:
        col = 0
        if len(route.get('legs')) == 1:
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            flightNo = flight.get('flightNumber')
            aircraftNo = flight.get('craftTypeName')
            aircraftSize = flight.get('craftTypeKindDisplayName')[:1]
            aircraft = aircraftNo+"("+aircraftSize+")"
            capacity = myModels_1.getCapacity(aircraft)
            price = legs.get('characteristic').get('lowestPrice')
            worksheet.write(row, col, '中国')
            col = col + 1
            worksheet.write(row, col, dcity)
            col = col + 1
            worksheet.write(row, col, acity)
            col = col + 1
            worksheet.write(row, col, flightNo)
            col = col + 1
            worksheet.write(row, col, aircraft)
            col = col + 1
            if capacity > 0:
                worksheet.write(row, col, capacity)
            else:
                file_log_empty = open(folder_name + "/data_log_empty.txt", "a")  # 打开记录文件
                file_log_empty.write(dcity + "--" + acity + "\n")
                file_log_empty.close()
                worksheet.write(row, col, capacity, style)
            col = col + 1
            worksheet.write(row, col, price)
        row = row + 1
    workbook.close()

    print(dcity, '------->', acity, date)


import warnings
import json
import os
import time
import gevent
from gevent import monkey
import warnings
import requests
import xlsxwriter
from browsermobproxy import Server
from retry import retry
import  aiohttp
import  asyncio
import requests
import time
import pyppeteer
from pyppeteer import launch
import myModels_1
monkey.patch_all()
warnings.filterwarnings("ignore")
def search_url(dcode, acode, date):
    url = "https://flights.ctrip.com/itinerary/oneway/"+dcode+"-"+acode+"?date="+ date
    return url

@retry()
async def get_request(url, server, semaphore, city_dep, city_arr, date):
    async with semaphore:
        while True:
            try:
                proxy = server.create_proxy()  # 创建一个浏览器代理
                break
            except Exception as e:
                print("创建proxy失败...")
                print(e)
        proxy.new_har(url, options={'captureContent': True, 'captureHeaders': True})

        browser = await launch(headless=True, autoClose=True, dumpio=True, ignoreHTTPSErrors=True, timeout=10,
                               args=['--ignore-certificate-errors', '--no-sandbox', '--disable-gpu',
                                     '--proxy-server={0}'.format(proxy.proxy)])
        page = await browser.newPage()
        await page.setViewport({'width': 1024, 'height': 768})
        while True:
            try:
                await page.goto(url, waitUntil='networkidle0')  # 6,13,9,10
                asyncio.sleep(5)
                break
            except Exception as e:
                repr(e)
        await browser.close()
        result = proxy.har
        proxy.close()

        headers = {}
        postdata_ = {}
        for entry in result['log']['entries']:
            if 'products' in entry['request']['url']:
                postdata_ = entry['request']['postData']['text']
                header = entry['request']['headers']
                for x in header:
                    if x['name'] == 'Connection':
                        headers[x['name']] = 'close'
                    else:
                        headers[x['name']] = x['value']
                break
        postdata = json.loads(postdata_)
        postdata = json.dumps(postdata)
        return headers, postdata ,city_dep, city_arr, date


def spider_searchflights(headers, postdata):
    search_URL = 'http://flights.ctrip.com/itinerary/api/12808/products'
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    # requests.packages.urllib3.disable_warnings()
    while True:
        try:
            print("抓取数据")
            response = s.post(search_URL, data=postdata, headers=headers, timeout=10)
            time.sleep(3)
            break
        except Exception as e:
            s.close()
            print(e)
    dict_json = json.loads(response.text)
    s.close()
    return dict_json


def getData(result, dcity, acity, date):
    routeList = result.get('data').get('routeList')
    dep = routeList[0].get('legs')[0].get('flight').get('departureAirportInfo').get('cityName')
    arr = routeList[0].get('legs')[0].get('flight').get('arrivalAirportInfo').get('cityName')
    folder_name = "数据_" + date
    if not os.path.exists(folder_name + "/" + arr):
        os.makedirs(folder_name + "/" + arr)
    filename = folder_name + "/" + arr + "/" + dep + "--" + arr + ".xlsx"
    workbook = xlsxwriter.Workbook(filename)  # 创建一个Excel文件
    worksheet = workbook.add_worksheet()  # 创建一个sheet
    style = workbook.add_format({
        "fg_color": "red"  # 单元格的背景颜色
    })
    worksheet.write(0, 0, "出发国家")
    worksheet.write(0, 1, "出发城市")
    worksheet.write(0, 2, "到达城市")
    worksheet.write(0, 3, "航班号")
    worksheet.write(0, 4, "机型")
    worksheet.write(0, 5, "最大载客量")
    worksheet.write(0, 6, "价格")

    row = 1
    for route in routeList:
        col = 0
        if len(route.get('legs')) == 1:
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            flightNo = flight.get('flightNumber')
            aircraftNo = flight.get('craftTypeName')
            aircraftSize = flight.get('craftTypeKindDisplayName')[:1]
            aircraft = aircraftNo + "(" + aircraftSize + ")"
            capacity = myModels_1.getCapacity(aircraft)
            price = legs.get('characteristic').get('lowestPrice')
            worksheet.write(row, col, '中国')
            col = col + 1
            worksheet.write(row, col, dep)
            col = col + 1
            worksheet.write(row, col, arr)
            col = col + 1
            worksheet.write(row, col, flightNo)
            col = col + 1
            worksheet.write(row, col, aircraft)
            col = col + 1
            if capacity > 0:
                worksheet.write(row, col, capacity)
            else:
                file_log_empty = open(folder_name + "/data_log_empty.txt", "a")  # 打开记录文件
                file_log_empty.write(dep + "--" + arr + "\n")
                file_log_empty.close()
                worksheet.write(row, col, capacity, style)
            col = col + 1
            worksheet.write(row, col, price)
        row = row + 1
    workbook.close()

    print(dep, '------->', arr, date)

def callback(task):
    headers, postdata, city_dep, city_arr, date = task.result()
    while True:
        try:
            result = spider_searchflights(headers, postdata)
            print('写数据')
            getData(result, city_dep, city_arr, date)
            break
        except Exception as e:
            repr(e)



def run(departureCity, arrivalCity, date, num):
    server = Server(path)  # 设置服务器脚本路径
    server.start()
    tasks = []
    semaphore = asyncio.Semaphore(num)  # 限制并发量

    url = search_url(departureCity, arrivalCity, date)
    print(departureCity + "--" + arrivalCity + "开始爬取数据...")
    c = get_request(url, server, semaphore, departureCity, arrivalCity, date)
    task = asyncio.ensure_future(c)
    task.add_done_callback(callback)
    tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print("server closed")
    server.stop()


if __name__ == '__main__':
    tic = time.time()
    # browsermob-proxy配置路径，请将这里填写为自己电脑上的路径
    path = 'F:/project file/pachong/携程爬虫2/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat'

    # 出发城市代码    日本韩国伊朗 美国 意大利西班牙德国法国英国瑞典
    iran = ['thr', 'syz', 'mhd', 'ifn', 'ihr']
    # italy = ['rom', 'mil', 'vce', 'nap', 'flr']
    # france = ['par','nce','lys','mrs', 'bod']
    japan = ['tyo','osa','spk','oka','fuk']
    # korea = ['sel','pus','cju','tae','cjj']               #
    # usa = ['was','lax','nyc','sfo','chi']
    # spain = ['mad','bcn','agp','alc','tci']
    # germany = ['ber','fra','muc','dus','ham']
    uk = ['lon','man','edi','bhx','gla']
    # sweden = ['sto','got','mma','krn','ume']
    # d = japan + korea + iran + usa + italy + spain + germany + france + uk + sweden
    # a = japan + korea + iran + usa + italy + spain + germany + france + uk + sweden
    usa = ['lax','nyc','sea','chi']#
    china = ['bjs','sha','can','ctu','szx']
    other = ['tyo','ber','del','par','lon','bsb','rom',
             'yow','sel','mow','cbr','mad','ist','ams',
             'ruh','brn','sto','waw','bru','bkk','vie',
             'thr','mnl','osl','kul','dub','tlv','cph',
             'hkg','sin','hel','scl','prg','lim','ath','lis']

    dep = usa + china + other
    arr = usa + china + other
    num = 1
    # 目的地代码 上海：sha  广州：can  杭州：hgh  南京：nkg 成都：ctu 深圳：szx 天津：tsn 北京：bjs 兰州：lhw
    # 时间    #
    arr_date = ['2020-03-25']             #0318,0322,0325,0329,0401,0405,0408,0412,0415,0419,0422,0426,0429,0503,0506,0510
    # 记录文件
    for date in arr_date:
        for departureCity in china:
            for arrivalCity in china:
                if departureCity != arrivalCity:
                    run(departureCity, arrivalCity, date, num)

    toc = time.time()
    hours = int((toc - tic) / 60 / 60)
    minutes = int(((toc - tic) / 60) % 60)
    seconds = int(toc - tic - 60 * minutes - 60 * 60 * hours)
    print("总用时：%d时%d分%d秒" %(hours,minutes,seconds))