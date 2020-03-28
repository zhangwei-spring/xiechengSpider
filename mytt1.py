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
def search_url(depport, arrport, depdate):

    international_url = ('https://flights.ctrip.com/international/search/oneway-%s-%s?depdate=%s&cabin=y_s&adult=1&child=0&infant=0') % (depport, arrport, depdate)
    return international_url

async def get_request(url, server, semaphore, city_dep, city_arr, date):
    async with semaphore:
        trigger_loop = 0
        # trigger_empty = 0
        while True:
            trigger_loop = trigger_loop + 1
            if trigger_loop > 10:
                return "error", city_dep, city_arr, date
            try:
                proxy = server.create_proxy()  # 创建一个浏览器代理

                proxy.new_har(url, options={'captureContent': True, 'captureHeaders': True})
                browser = await launch(headless=True, autoClose=True, dumpio=True, ignoreHTTPSErrors=True,
                                       args=['--ignore-certificate-errors', '--no-sandbox', '--disable-gpu',
                                             '--proxy-server={0}'.format(proxy.proxy)])
                # await page.setViewport({'width': 1024, 'height': 768})
                page = await browser.newPage()
                await page.goto(url, waitUntil='networkidle0')  # 6,13,9,10
                await asyncio.sleep(5)
                await page.evaluate("""
                            () =>{
                                Object.defineProperties(navigator,{
                                    webdriver:{
                                    get: () => false
                                    }
                                })
                            }
                        """)
                result = proxy.har
                for entry in result['log']['entries']:
                    if 'batchSearch' in entry['request']['url']:
                        if 'text' not in entry['response']['content']:
                            raise Exception("ERROR: unexpected Exception! --- text")
                        text = entry['response']['content']['text']
                        text = json.loads(text)
                        searchId = text['data']['context']['searchId']
                        if searchId == "":
                            raise Exception("ERROR: searchId is null!")
                        break
                length = 0
                for entry in result['log']['entries']:
                    if searchId in entry['request']['url']:
                        length = length + 1

                for entry in result['log']['entries']:
                    if searchId in entry['request']['url']:
                        text = entry['response']['content']['text']
                        text = json.loads(text)
                        finished = text['data']['context']['finished']
                        if finished is True:
                            if not 'flightItineraryList' in text['data']:
                                # trigger_empty  =trigger_empty + 1
                                # if trigger_empty > 2:
                                #     return "empty", city_dep, city_arr, date
                                # else:
                                #     raise Exception("ERROR: finished but empty!")
                                return "empty", city_dep, city_arr, date
                            data = text['data']['flightItineraryList']
                            return data, city_dep, city_arr, date
                        length = length - 1
                        if length == 0:
                            raise Exception("ERROR: connection is not finished!")

            except Exception as e:
                print(city_dep + "--" + city_arr +" " + str(e))
            finally:
                proxy.close()
                await browser.close()


        # for entry in result['log']['entries']:
        #     if 'batchSearch' in entry['request']['url']:
        #         if 'text' not in entry['response']['content']:
        #             headers = "empty"
        #             break
        #         if  'flightItineraryList' not in entry['response']['content']['text']:
        #             headers = "empty"
        #             break
        #         else:
        #             postdata_ = entry['request']['postData']['text']
        #             header = entry['request']['headers']
        #             for x in header:
        #                 if x['name'] == 'Connection':
        #                     headers[x['name']] = 'close'
        #                 else:
        #                     headers[x['name']] = x['value']
        #                 postdata = json.loads(postdata_)
        #                 postdata = json.dumps(postdata)
        #             break
        # return headers, postdata ,city_dep, city_arr, date
        # search_URL = "https://flights.ctrip.com/international/search/api/search/batchSearch?v="
        # search_URL = "https://baidu.com"

        # async with aiohttp.ClientSession() as aio:
        #     while True:
        #         try:
        #             print('kaishi')
        #             async with await aio.post(search_URL,headers=headers, data = postdata, timeout=10) as res:
        #                 print("123")
        #                 print(await res.json(encoding='UTF-8'))
        #                 result = await (res.json())
        #                 print("res :"+result)
        #                 break
        #         except Exception as e:
        #             repr(e)


        # return data


