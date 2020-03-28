# coding:utf-8
import json
import os
import time
import traceback
import warnings

import requests
import xlsxwriter
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from  selenium.webdriver.firefox.options import Options as firefoxOptions
from win32api import RGB
import asyncio

import myModels_1

warnings.filterwarnings("ignore")
def search_url(depport, arrport, depdate):
    """
    获取携程国际机票搜索的url
    参数：
        depport：出发机场码（机场码可参考（https://github.com/wzyblowfire/flightsmonitor）
                            data文件夹下的world-airports.csv或
                            访问http://ourairports.com/airports.html下载）
        arrport: 到达机场码
        depdate: 出发日期
    返回值：
        international_url：国际航班搜索url
    """
    international_url = ('https://flights.ctrip.com/international/search/oneway-%s-%s?' + \
                         'depdate=%s&cabin=y_s&adult=1&child=0&infant=0') % (depport, arrport, depdate)
    return international_url


def get_initinfo(url, proxy, sleep_time):
    def isElementPresent(driver, value):
        try:
            element = driver.find_element_by_class_name(value)
        # 原文是except NoSuchElementException, e:
        except Exception as e:
            # 打印异常信息
            print(e)
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        # 没有发生异常，表示在页面中找到了该元素，返回True
        return True
    """
    本函数用于获取签名sign信息,transactionID和后续请求data.
    其中使用了selenium和browsermob-proxy.
    参数：
        url: 携程搜索国际航班的url
    返回值：
        headers：后续请求头信息
        postdata: 后续持续获取航班信息请求头中的提交json信息
    """

    # chrome测试配置
    # options = Options()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    # options.add_argument('--disable-gpu')
    # options.add_argument('window-size=1200x600')
    # # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)  # 使用selenium创建浏览器窗口

    # firefox测试配置
    options_ = firefoxOptions()
    options_.add_argument('--ignore-certificate-errors')
    options_.add_argument('--proxy-server={0}'.format(proxy.proxy))
    options_.add_argument('--disable-gpu')
    # options_.add_argument('--headless')
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    # profile.set_preference('permissions.default.image',2)
    driver = webdriver.Firefox(options=options_,firefox_profile= profile)
    proxy.new_har(url, options={'captureContent': True, 'captureHeaders': True})  # 代理服务器开始监测，捕捉文本和请求头信息
    # 显示等待5秒，因为网页会持续加载，需要等待一段时间，直到航空公司内容出现，说明加载成功
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        driver.quit()
        return "timeout",''
    time.sleep(5)
    try:
        WebDriverWait(driver, sleep_time, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'airline-name')))  #airline-name
    except Exception as e:
        if isElementPresent(driver, 'no-result'):
            return "empty", ''
        else:
            print(e)
            return "error_timeout",''
    finally:
        driver.quit()
    result = proxy.har

    # 获取https://flights.ctrip.com/international/search/api/search/batchSearch这个访问过程中的重要信息
    headers = {}
    for entry in result['log']['entries']:
        if 'batchSearch' in entry['request']['url']:
            postdata = entry['request']['postData']['text']
            header = entry['request']['headers']
            # response = entry['response']['content']['text']
            # response_ = json.loads(response)['data']
            # if 'flightItineraryList' in response_:
            #     result = response_['flightItineraryList']
            # else:
            #     result = "empty"
            for x in header:
                if x['name'] == 'Connection':
                    headers[x['name']] = 'close'
                else:
                    headers[x['name']] = x['value']
            # return result
            return headers,postdata
    return "error",''



def spider_searchflights(headers, post_data):
    """
    后续持续获取数据函数
    参数：
        headers：请求头信息
        post_data: 请求头中的数据信息（json）
    返回：
        dict_json: 航班信息（字典）
    """

    search_URL = 'https://flights.ctrip.com/international/search/api/search/batchSearch?v='
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    # requests.packages.urllib3.disable_warnings()
    headers["Connection"] = "close"
    try:
        response = s.post(search_URL, data=post_data, headers=headers, timeout=10)
    except Exception as e:
        s.close()
        print(e)
        time.sleep(3)

    dict_json = json.loads(response.text)

    # 如果请求不成功，输出信息
    if dict_json['status'] != 0:
        print(dict_json['msg'])

    s.close()


    return dict_json


