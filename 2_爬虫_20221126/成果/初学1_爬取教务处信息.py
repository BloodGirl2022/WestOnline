# 2022_12_06_2:44毕 222100306_洪朗晨
import time     # 美化输出，每爬取一页暂停
import random
import requests # 第三方模块，可发送请求
import re
import pymysql
import sqlite3  # 内置模块
import csv
#from beautifulsoup4 import Beautifulsoup
#from lxml import etree
from urllib.request import urlopen

'''
前提:
（1）此程序要在联网的情况下正常运行，否则报错
（2）为方便检查，此程序可运行一次。
实际上可以注释掉第164~204行代码，在自己已经创建的数据库基础上运行

使用说明：
(1)手动修改约142行遍历时的170（将其改为0）
即可获得所有通知
(2)总页数是自己看出来的...175页，不是获取的
(3)运行后会生成一个csv文件，and会把数据存到数据库

盲区：
不会把附件追加到同一行末

备注：
此处没有用到教程中的Jason网站
网址：jason.cn
功能：将复杂的嵌套的字典结构解析为客观的层状结构，便于观察
'''

# 预备知识
'''
1. 打开网页
（1）F12 检查
（2）Network：拦截所有请求
*  请求    响应  
* 浏览器   服务器
（3）ctr+R    刷新
* Name中有很多信息（文字、图片...）都是请求
（4）在Search下方的 Aa .* 旁“搜索”图标中搜索自己想要的内容
（5）在Response下的闪动的那一行就会给你搜索的内容的信息（在哪一行）
<a href="info/1036/12441.htm" target="_blank" title="关于部分教室改造的调课通知">关于部分教室改造的调课通知</a>
在这里面确认一下，是否有自己搜索的信息
（6）Headers
* 每发送一个请求都有对应的一个网址
* Request URL 请求网址：https://jwch.fzu.edu.cn/jxtz.htm
* Request Method 请求方式
* Status Code 请求状态
* Remote Adress 域名
*********************************************
Request URL: https://jwch.fzu.edu.cn/jxtz.htm
Request Method: GET
Status Code: 304 
Remote Address: 59.77.227.11:443
Referrer Policy: strict-origin-when-cross-origin
************************************************
（7）请求响应中使用什么编码之类的信息
* Request Headers   重点
    ** accept
    ** cookie
* Response Headers

================================================
2.爬虫——（通过代码）模拟请求（浏览器访问服务器）
（1）发送请求 https://jwch.fzu.edu.cn/jxtz.htm
（2）获取数据
（3）解析数据 <a href="info/1036/12441.htm" target="_blank" title="关于部分教室改造的调课通知">关于部分教室改造的调课通知</a>
（4）保存数据
================================================
'''

# 一些很长的网址前后缀
fro= "https://jwch.fzu.edu.cn/"
ap_link_fro= "https://jwch.fzu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner="
ap_link_mid= '&wbfileid='
ap_ad_fro= "https://jwch.fzu.edu.cn/system/resource/code/news/click/clicktimes.jsp?wbnewsid="
ap_ad_mid= '&owner='
aps_ad_but= '&type=wbnewsfile&randomid=nattach'
db='jwc_infos'
table1='infos'  # 表1的名字
table2='apd_infos'
ist='INSERT INTO'  # sql语句-插入
vl='VALUES'        # sql语句-插入的值

# 计数
line = 0    # 通知条数
page = 0
apd=0

# 页结束标志
def cover_but():
    print("   * * * *   ")
    print("*           *")
    print(" 第" + str(page) + "页加载成功")
    print("*           *")
    print("   * * * *   ")

# 数据库-执行sql语句
# 输入：sql命令
# 功能：执行语句
def doSql(sql):
    #sql='''CREATE TABLE infos(`时间` TEXT,`详情链接` TEXT,`通知单位` TEXT,`标题` TEXT);''' # 表已经创建好了
    #print(sql)         # test
    cur.execute(sql)   # 执行
    connect.commit()        # 提交

