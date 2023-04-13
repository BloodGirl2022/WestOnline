# 2022_12_06_ddl激战中毕 222100306_洪朗晨
# 年份，事件类型(birth、death等)，标题，简要内容

import pymysql
import time
import requests as requests
import re
#import random

# 一些很长的字符串（网址前后缀）
db='history_date_check'
last=[31,28,31,30,31,30,31,31,30,31,30,31] # 表示下标+1所对应一个月的天数
line=0

# 数据库-执行sql语句
# 输入：sql命令
# 功能：执行语句
def doSql(sql):
    cur.execute(sql)   # 执行
    conn.commit()        # 提交

# 数据库打开预备
conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',charset='utf8')
cur = conn.cursor()
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}

#==============================================
# 以下语句可创建数据库、表
sql='CREATE DATABASE '+db   # 创建数据库（方便检查）
doSql(sql)

conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',charset='utf8',db=db) # 连接数据库
cur = conn.cursor()

sql='''CREATE TABLE data(
`序号` int,
`日期` text,
`事件年份` int,
`事件类型` text,
`事件标题` text,
`简要内容` text,
`链接` text);'''
doSql(sql)

# 以上语句在自己电脑可删除
#==============================================

# 通过指定月份、日子确定url
# 输入：整型或字符串moth、day
# 输出：整理好的url
def prc_url(month_, day_):
    time_ = time.mktime(time.strptime(f"2022-{month_}-{day_} 00:00:00", "%Y-%m-%d %H:%M:%S")) * 1000
    return "https://baike.baidu.com/cms/home/eventsOnHistory/" + str(month_) + ".json?_=" + str(time_)# 拼接url，找到数据

# 功能：处理爬到的数据（存在列表里） 整理为字典
# 输入：数据列表
# 返回：处理好后的数据字典一条
def prc_infos(line,month_,day_,info):
    # 找到网页对应数据
    year = info['year']
    type = info['type']
    title = info['title']
    link = info['link']
    desc = info['desc']
    # 处理数据
    title = re.sub(r'<.*?>', '', title)
    desc = re.sub(r'<.*?>', '', desc) + '...'
    date = month_ + '-' + day_  # 自定义数据

    # 返回
    info_dict = {"序号":line,"日期":date,"事件年份": year, "事件类型": type, "事件标题": title, "链接": link, "简要内容": desc}
    return info_dict  # 将一条数据以字典返回

# 功能：将某日期对应所有信息条一起存入数据库
# 单位：某天
# 输入：信息list
# 输出：无
def ist(list):
    # 这边全用%s而不是%d是因为有bug无法解决，说只能用这个
    sql = "INSERT INTO `data` (`序号`,`日期`,`事件年份`, `事件类型`, `事件标题`, `链接`, `简要内容`) VALUES(%s,%s,%s, %s, %s, %s, %s);"
    for info in list:
        cur.execute(sql,(info["序号"],info["日期"],info["事件年份"], info["事件类型"], info["事件标题"], info["链接"], info["简要内容"]))
        conn.commit()   # 保存

# 遍历日期
for month in range(1,13):
    for day in range (1,last[month-1]+1):
        month_s = str(month).zfill(2)    # 字符串形式
        day_s = str(day).zfill(2)        # 字符串形式

        # 通过函数得到url，请求，得到数据
        url=prc_url(month_s, day_s)
        json_help = requests.get(url=url, headers=headers).json()
        json_list = json_help[str(month_s)][str(month_s) + str(day_s)]

        # 加工数据，将所有条信息存入total_data（列表）
        total_data=[]
        for info in json_list:
            line += 1  # 条数加1
            # 加工数据，并将整条信息存入列表
            total_data.append(prc_infos(int(line), month_s, day_s, info)) # append了一个字典)

        # 将信息列表导入数据库
        ist(total_data)

        # 展示
        print(month_s + "月" + day_s + "日" + "信息加载成功.")
        #print(total_data[len(json_list)-1])    # 最后一条信息如下

# 关闭
cur.close()
conn.close()