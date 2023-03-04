'''
2023.3.1    星期三     222100306   洪朗晨     Python后端第一轮
'''

'''
            < 笔 记 >
<1>
# json是前后端数据交互格式
# json 和 字典 相互转化
# 键值对方式取值

# 前端：1.负责好看 2.同一页面显示不同数据（实时变化）
# 后端：具体功能实现 

<其他>
python无清屏命令

'''
import requests # 请求网页
import prettytable as pt # 取别名
import pymysql

url='https://kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E5%91%A8%E6%9D%B0%E4%BC%A6&pn=1&rn=20&httpsStatus=1&reqId=2b73dff0-b906-11ed-b1eb-1d6c76c373c5'  # 酷我网址
# debug:requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
# url写错了
# 原因：url写错了
# url直接网址复制粘贴了，其实要在Headers里找
db='music'  # 数据库名字

cnt=0 # 条数为0
list=[]

# 制作一个可视化table格式
tb=pt.PrettyTable()
tb.field_names = ['序号','rid','歌名',"下载地址",'歌手','专辑名','时长表示','VIP']   # 8
# print(tb)

# 《打开链接数据库》
# 数据库叫 music
# 表叫 infos

# 数据库-执行sql语句
# 输入：sql命令
# 功能：执行语句
def doSql(sql):
    #sql='''CREATE TABLE infos(`时间` TEXT,`详情链接` TEXT,`通知单位` TEXT,`标题` TEXT);''' # 表已经创建好了
    #print(sql)         # test
    cur.execute(sql)   # 执行
    conn.commit()        # 提交

# 功能：将某一个条所有信息一起存入数据库
# 输入：信息list
# 输出：无
def ist(dic):
    # 这边全用%s而不是%d是因为有bug无法解决，说只能用这个
    sql = "INSERT INTO `infos` (`序号`,`rid`,`歌名`,`下载地址`,`歌手`,`专辑名`,`时长表示`,`VIP`) VALUES(%s,%s,%s, %s, %s, %s, %s,%s);"   # 8
    cur.execute(sql,(dic["序号"],dic["rid"],dic["歌名"], dic["下载地址"], dic["歌手"], dic["专辑名"], dic["时长表示"],dic['VIP']))
    conn.commit()   # 保存

# 数据库打开预备
conn=pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    #db=db_check,
    charset='utf8'
)
cur = conn.cursor()

# # ====================================
# # 以下语句在自己电脑可删除
# # 创建新数据库
# cur = conn.cursor()
# sql='CREATE DATABASE '+db   # 创建数据库（方便检查）
# doSql(sql)
#
# # 第二次数据库打开预备        # 不知道为什么开两次，但是不打开两次就不行
# conn=pymysql.connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         password='123456',
#         db=db,
#         charset='utf8'
#     )
# cur = conn.cursor()
#
# # 创建新表1 歌曲信息保存
# sql='''
# CREATE TABLE infos
# (
# `序号` INT,
# `rid` text,
# `歌名` text,
# `下载地址` text,
# `歌手` text,
# `专辑名` text,
# `时长表示` text,
# `VIP` bool
# );'''
# doSql(sql)
#
# # 创建新表2 用户信息：用来验证密码是否正确
# sql='''
# CREATE TABLE users
# (
# `序号` INT ,
# `用户名` varchar(15) PRIMARY KEY,
# `密码` text
# );'''
# doSql(sql)
#
# # 以上语句在自己电脑可删除
# # ====================================

'''
# 0.伪装：复制以下信息
* cookie：用户信息
* user-agent：浏览器基本信息
* referer：防盗
'''

# 增添：构建成字典格式
headers={
    'cookie': '_ga=GA1.2.719429030.1677493383; _gid=GA1.2.84836575.1677674786; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1677493383,1677674789; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1677679156; _gat=1; kw_token=6CEVHP6TTHQ',
    'referer': 'http://www.kuwo.cn/search/list?key=a',
    'csrf': '6CEVHP6TTHQ',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
}

# 1.发送请求 返回响应
# Request Method: GET  所以request后为get
resp = requests.get(url=url, headers=headers)
resp.encoding = 'utf-8'
# print(resp)  # <Response [200]>

# 2.获取数据 json
# 和response里的数据一样
# <Response [200]> 请求成功
'''
增添：
# json是前后端数据交互格式 —— 和 字典 相互转化
# 前端：1.负责好看 2.同一页面显示不同数据（实时变化）
# 后端：具体功能实现 
'''
html_json=resp.json()   # 返回的response
# print(html_json)  # test

# 3.解析数据 获取数据
html_json2=html_json['data']['list']

for i in html_json2:
    # 4.解析数据 rid 歌名  音乐的下载地址 歌手  专辑名 时长 时长表示 VIP
    # (1) 存数据
    rid=i['rid']           # rid
    # print(rid)
    name=i['name']         # 歌名
    # mus_url # 音乐的下载地址
    art=i['artist']     # 歌手
    alb=i['album']       # 专辑名
    dur=i['songTimeMinutes']   # 时长表示（字符串）
    isFee=i['isListenFee']           # 是否需要VIP

    # （2）音乐下载比较难搞
    # 这是一个音乐信息的网站，不止有下载地址
    music_inform_url = f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}" # 音乐网址通过rid分别;
    if isFee:
        mus_url="None"
    else:
        mus_url = requests.get(music_inform_url).json()['data']['url']  # 我们通过rid，取出音乐的下载地址
    # print(mus_url)

    # 展示表格
    tb.add_row([cnt, "rid", name, "mus_url", art, alb, dur, isFee])  # 添加一条
    # 此列表每次都清理为0，更新
    infm_list=[cnt, rid, name, mus_url, art, alb, dur, isFee] # 加到数据库
    # print(infm_list)
    list.append(infm_list)
    # 编序号
    cnt += 1
    if cnt>5:
        break

# 展示表格 提供选项
print(tb)

# 运行
while(1):
    index = int(input("请输入你要下载的歌曲序号（-1退出）"))
    if index == -1:
        break
    elif index > cnt:
        print("No such number!")
    else:
        song = (list[index])
        with open(f'music/{song[2]}.mp3', mode='wb') as f:  # 4是作者
            if song[3]=="None":
                print("需要付费下载！")
            else:
                mus_data = requests.get(song[3]).content  # 音乐数据内容
                f.write(bytes(song[3]))  # 下载音乐
                print("下载成功！")
'''
            < debug >
1. 
# debug:requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
# 原因：url写错了
# url直接网址复制粘贴了，其实要在Headers里找

2.
sys.exit()
执行该语句会直接退出程序，这也是经常使用的方法，也不需要考虑平台等因素的影响，一般是退出Python程序的首选方法。
该方法中包含一个参数status，默认为0，表示正常退出，也可以为1，表示异常退出。
'''