def spider_searchflights(headers, postdata):
    search_URL = 'https://flights.ctrip.com/international/search/api/search/batchSearch?v='
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    # requests.packages.urllib3.disable_warnings()
    while True:
        try:
            response = s.post(search_URL, data=postdata, headers=headers, timeout=10)
            break
        except Exception as e:
            s.close()
            print(e)
    dict_json = json.loads(response.text)
    s.close()
    return dict_json


def getData(result, city_dep, city_arr, date):
    folder_name = "数据_" + date
    # dic = result['data']['flightItineraryList']
    list = myModels_1.ItineraryList(result)
    l = len(list.itineraryList[0].flightList)
    dcity = list.itineraryList[0].flightList[0].departureCityName
    acity = list.itineraryList[0].flightList[l - 1].arrivalCityName
    if not os.path.exists(folder_name + "/" + acity):
        os.makedirs(folder_name + "/" + acity)
    filename = folder_name + "/" + acity + "/" + dcity + "--" + acity + ".xlsx"
    # filename = folder_name + "/" + city_arr + "/" + city_dep + "--" + city_arr + ".xlsx"
    workbook = xlsxwriter.Workbook(filename)  # 创建一个Excel文件
    worksheet = workbook.add_worksheet()  # 创建一个sheet
    style = workbook.add_format({
        "fg_color": "red"  # 单元格的背景颜色
    })

    # 写入title
    worksheet.write(0, 0, "出发国家")
    worksheet.write(0, 1, "出发城市")
    worksheet.write(0, 2, "到达城市")
    worksheet.write(0, 3, "价格")
    for i in range(0, 5):
        worksheet.write(0, 4 + i * 4 + 0, "航班号" + str(i + 1))
        worksheet.write(0, 4 + i * 4 + 1, "机型" + str(i + 1))
        worksheet.write(0, 4 + i * 4 + 2, "经停地" + str(i + 1))
        worksheet.write(0, 4 + i * 4 + 3, "最大载客量" + str(i + 1))

    count = 0
    mark = False
    for r, flightList in enumerate(list.itineraryList):
        row = r + 1
        col = 0
        length = len(flightList.flightList)
        chufadi = flightList.flightList[0].departureCityName
        mudidi = flightList.flightList[length - 1].arrivalCityName
        country_de = flightList.flightList[0].departureCountryName
        price = flightList.price
        worksheet.write(row, col, country_de)
        col = col + 1
        worksheet.write(row, col, chufadi)
        col = col + 1
        worksheet.write(row, col, mudidi)
        col = col + 1
        worksheet.write(row, col, price)
        col = col + 1
        for flight in flightList.flightList:
            worksheet.write(row, col, flight.flightNo)
            col = col + 1
            worksheet.write(row, col, flight.aircraftName)
            col = col + 1
            worksheet.write(row, col, flight.arrivalCityName)
            col = col + 1
            if flight.aircraftName != '' and flight.aircraftCapacity > 0:
                worksheet.write(row, col, flight.aircraftCapacity)
            else:
                if mark == False:
                    print("red:" + city_dep + "--" + city_arr)
                mark = True
                file_log_empty = open(folder_name + "/data_log_empty.txt", "a")  # 打开记录文件
                file_log_empty.write(city_dep + "--" + city_arr + "\n")
                file_log_empty.close()
                worksheet.write(row, col, flight.aircraftCapacity, style)
            col = col + 1
        count = count + 1
    file_log = open(folder_name + "/data_log.txt", "a")  # 打开记录文件
    file_log.write(city_dep + "\t" + city_arr + "\t" + str(count) + "\n")
    file_log.close()
    print(city_dep + "--" + city_arr + " " + date + "  共" + str(count) + "条")
    workbook.close()

