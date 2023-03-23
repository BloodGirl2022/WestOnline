from flask import redirect,jsonify,render_template,request,Flask,url_for
from mysql import app
import sys
sys.path.append('/path/to/PyJWT')
import myjwt
from mysql import User,Music
# import jwt,PyJWT  # 安装PyJWT库，可以通过 pip install PyJWT 命令来安装。
# from mysql import app
from mysql import db
import mysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from flask import Blueprint
# music
import prettytable as pt # 取别名
import fs,requests
from werkzeug.security import check_password_hash

'''
python 是引用传递
'''
# ==============================================================#
# 创建一个Flask应用实例对象
# 其中`_name_`是当前模块的名称，用于Flask 知道应该在哪里查找静态文件和模板文件等。
# app = Flask(__name__)

# 登录
@app.route('/user/login',methods=['GET','POST'])
# @app.route('/user/login',methods=['GET','POST'],endpoint='a')
# endpoint，别名，如果不写的话
# 【用来redirect(url_for(a))】
def login( ):
    # return '登录'   # HttpResponse
    # 直接返回一个字符串'登录'
    # 这相当于 'HttpResponse('登录')
    # 浏览器将会显示出"登录”这个文本;
    # return render_template('login.html')  # render

    if request.method == 'GET':
        return redirect("http://localhost:5173/#/login")
    # 正常访问网址时就打开界面，前端界面
    # 不确定

    # data = request.get_json()
    '''问题1：获取的是表单数据，而不是get_json，大家都用get_json，我不知道这俩啥区别具体咋搞'''

    # post表单数据时，处理数据，以下是处理数据
    info = request.form  # 获取表单数据
    get_username = info.get('username')
    get_password = info.get('password') # 拿到的是password不是hash_password
    # fs.get_form(info,get_username,get_password,'')
    return "21"
#     get_hash_password = fs.hash(get_password)    # 将get到的密码hash处理
#     # print('-TEST-GET获取到的用户名和密码如下:',end='')
#     # print(fs.show_uandp(get_username, get_password))  # 检查是否正确得到用户名和密码
#     # print('-TEST-the type of username is:',end='')
#     # print(type(username))
#
#     # 因为把username设置为了主键，所以这里可以直接查到信息
#     user = User.query.get(get_username) # 在数据库中查找username，以及对应id
#     '''
#     问题3：是否可以查到信息。为什么查不到呢，明明username是主键
#         解答：
#             查得到。查不到可能有以下几个原因：
#         <1> 数据库未保存
#         <2> 未将其设置为主键
#     '''
#     # print('-TEST-User.query.get("admin")是',end='')
#     # print(user)
#
#     if(user==None): # 查询是否存在用户信息（username）
#         return jsonify(fs.fail404("用户信息不存在,请注册！"))
#     else:   # 用户信息存在
#         store_id=user.id    # 查询到的id
#
#         # login = user.check_password_hash(get_password)  # 通过hash校验密码
#         # print(login)
#
#         store_password=user.hash_password
#
#         print(get_hash_password)
#         print(store_password)
#
#         # 用封装好的函数生成token
#         token = myjwt.crt_token(get_username, user.hash_password)
#         user.token=token    # 存token
#         # （TEST）数据库中的
#         # print(fs.show_iuandp(store_id, get_username, store_password))  # 检查是否正确得到用户名和密码,数据库中的
#         if myjwt.ckpwd(store_password,get_hash_password): # 判断这俩家伙是否相等
#             return jsonify(fs.suc(fs.lgin_suc(store_id, user.username, token)))  # 成功    链接数据库
#         else:   # 密码哈希值不正确
#             # print(store_password)                                                                                                                                                                                          print(get_hash_password)
#             return jsonify(fs.fail404("密码错误"))
#
# 注册 test 成功
@app.route('/user', methods=['POST'])
def register():
    if request.method == 'GET':
        return redirect("http://localhost:5173/#/login")
    # 正常访问网址时就打开界面，前端界面

    # post表单数据时，处理数据，以下是处理数据
    info = request.form  # 获取表单数据
    get_username = info.get('username')
    # print(get_username)#test
    get_password = info.get('password')  # 注意拿到的是password不是hash_password!不要写错了
    get_checkPassword=info.get('checkPassword')
    print(get_username,get_password,get_checkPassword)    # 正确获得

    with app.app_context():  # 任何与数据库有关的操作都要在数据库app的下面
        try:
            user = User.query.get(str(get_username))# 在数据库中查找username
        except Exception as e:
            print(f"Error querying user: {e}")
            user = None  # 将 user 设置为默认值
        else:
            if not user:
                print(f"No user found with username: {get_username}")
                user = None  # 将 user 设置为默认值