def getData(headers,postdata,date):
    postdata = json.loads(postdata)
    postdata = json.dumps(postdata)
    print("开始爬取数据...")
    result = spider_searchflights(headers, postdata)
    if 'flightItineraryList' not in result['data']:
        print("数据为空...")
        return;
    dic = result['data']['flightItineraryList']
    list = myModels_1.ItineraryList(dic)
    # list.itineraryList下有多个航班Flightlist(myModels)，每个航班下有多个航程Flight(myModels)
    l = len(list.itineraryList[0].flightList)
    city_de = list.itineraryList[0].flightList[0].departureCityName
    city_arr = list.itineraryList[0].flightList[l - 1].arrivalCityName
    folder_name = "数据_"+date
    if not os.path.exists(folder_name + "/" + city_arr):
        os.makedirs(folder_name + "/" + city_arr)
    filename = folder_name + "/" + city_arr + "/" + city_de + "--" + city_arr + ".xlsx"
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
                print("red:" + city_de + "--" + city_arr)
                file_log_empty = open(folder_name + "/data_log_empty.txt", "a")  # 打开记录文件
                file_log_empty.write(city_de + "--" + city_arr + "\n")
                file_log_empty.close()
                worksheet.write(row, col, flight.aircraftCapacity, style)
            col = col + 1
        count = count + 1
    file_log = open(folder_name + "/data_log.txt", "a")  # 打开记录文件
    file_log.write(city_de + "\t" + city_arr + "\t"+str(count)+"\n")
    file_log.close()
    print(date + " >>> 共"+str(count)+"条")
    workbook.close()

def run(departureCity, arrivalCity, date, proxy):
    sleep_time = 5
    url = search_url(departureCity, arrivalCity, date)
    while True:
        print("开始分析头部...")
        headers,postdata = get_initinfo(url, proxy, sleep_time)
        if headers == "empty":
            print(departureCity + "--" + arrivalCity + "为空!!")
            file_log = open("数据_"+ date + "/data_log.txt", "a")  # 打开记录文件
            file_log.write(departureCity + "\t" + arrivalCity + "\t" + str(0) + "\n")
            file_log.close()
            print(date + " >>> 共" + str(0) + "条")
            print("------------------------------------------------")
            break
        elif headers == "error":
            print(departureCity + "--" + arrivalCity + "出错，重试中...")
            # time.sleep(3)
        elif headers == "error_timeout":
            sleep_time = sleep_time + 3
            if sleep_time > 15:
                print("跳过...")
                file_log_empty = open("数据_"+ date + "/data_log_error.txt", "a")  # 打开记录文件
                file_log_empty.write(departureCity + "--" + arrivalCity + "\terror\n")
                file_log_empty.close()
                break
            print(departureCity + "--" + arrivalCity + "出错，重试中...")
            # time.sleep(3)
        elif headers == "timeout":
            print(departureCity + "--" + arrivalCity + "超时，重试中...")
            # time.sleep(3)
        else:
            try:
                getData(headers,postdata,date)
                print(departureCity + "成功.")
                print("------------------------------------------------")
                break
            except Exception as e:
                print(e)
                print("出错，重试中...")
                # time.sleep(3)



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
    other = ['tyo','ber','del','par','lon','bsb','rom',
             'yow','sel','mow','cbr','mad','ist','ams',
             'ruh','brn','sto','waw','bru','bkk','vie',
             'thr','mnl','osl','kul','dub','tlv','cph',
             'hkg','sin','hel','scl','prg','lim','ath','lis']

    dep = china + other
    arr = usa + china + other
    # 目的地代码 上海：sha  广州：can  杭州：hgh  南京：nkg 成都：ctu 深圳：szx 天津：tsn 北京：bjs 兰州：lhw
    # 时间    #
    arr_date = ['2020-03-25']             #0318,0322,0325,0329,0401,0405,0408,0412,0415,0419,0422,0426,0429,0503,0506,0510
    # 记录文件
    file_log = 'data_log.txt'
    server = Server(path)  # 设置服务器脚本路径
    server.start()
    while True:
        try:
            proxy = server.create_proxy()  # 创建一个浏览器代理
            break
        except Exception as e:
            print("创建proxy失败...")
            print(e)
    for date in arr_date:
        for departureCity in dep:
            for arrivalCity in arr:
                if not (departureCity in china and arrivalCity in china):
                    if arrivalCity != departureCity:
                        print(departureCity + "--" + arrivalCity)
                        # run(departureCity, arrivalCity, date, proxy)
    proxy.close()
    server.stop()
    toc = time.time()
    hours = int((toc - tic) / 60 / 60)
    minutes = int(((toc - tic) / 60) % 60)
    seconds = int(toc - tic - 60 * minutes - 60 * 60 * hours)
    print("总用时：%d时%d分%d秒" %(hours,minutes,seconds))
