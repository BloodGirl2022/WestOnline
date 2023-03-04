import fs,requests
from init import app,User,Music
from flask import request
import prettytable as pt # 取别名
from init import db

'''
跨域功能尚未完善
'''
# 增添：构建成字典格式
headers={
    'cookie': '_ga=GA1.2.719429030.1677493383; _gid=GA1.2.84836575.1677674786; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1677493383,1677674789; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1677679156; _gat=1; kw_token=6CEVHP6TTHQ',
    'referer': 'http://www.kuwo.cn/search/list?key=a',
    'csrf': '6CEVHP6TTHQ',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
}
# 制作一个可视化table格式
tb = pt.PrettyTable()
tb.field_names = ['序号', 'rid', '歌名', "下载地址", '歌手', '专辑名', '时长表示', 'VIP']  # 8
# print(tb)

# 搜索音乐
sear_list=[]
@app.route('/search?text=<text>', methods=['GET','POST'])
def sear(text):

    # 1.发送请求 返回响应
    # Request Method: GET  所以request后为get
    url = 'https://kuwo.cn/api/www/search/searchMusicBykeyWord?key=' + text  # 酷我网址
    # debug:requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    # url写错了
    # 原因：url写错了
    # url直接网址复制粘贴了，其实要在Headers里找
    resp = requests.get(url=url, headers=headers)
    resp.encoding = 'utf-8'
    # 2.获取数据 json
    # 和response里的数据一样
    # <Response [200]> 请求成功
    '''
    增添：
    # json是前后端数据交互格式 —— 和 字典 相互转化
    # 前端：1.负责好看 2.同一页面显示不同数据（实时变化）
    # 后端：具体功能实现 
    '''
    html_json = resp.json()  # 返回的response
    # print(html_json)  # test

    # 3.解析数据 获取数据
    judge = fs.authorized_user(request.headers.get("Authorization"))
    if not judge:
        return fs.fail()
    cnt = 0  # 条数为0

    html_json2 = html_json['data']['list']
    for i in html_json2:
        # 4.解析数据 rid 歌名  音乐的下载地址 歌手  专辑名 时长 时长表示 VIP
        # (1) 存数据
        rid = i['rid']  # rid
        # print(rid)
        name = i['name']  # 歌名
        # mus_url # 音乐的下载地址
        art = i['artist']  # 歌手
        alb = i['album']  # 专辑名
        dur = i['songTimeMinutes']  # 时长表示（字符串）
        isFee = i['isListenFee']  # 是否需要VIP

        # （2）音乐下载比较难搞
        # 这是一个音乐信息的网站，不止有下载地址
        music_inform_url = f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}"  # 音乐网址通过rid分别;
        if isFee:
            mus_url = "None"
        else:
            mus_url = requests.get(music_inform_url).json()['data']['url']  # 我们通过rid，取出音乐的下载地址
        # print(mus_url)

        # 记录表格
        info=[cnt, "rid", name, mus_url, art, alb, dur, isFee]  # 一首信息
        tb.add_row(info)  # 添加一条
        # 记录到数据库
        db.session.add(info)
        db.session.commit()
        # 此列表每次都清理为0，更新
        dic=fs.music_inform(cnt, rid, name, mus_url, art, alb, dur, isFee)  # 搜索记录
        sear_list.append(dic)

    # 展示表格 提供选项
    print(tb)
    return jsonify(code=200, message="success", data=sear_list)     # 上下十行左右不确定

# 下载音乐
@app.route('/search/download/:<rid>', methods=['GET', 'POST'])
def dnld(rid):      # 这里cnt咋给呀 ，咋传
    while (1):
        index = int(input("请输入你要下载的歌曲的rid（-1退出）"))
        try:
            if index == -1:
                return
            else:
                song = ()
                with open(f'music/{song[2]}.mp3', mode='wb') as f:  # 4是作者
                    if song[3] == "None":
                        return jsonify(fs.fail(fs.dnld_fail))
                    else:
                        mus_data = requests.get(song[3]).content  # 音乐数据内容
                        f.write(mus_data)  # 下载音乐(感觉有bug)
                        path='music/'+song[2]+'.mp3'
                        return open(path,mode='r')  # 不知行不行
        except:
            return jsonify(fs.fail(fs.dnld_fail))


