# -*- coding: utf-8 -*-
import requests
import chardet
import json
import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

def fun1():
    
    # 关闭https证书验证警告
    # requests.packages.urllib3.disable_warnings()
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
    # 12306的城市名和城市代码js文件url
	url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
	r = requests.get(url, verify=False)
	pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
	result = re.findall(pattern, r.text)
	result1=json.dumps(result,encoding="utf-8",ensure_ascii=False)
	return result

def get_query_url(text):
	result1=fun1()
	#返回调用api的url链接
	# 解析参数 aggs[0]里是固定字符串：车票查询 用于匹配公众号接口
	args = str(text).split(' ')
	try:
		date = args[0]
		from_station_name = args[1]
		to_station_name = args[2]

		for i in result1:
			if i[0]==from_station_name:
				from_station=i[1]

		for i in result1:
			if i[0]==to_station_name:
				to_station=i[1]
	except:
		date, from_station, to_station = '--', '--', '--'
		# 将城市名转换为城市代码
	# api url 构造
	url = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)
	return url




def query_train_info(url):
	#查询火车票信息：返回 信息查询列表
	info_list = []
	try:
		r = requests.get(url, verify=False)
       # 获取返回的json数据里的data字段的result结果
		raw_trains = r.json()['data']['result']
		#raw1= json.dumps(raw_trains, encoding="utf-8", ensure_ascii=False)
		info_list = []
		for i in raw_trains:
            # 循环遍历每辆列车的信息
			data_list = i.split("|")
			# 车次号码
			train_no = data_list[3]
			#train_no=json.dumps(data_list[3], encoding="utf-8", ensure_ascii=False)
			# 出发站
			from_station_code = data_list[6]
			l2=fun1()
			for i in l2:
				if i[1]==from_station_code:
					from_station_name = i[0]
			# 终点站
			to_station_code = data_list[7]
			for i in l2:
				if i[1]==to_station_code:
					to_station_name = i[0]
			# 出发时间
			start_time = data_list[8]
			# 到达时间
			arrive_time = data_list[9]
			# 总耗时
			time_fucked_up = data_list[10]
			# 一等座
			first_class_seat = data_list[31] or '--'
			# 二等座
			second_class_seat = data_list[30] or '--'
			# 软卧
			soft_sleep = data_list[23] or '--'
			# 硬卧
			hard_sleep = data_list[28] or '--'
			# 硬座
			hard_seat = data_list[29] or '--'
			# 无座
			no_seat = data_list[26] or '--'
			# 打印查询结果
			# info = ('第{}列，车次名称:{}\n出发站:{}\n目的地:{}\n出发时间:{}\n到达时间:{}\n消耗时间:{}\n座位情况：\n 一等座：「{}」 \n二等座：「{}」\n软卧：「{}」\n硬卧：「{}」\n硬座：「{}」\n无座：「{}」\n\n'.format(
			# i,train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,
			# second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))
			# info_list.append(info)
			info = {"车次名称": train_no, "出发站": from_station_name, "终点站": to_station_name, "出发时间": start_time,
                    "到达时间": arrive_time, "总耗时": time_fucked_up, "一等座": first_class_seat, "二等座": second_class_seat,
                    "软卧": soft_sleep, "硬卧": hard_sleep, "硬座": hard_seat, "无座": no_seat}
			info_list.append(info)
		r=json.dumps(info_list).decode("unicode-escape")
		r1=json.dumps(info_list,encoding="utf-8",ensure_ascii=False)
		s= r1.replace( '\"','')
		return s
	except:
		return "N"
def mian(a, b, c):
	z = a + " " + b + " " + c
	return query_train_info(get_query_url(z))


# text="2018-05-28 广州 哈尔滨"
#s= mian('2018-06-21','广州','哈尔滨')
# print("***********")
#print(s)
# print("***********")
# print(mian(text))
