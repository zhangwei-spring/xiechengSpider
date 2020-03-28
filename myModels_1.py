class ItineraryList:
    def __init__(self, dic):
        self.itineraryList = []
        for item in dic:
            dic_flightList = item['flightSegments'][0]['flightList']
            dic_priceList = item['priceList'][0]
            flightList = FlightList(dic_flightList, dic_priceList)
            self.itineraryList.append(flightList)

    def __str__(self):
        stri = ""
        for flightList in self.itineraryList:
            stri = stri + str(flightList)
        return stri


class FlightList:
    def __init__(self, list, priceList):
        # 航班价格
        self.price = priceList['adultPrice'] + priceList['adultTax']
        self.flightList = []
        for item in list:
            flight = Flight(item)
            self.flightList.append(flight)

    def __str__(self):
        stri = ""
        for i in self.flightList:
            stri = stri + str(i) + "\n"
        return stri


class Flight:
    def __init__(self, data):
        # 航班号
        self.flightNo = data['flightNo']
        # 出发国家
        self.departureCountryName = data['departureCountryName']
        # 到达国家
        self.arrivalCountryName = data['arrivalCountryName']
        # 转机序号
        self.sequenceNo = data['sequenceNo']
        # 出发城市代号
        self.departureCityCode = data['departureCityCode']
        # 出发城市名称
        self.departureCityName = data['departureCityName']
        # 到达城市代码
        self.arrivalCityCode = data['arrivalCityCode']
        # 到达城市名称
        self.arrivalCityName = data['arrivalCityName']
        # 飞机型号
        self.aircraftCode = data['aircraftCode']
        # 起飞时间
        self.departureDateTime = data['departureDateTime']

        # 飞机名称
        self.aircraftName = ''
        #  载客量
        self.aircraftCapacity = ''
        if 'aircraftName' in data:
            self.aircraftName = data['aircraftName']
            self.aircraftCapacity = getCapacity(self.aircraftName)

    def __str__(self):
        return "flightNo:" + str(self.flightNo) + "\tsequenceNo:" + str(
            self.sequenceNo) + "\tdepartureCity:" + self.departureCityName + "\tarrivalCity:" + self.arrivalCityName + "\taircraft:" + self.aircraftName + "\taircraftCapacity:" + str(
            self.aircraftCapacity) +"\tarrivalCountryName:" + self.arrivalCountryName


def getCapacity(aircraftName):
    if aircraftName == "空客350(大)":
        return 369
    elif aircraftName == "波音737(中)":
        return 180
    elif aircraftName == "空客321(中)":
        return 180
    elif aircraftName == "空客319(中)":
        return 120
    elif aircraftName == "空客330(大)":
        return 300
    elif aircraftName == "波音777(大)":
        return 300
    elif aircraftName == "波音738(中)":
        return 162
    elif aircraftName == "波音757(中)":
        return 180
    elif aircraftName == "波音717(中)":
        return 100
    elif aircraftName == "波音787(大)":
        return 259
    elif aircraftName == "空客320(中)":
        return 160
    elif aircraftName == "巴航工190(中)":
        return 114
    elif aircraftName == "巴航工190-E2(中)":
        return 114
    elif aircraftName == "空客318(中)":
        return 107
    elif aircraftName == "庞巴迪700(小)":
        return 69
    elif aircraftName == "庞巴迪900(小)" or aircraftName == "庞巴迪(小)":
        return 90
    elif aircraftName == "庞巴迪1000(中)" or aircraftName == "庞巴迪(中)":
        return 100
    elif aircraftName == "巴航工145(小)":
        return 50
    elif aircraftName == "巴航工140(小)":
        return 44
    elif aircraftName == "巴航工175(小)":
        return 88
    elif aircraftName == "巴航工195(中)":
        return 122
    elif aircraftName == "巴航工ERJ(小)":
        return 50
    elif aircraftName == "空客220(中)":
        return 160
    elif aircraftName == "空客380(大)":
        return 500
    elif aircraftName == "波音747(大)":
        return 467
    elif aircraftName == "空客32S(中)":
        return 160
    elif aircraftName == "法宇航42(小)":
        return 42
    elif aircraftName == "法宇航72(小)":
        return 72
    elif aircraftName == "波音767(大)":
        return 280
    elif aircraftName == "巴航工170(小)":
        return 80
    elif aircraftName == "比奇1900(小)":
        return 19
    elif aircraftName == "德·哈维兰8(小)":
        return 70
    elif aircraftName == "空客340(大)":
        return 350
    elif aircraftName == "苏霍伊超100(小)":
        return 80
    elif aircraftName == "阿弗罗100(小)" or aircraftName == "阿弗罗100(小)":
        return 97
    elif aircraftName == "阿弗罗85(小)":
        return 72
    elif aircraftName == "ARJ21(小)":
        return 90
    else:
        return -1
