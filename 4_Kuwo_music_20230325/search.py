from flask import redirect,jsonify,render_template,request,Flask,url_for
import fs
import sys
sys.path.append('/path/to/PyJWT')
import myjwt
from mysql import User,Music
# import jwt,PyJWT  # 安装PyJWT库，可以通过 pip install PyJWT 命令来安装。
from mysql import app
from mysql import db
import mysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from flask import Blueprint
import prettytable as pt # 取别名
import fs,requests

search = Blueprint('search', __name__)

'''Music'''
# 增添：构建成字典格式
@search.route('/search', methods=['GET','POST'])
def sear():
    headers = {
        'cookie': '_ga=GA1.2.719429030.1677493383; _gid=GA1.2.84836575.1677674786; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1677493383,1677674789; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1677679156; _gat=1; kw_token=6CEVHP6TTHQ',
        'referer': 'http://www.kuwo.cn/search/list?key=a',
        'csrf': '6CEVHP6TTHQ',
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
        }

    # 制作一个可视化table格式
    tb = pt.PrettyTable()
    tb.field_names = ['序号', 'rid', '歌名', "下载地址", '歌手', '专辑名', '时长表示', 'VIP']  # 8
    cnt = 1

    text = request.args.get('text') # query请求函数
    # text = input("text:")
    url = 'https://kuwo.cn/api/www/search/searchMusicBykeyWord?key=' + text  # 酷我网址

    resp = requests.get(url=url, headers=headers)
    resp.encoding = 'utf-8'
    html_json = resp.json()  # 返回的response
    html_json2 = html_json['data']['list']  # 取数据

    song_list_return = []  # 只包含返回信息
    song_list = []  # 包含所有信息
    for i in html_json2:
        # 4.解析数据 rid 歌名  音乐的下载地址 歌手  专辑名 时长 时长表示 VIP
        # (1) 存数据
        rid = i['rid']  # rid
        # print(rid)
        name = i['name']  # 歌名
        # print(name) # 正常
        # mus_url # 音乐的下载地址
        artist = i['artist']  # 歌手
        album = i['album']  # 专辑名
        duration = i['songTimeMinutes']  # 时长表示（字符串）
        isFee = i['isListenFee']  # 是否需要VIP

        # （2）音乐下载比较难搞
        # 这是一个音乐信息的网站，不止有下载地址
        music_inform_url = f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}"  # 音乐网址通过rid分别;
        if isFee:
            mus_url = "None"
        else:
            mus_url = requests.get(music_inform_url).json()['data']['url']  # 我们通过rid，取出音乐的下载地址
            # 上面这个地址，mus_url，直接打开即可下载

        # 添加到表格
        song_info = [cnt,rid, name, mus_url, artist, album, duration, isFee]  # 问题7：如何在列表最前面添加元素？
        tb.add_row(song_info)  # 添加一条
        song_list.append(song_info)
        cnt += 1

        # 添加到数据库
        with app.app_context():
            if Music.query.get(song_info[1])==None:

                mysql.add_music(song_info)

        # 制作return json
        # 最后把整合好的list传进suc
        song = fs.mk_song(name, artist, album, duration, rid)  # 一首歌的信息，返回为字典
        # print(song) # 字典正常
        song_list_return.append(song)  # 歌曲信息集
    print(tb)
    # print(song_list)

    final_dic = fs.suc({"list": song_list_return})
    return jsonify(final_dic)
    # print(tb)
    # return '3'

# 下载
@search.route('/search/download/<rid>', methods=['GET','POST'])
def download(rid):
    try:
        '''
        查询:filter_by精确查询
        返回名字等于wang的所有人
        User.query.filter_by(name='wang').all()
        '''
        song = Music.query.get(int(rid))  # 如果查不到，会有错误，被捕捉
        '''
        'song`是一个'Music`对象
        根据代码片段中的`Music.query.get( int(rid))'可以看出，我们是通过`rid`获取`Music对象的。
        ‘Music`是一个ORM (对象关系映射）模型，它是我们定义的一个数据表，包含了多个属性(如`name'、'mus_url等)。
        当我们通过查询获取到—个'Music `对象时，该对象就包含了所有该数据表的属性和相关方法，我们可以通过调用它们来获取或操作该对象的各个属性。
        '''
        print(song.rid)
        print(song.name)
        '''
        其中，'song.name`表示获取song对象的name属性的值
        ` Song.mus_url'表示获取mus_url属性的值。
        如果song不存在，则会输出Cannot find song with rid XXX的提示。
        '''
        if song.mus_url == "None":
            print(jsonify(fs.fail404(fs.dnld_fail)))
            return jsonify(fs.fail404(fs.dnld_fail))

        if (song.isFee == True):  # 3是下载地址
            print("付费！")
        else:
            with open(f'music/{song.name}.mp3', mode='wb') as f:  # 2是歌名  这是路径
                mus_data = requests.get(song.mus_url).content  # 音乐数据内容 3是下载地址
                f.write(mus_data)  # 下载音乐(感觉有bug)
                path = 'music/' + song.name + '.mp3'  # 3是下载地址
                return open(path, mode='r')     # 这个应该是返回一个文件？
                # 非常好，成功了
                # return "suc"
    except Exception as e:
        print(e)
        return jsonify(fs.fail404(fs.dnld_fail))