# 输入：需要拼接的参数
# 功能：拼接出sql语句
# 输出：返回sql语句字符串
def prc_sql(table,list):
    str_list=str(list).replace('[','(').replace(']',')')
    #print(str_list)
    sql=ist+' '+table+' '+vl+str_list
    print(sql)
    return sql

# 输入：网址addr，匹配格式字符串match
# 输出：返回响应txt
def retxt(addr, match):
    resp = requests.get(url=addr, headers=headers)
    resp.encoding = 'utf-8'
    html_data = resp.text
    rsl = re.findall(match, html_data, re.S)
    # 验证
    #print("=====================")
    #print(type(rsl))
    #print("返回数量为：" + str(len(rsl)))
    # ======验证：查看子网页响应=========
    # print(html_data)
    # print(len(ap))
    return rsl

# 正片
'''
# 0.伪装：复制以下信息
* cookie：用户信息
* user-agent：浏览器基本信息
* referer：防盗
'''
headers={
    'cookie': 'ElvisLives-47873=BCOHENDLFAAA; _ga=GA1.3.263781604.1633882276; JSESSIONID=743B10D7FC324F55B64964A3C11DFA75', # 翻页都变了
    'referer': 'https://jwch.fzu.edu.cn/jxtz/174.htm',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'   # 翻页都变了
}

'''准备工作'''
# csv文件写表头
with open("教务处通知.csv", mode='w', encoding='utf-8-sig', newline='') as f:
    csv.writer(f).writerow(["序号","时间", "详情链接", "通知单位", "标题","附件数/附件名","附件详情","下载次数"])
# 'jwc_infos'数据库创建表'infos'

# 数据库打开预备
connect=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        #db=db_check,
        charset='utf8'
    )
cur = connect.cursor() #  加一句应该没问题吧

# ====================================
# 以下语句在自己电脑可删除
# 创建新数据库
cur = connect.cursor()
sql='CREATE DATABASE '+db   # 创建数据库（方便检查）
doSql(sql)

# 数据库打开预备
connect=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        db=db,
        charset='utf8'
    )
cur = connect.cursor()

# 创建新表1
sql='''
CREATE TABLE infos
(
`序号` INT,
`日期` text,
`通知单位` text,
`详情链接` text,
`标题` text,
`附件数量` int);'''
doSql(sql)

# 创建新表2
sql='''
CREATE TABLE apd_infos
(
`序号` INT NOT NULL COMMENT '主键',
`标题` text,
`下载链接` text,
`下载次数` text,
`来自通知` text,
`通知序号` int);'''
doSql(sql)
# 以上语句在自己电脑可删除
# ====================================