#         # if (user != None):  # 查询是否存在用户信息（username）
#             print(user)#test
#             return jsonify(fs.fail404("用户名已存在,请重新注册！"))
# #         # 用户信息可以注册
# #         # 问题4：密码长度和密码是否相同前端已经确认了，这里需要再次确认吗？
#         if(get_password!=get_checkPassword):
#             return jsonify(fs.fail404("两次密码输入不同,请重新注册！"))
#
#         # 数据库处理
#         hash_password=fs.hash(get_password)
#         # print(fs.hash(str(123456)))   # 123456的哈希
#         # 密码合理
#         mysql.add_user(get_username,hash_password)  # 增添一条信息，密码用哈希处理
#
#         # 问题6：自增的id不知道能不能直接获得
#         user = User.query.get(get_username)  # 在数据库中查找username，以及对应id
        store_id = user.id  # 查询到的id

        return fs.suc(fs.regi_suc(store_id,get_username))
        # return redirect(url_for('login'))
    # return "redirect"
#
# '''Music'''
# # 增添：构建成字典格式
# @app.route('/search', methods=['GET','POST'])
# def sear():
#     headers = {
#         'cookie': '_ga=GA1.2.719429030.1677493383; _gid=GA1.2.84836575.1677674786; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1677493383,1677674789; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1677679156; _gat=1; kw_token=6CEVHP6TTHQ',
#         'referer': 'http://www.kuwo.cn/search/list?key=a',
#         'csrf': '6CEVHP6TTHQ',
#         'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
#         }
#
#     # 制作一个可视化table格式
#     tb = pt.PrettyTable()
#     tb.field_names = ['序号', 'rid', '歌名', "下载地址", '歌手', '专辑名', '时长表示', 'VIP']  # 8
#     cnt = 1
#
#     text = request.args.get('text') # query请求函数
#     # text = input("text:")
#     url = 'https://kuwo.cn/api/www/search/searchMusicBykeyWord?key=' + text  # 酷我网址
#
#     resp = requests.get(url=url, headers=headers)
#     resp.encoding = 'utf-8'
#     html_json = resp.json()  # 返回的response
#     html_json2 = html_json['data']['list']  # 取数据
#
#     song_list_return = []  # 只包含返回信息
#     song_list = []  # 包含所有信息
#     for i in html_json2:
#         # 4.解析数据 rid 歌名  音乐的下载地址 歌手  专辑名 时长 时长表示 VIP
#         # (1) 存数据
#         rid = i['rid']  # rid
#         # print(rid)
#         name = i['name']  # 歌名
#         # print(name) # 正常
#         # mus_url # 音乐的下载地址
#         artist = i['artist']  # 歌手
#         album = i['album']  # 专辑名
#         duration = i['songTimeMinutes']  # 时长表示（字符串）
#         isFee = i['isListenFee']  # 是否需要VIP
#
#         # （2）音乐下载比较难搞
#         # 这是一个音乐信息的网站，不止有下载地址
#         music_inform_url = f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}"  # 音乐网址通过rid分别;
#         if isFee:
#             mus_url = "None"
#         else:
#             mus_url = requests.get(music_inform_url).json()['data']['url']  # 我们通过rid，取出音乐的下载地址
#             # 上面这个地址，mus_url，直接打开即可下载
#
#         # 添加到表格
#         song_info = [cnt, rid, name, mus_url, artist, album, duration, isFee]  # 问题7：如何在列表最前面添加元素？
#         tb.add_row(song_info)  # 添加一条
#         song_list.append(song_info)
#         cnt += 1
#
#         # 添加到数据库
#         with app.app_context():
#             mysql.add_music(song_info)
#
#         # 制作return json
#         # 最后把整合好的list传进suc
#         song = fs.mk_song(name, artist, album, duration, rid)  # 一首歌的信息，返回为字典
#         # print(song) # 字典正常
#         song_list_return.append(song)  # 歌曲信息集
#     print(tb)
#     # print(song_list)
#
#     final_dic = fs.suc({"list": song_list_return})
#     return jsonify(final_dic)
#     # print(tb)
#
# # 下载
# @app.route('/search/download/<rid>', methods=['GET','POST'])
# def download(rid):
#     try:
#         '''
#         查询:filter_by精确查询
#         返回名字等于wang的所有人
#         User.query.filter_by(name='wang').all()
#         '''
#         song = Music.query.get(int(rid))  # 如果查不到，会有错误，被捕捉
#         '''
#         'song`是一个'Music`对象
#         根据代码片段中的`Music.query.get( int(rid))'可以看出，我们是通过`rid`获取`Music对象的。
#         ‘Music`是一个ORM (对象关系映射）模型，它是我们定义的一个数据表，包含了多个属性(如`name'、'mus_url等)。
#         当我们通过查询获取到—个'Music `对象时，该对象就包含了所有该数据表的属性和相关方法，我们可以通过调用它们来获取或操作该对象的各个属性。
#         '''
#         print(song.rid)
#         print(song.name)
#         '''
#         其中，'song.name`表示获取song对象的name属性的值
#         ` Song.mus_url'表示获取mus_url属性的值。
#         如果song不存在，则会输出Cannot find song with rid XXX的提示。
#         '''
#         if song.mus_url == "None":
#             print(jsonify(fs.fail404(fs.dnld_fail)))
#             return jsonify(fs.fail404(fs.dnld_fail))
#
#         if (song.isFee == True):  # 3是下载地址
#             print("付费！")
#         else:
#             with open(f'music/{song.name}.mp3', mode='wb') as f:  # 2是歌名  这是路径
#                 mus_data = requests.get(song.mus_url).content  # 音乐数据内容 3是下载地址
#                 f.write(mus_data)  # 下载音乐(感觉有bug)
#                 path = 'music/' + song.name + '.mp3'  # 3是下载地址
#                 return open(path, mode='r')     # 这个应该是返回一个文件？
#                 # 非常好，成功了
#                 # return "suc"
#
#     except Exception as e:
#         print(e)
#         return jsonify(fs.fail404(fs.dnld_fail))
#
# # 删除历史记录
# @app.route('/user/history', methods=['DELETE'])
# def delete():
#     # Authorization = request.headers.get('Authorization')  # 获取
#     # if not Authorization:
#     #     return fs.fail404("未登录")
#     # token = myjwt.authorized_user(Authorization)
#     # if not token:
#     #     return fs.fail403()  # token检验失败
#
#     data = request.get_json()  # 不知道什么json。应该是body里的
#     type = data.get('type')
#     id = data.get('id')  # type为0时根据\id删除
#     list = data.get('list')  # type为1时删除id为list中的所有数字
#     # print(data)
#     # print(type)
#     # print(id)
#     # print(list)
#     try:
#         if type == 0:  # type为0时根据id删除
#             with app.app_context():
#                 # Working outside of application context
#                 # 不加上面这句就会疯狂报错，哼！
#                 music = Music.query.filter(Music.id == id)
#                 # print(music.first())
#                 db.session.delete(music.first())
#                 db.session.commit()
#         elif type == 1:
#             for i in list:
#                 try:
#                     music = Music.query.filter(Music.id == i)
#                     db.session.delete(music.first())
#                     db.session.commit()
#                 except:
#                     pass  # 此处，查不到id时，说明不存在，报错则忽略
#                     # 可查到id时，则正常删除
#         return fs.suc0()
#     except:
#         return fs.fail404(fs.dlt_fail)
#
#
# # 获取历史记录
# @app.route('/user/history', methods=['GET'])
# def get_hisroty():
#     # Authorization = request.headers.get('Authorization')  # 获取
#     # if not Authorization:
#     #     return fs.fail404("未登录")
#     # token = myjwt.authorized_user(Authorization)
#     # if not token:
#     #     return fs.fail403()  # token检验失败
#
#     page = int(request.args.get('page'))  # query请求函数
#     per_page = 10  # 每10条获取一次
#
#     # length = Music.query.count()    # 表长度-正常获取
#     # start = (page-1)*10+1   # 起始条数
#     # end = page*10   # 终止条数
#
#     music_list = Music.query.order_by(asc(Music.id)).paginate(page=page, per_page=per_page)
#     count = music_list.pages  # 获取总共的页数
#
#     # 这里使用`paginate()`方法进行分页查询
#     # 参数`page`表示要获取的页数
#     # `per_page`表示每页显示的记录数
#     # `order_by()`方法接收一个按照id属性升序排序的函数，在这里我们使用的是`asc()`方法。
#
#     # 以下是整合数据拼成返回格式
#     list = fs.mk_history(music_list)  # list
#     data_dic = {"list": list, "count": count}  # data
#     return_dic = fs.suc(data_dic)  # return
#
#     # 返回
#     return return_dic
#
#
# # 修改历史记录收藏
# @app.route('/user/history/lc', methods=['PUT'])  # lc啥意思？
# def lc():
#     Authorization = request.headers.get('Authorization')  # 获取
#     if not Authorization:
#         return fs.fail404("未登录")
#     token = myjwt.authorized_user(Authorization)
#     if not token:
#         return fs.fail403()  # token检验失败
#
#     data = request.get_json()  # body里的
#     fav = data.get('fav')
#     id = data.get('id')  # type为0时根据id删除
#
#     music = Music.query.filter(Music.id == id).first()  # 找到信息.因为只有1条，所以取【0】就行（不太会用get）
#     music.fav = fav  # 更改
#     db.session.commit()  # 保存
#
#     return fs.suc(fs.mk_song2(music))  # 返回
#
# ==============================================================#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    '''问题2：为什么要用0.0.0.0？'''
    # 要放在最后呀！放在前面会报错
    # 启动Web服务器。
    # 其中 'host参数指定服务器监听的地址，默认为`127.0.0.1，即只能本机访问。
    # 这里使用'0.0.0.0"让服务器监听所有的网络接口
    # ==============================================================#