def callback(task):
    result, city_dep, city_arr, date = task.result()
    if not os.path.exists("数据_" + date):
        os.makedirs("数据_" + date)
    if result == 'error':
        file_log = open("数据_" + date + "/data_log_error.txt", "a")  # 打开记录文件
        file_log.write(city_dep + "\t" + city_arr + "\n")
        file_log.close()
        print(city_dep + "--" + city_arr + " " + date + "出错")
    if result == 'empty':
        file_log = open("数据_" + date + "/data_log.txt", "a")  # 打开记录文件
        file_log.write(city_dep + "\t" + city_arr + "\t" + str(0) + "\n")
        file_log.close()
        print(city_dep + "--" + city_arr + " " + date + "  共" + str(0) + "条")
    else:
        trigger = 0
        while True:
            trigger = trigger + 1
            if trigger > 5:
                file_log = open("数据_" + date + "/data_log_error.txt", "a")  # 打开记录文件
                file_log.write(city_dep + "\t" + city_arr + "\n")
                file_log.close()
                print(city_dep + "--" + city_arr + " " + date + "出错")
                break
            try:
                # result = spider_searchflights(headers, postdata)
                getData(result, city_dep, city_arr, date)
                break
            except Exception as e:
                print("写错误：", e)

def run(dep, arr, arr_date, num, china):
    server = Server(path)  # 设置服务器脚本路径
    server.start()
    tasks = []
    semaphore = asyncio.Semaphore(num)  # 限制并发量
    i = 0
    for date in arr_date:
        for departureCity in dep:
            for arrivalCity in arr:
                if departureCity != arrivalCity:
                    if departureCity not in china or arrivalCity not in china:
                        url = search_url(departureCity, arrivalCity, date)
                        print(departureCity + "--" + arrivalCity + "开始爬取数据..."+str(i))
                        i = i+1
                        while True:
                            try:
                                c = get_request(url, server, semaphore, departureCity, arrivalCity, date)
                                task = asyncio.ensure_future(c)
                                task.add_done_callback(callback)
                                tasks.append(task)
                                break
                            except Exception as e:
                                print(e)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print("server closed")
    server.stop()


if __name__ == '__main__':
    tic = time.time()
    # browsermob-proxy配置路径，请将这里填写为自己电脑上的路径
    path = 'F:/project file/pachong/携程爬虫2/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat'

    # 出发城市代码    日本韩国伊朗 美国 意大利西班牙德国法国英国瑞典
    # iran = ['thr', 'syz', 'mhd', 'ifn', 'ihr']
    # italy = ['rom', 'mil', 'vce', 'nap', 'flr']
    # france = ['par','nce','lys','mrs', 'bod']
    # japan = ['tyo','osa','spk','oka','fuk']
    # korea = ['sel','pus','cju','tae','cjj']               #
    # usa = ['was','lax','nyc','sfo','chi']
    # spain = ['mad','bcn','agp','alc','tci']
    # germany = ['ber','fra','muc','dus','ham']
    # uk = ['lon','man','edi','bhx','gla']
    # sweden = ['sto','got','mma','krn','ume']
    # d = japan + korea + iran + usa + italy + spain + germany + france + uk + sweden
    # a = japan + korea + iran + usa + italy + spain + germany + france + uk + sweden
    usa = ['lax','nyc','sea','chi']
    china = ['bjs','sha','can','ctu','szx']
    other1 = ['tyo','ber','del','par','lon','bsb','rom',
             'yow','sel','mow','cbr','mad','ist','ams']
    other2 = ['ruh','brn','sto','waw','bru','bkk','vie',
             'thr','mnl','osl','kul','dub','tlv','cph']
    other3 = ['hkg','sin','hel','scl','prg','lim','ath',
              'lis','mex','jkt','bue','tpe','abv',
              'auh','pry','cae','dag','han','wlg','bgw']
    dep = usa + china + other1 + other2 + other3
    arr = usa + china + other1 + other2 + other3
    num = 5
    # 目的地代码 上海：sha  广州：can  杭州：hgh  南京：nkg 成都：ctu 深圳：szx 天津：tsn 北京：bjs 兰州：lhw
    # 时间    #0401,0405,0408
    arr_date = ['2020-04-08']             #0318,0322,0325,0329,0401,0405,0408,0412,0415,0419,0422,0426,0429,0503,0506,0510
#usa+china+
    run(other1, arr , arr_date, num, china)

    toc = time.time()
    hours = int((toc - tic) / 60 / 60)
    minutes = int(((toc - tic) / 60) % 60)
    seconds = int(toc - tic - 60 * minutes - 60 * 60 * hours)
    print("总用时：%d时%d分%d秒" %(hours,minutes,seconds))

    #实用版本