# 初始网址
url= fro + "/jxtz.htm"
'''（一）翻页'''
for i in range (175,170,-1):
    print("============")
    page += 1   # 页数

    # 1.发送请求
    # Request Method: GET  所以request后为get
    resp=requests.get(url=url,headers=headers)
    resp.encoding='utf-8'

    # 2.获取数据
    # 和response里的数据一样
    # <Response [200]> 请求成功
    html_data=resp.text
    # print(html_data)

    # 3.解析数据
    # print html_data后在结果中 ctr+F 弹出搜索框
    # 使用工具：正则re（impoert re）
    # 搜索框中，点亮右边.*按钮：
    # 解释：A后输入(.*)再输入B，会将：A后所有语句全部匹配直到B
    # ===============================================
    # 命令：re.findall('A(.*))B','被搜索字符串')
    # (.*)B匹配到此行最后一个符合的B结束
    # (.*?)B则匹配到第一个符合的B就结束
    # 结果：即可得到所有符合A(.*)B的 (.*) 中所有内容
    # 存储：匹配内容存储在列表中(不论数量书否大于1)
    # 多个(.*)则以元组的形式存储
    # ===============================================
    # 这条语句非常慢
    # 功能：提取所有数据信息，用[列表（元组）]的形式存储
    # 要求：提取通知信息中的“通知人”（1）、标题（3）、日期（0）(少了2开头)、详情链接（2）
    # 命令：re.S 表示可跨行匹配（默认不跨行匹配）
    # 存储：多行匹配返回的也是列表
    all=re.findall('<li>.*?<span class="d.*?2(.*?)<.*?【(.*?)】.*?"(.*?)".*?e="(.*?)"',html_data, re.S)# <class 'list'>

    '''（二）每条'''
    for j in all:   # i是一个元组，而不是下标123，所以不能打印all[i],all[i][0]这样的
        line += 1  # 总条数

        # 4.处理数据、保存数据
        # all[0][0]='21' 不能直接修改#TypeError: 'tuple' object does not support item assignmentx
        date= "2" + j[0].replace("\n         ", "")
        informer=(j[1])
        addr=(fro + j[2])
        title=(j[3])

        # 5.查找附件
        # 打开网页，查看是否有附件；有则保存信息
        match='owner=(.*?)&.*?fileid=(.*?)".*?>(.*?)<'
        ap=retxt(addr,match)
        l_ap=len(ap)

        # 将信息存入一个列表
        list_info=[]
        list_info.append(line)
        list_info.append(date)
        list_info.append(informer)
        list_info.append(addr)
        list_info.append(title)
        list_info.append(l_ap)

        # 6.保存数据（到csv）
        # 直接copy教程的我也看不懂
        # time,informer,addr,title
        with open("教务处通知.csv", mode='a', encoding='utf-8-sig', newline='') as f:
            csv.writer(f).writerow([list_info])  # 通知信息和附件数量的保存

        # 7.存到数据库
        doSql(prc_sql(table1,list_info))

        # 8.处理附件信息
        if(l_ap!=0):  # 有附件
            '''（三）附件'''
            for k in range(0,len(ap)): # 如果有附件
                apd +=1  # 总附件数
                # ap[k][0]owner;ap[k][1]wbfield;ap[k][2]名称
                # 关键信息放置
                owner=ap[k][0]
                wbfield=ap[k][1]
                # 处理数据
                ap_link= ap_link_fro + owner + ap_link_mid + wbfield   # 附件下载地址
                ap_title=ap[k][2]    # 附件名称
                ap_ad=ap_ad_fro+wbfield+ap_ad_mid+owner+aps_ad_but

                '''（四）下载次数'''
                match='times":(.*?),'
                times=retxt(ap_ad, match) # 返回一个列表，只有下载次数一个元素
                #print("下载次数返回的类型为"+str(type(times)))
                ap_click=times[0]

                # 信息存到一个列表
                list_apdInf=[]
                list_apdInf.append(apd)
                list_apdInf.append(ap_title)
                list_apdInf.append(ap_link)
                list_apdInf.append(ap_click)
                list_apdInf.append(title)
                list_apdInf.append(line)

                # 6.（2）附件存到csv文件
                with open("教务处通知.csv", mode='a', encoding='utf-8-sig', newline='') as f:
                    csv.writer(f).writerow(['','','','', ap_title, ap_link, ap_click])
                # 7.（2）存到数据库
                doSql(prc_sql(table2,list_apdInf))

                # 8.下载附件
                ctt = requests.get(ap_link)
                where = "附件/" + ap_title
                with open(where, "wb") as code:
                    code.write(ctt.content)

            print(str(l_ap) + "个附件" + "加载成功")
        #input()    # 调试
        print(" 第" + str(line) + "条加载成功")
        print("=============")# 装饰
    cover_but() # 装饰一页结束
    print("=============")  # 装饰
    print("第"+str(page)+"页网址："+url)
    time.sleep(random.randint(2,2)) # 听说这个语句可以延时

    # 下一次循环开始
    url= fro + "/jxtz/" + str(i - 1) + ".htm"
print("=============")  # 装饰
print("共"+str(line)+"条通知")

# 显示数据库内容
res=cur.fetchone()# test

# 关闭数据库
cur.close()  # 关闭
connect.close()