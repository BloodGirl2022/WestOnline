# 导入所需的库
import fs as db
import jwt as jwt
import requests, json
from flask import Flask, jsonify, redirect
from flask import SQLAlchemy
import pymysql
from sqlalchemy.testing.pickleable import User
import hashlib
import random
import string

#==============================================================#
# 创建链接数据库
pymysql.install_as_MySQLdb()
# 初始化Flask
app = Flask(__name__)
#==============================================================#
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
#==============================================================#
class Config():
    DEBUG=True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/tdl?charset=utf8" # 手动创建数据库
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config.from_object(Config)
#==============================================================#
# 不太明白上面代码的意思，但不敢动它，一不小心就报错
#==============================================================#
# 链接数据库
db = SQLAlchemy(app)
#==============================================================#
# 函数
# 用来将密码用哈希算法加密的算法
def generate_password_hash(s: str):
    # 随机生成长度为4的盐值
    salt = "".join([random.choice(string.ascii_lowercase) for i in range(4)])

    # 拼接原始密码和盐值
    s = s + salt

    # 对加入盐值的字符串加密
    _md5 = hashlib.md5()
    _md5.update(s.encode("utf-8"))
    return salt + "$" + _md5.hexdigest()    # 返回 盐值+哈希值 的字符串
#==============================================================#

# 从酷我音乐网页上获取搜索结果
def getSearchResult(keyword):
    url = 'http://www.kuwo.cn/search/list?key=' + keyword
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# 跨域功能
@app.route('/cross-domain', methods=['GET','POST'])
def cross_domain():
    # 获取前端传来的数据
    data = requests.get_json()
    # 进行跨域请求
    headers = {'Access-Control-Allow-Origin': '*'}
    response = requests.post('https://console-docs.apipost.cn/preview/40c70e0e04322bed/9a886251aff222d0', data=data, headers=headers)
    data = json.loads(response.text)
    # 返回数据给前端
    return jsonify(data)

# 登录注册功能
@app.route('/login', methods=['POST'])
def login():
    # 获取前端传来的数据
    data = requests.get_json()
    # 进行密码哈希处理
    password = generate_password_hash(data['password'])
    # 查询用户名和密码是否正确
    user = User.query.filter_by(username=data['username'],password=password).first()
    if user:
        # 生成token
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256') # 返回token给前端
        return jsonify({'token': token.decode('utf-8')})
    else:
        # 返回错误信息给前端
        return jsonify({'error': 'Incorrect username or password'})

# 使用rid获取歌曲地址
@app.route('/getMusicUrl', methods=['POST'])
def getMusicUrl():
    # 获取前端传来的数据
    data = requests.get_json()
    # 根据rid进行请求
    url = 'https://link.hhtjim.com/?rid=' + data['rid']
    # return jsonify({'error': 'Unauthorized access'})

    response = requests.get(url)
    data = json.loads(response.text)
    # 返回歌曲地址给前端
    return jsonify(data)

# 保存音乐文件历史记录
@app.route('/saveHistory', methods=['POST'])
def saveHistory():
    # 获取前端传来的数据
    data = requests.get_json()
    # 保存历史记录到数据库中
    # history = History(data['user_id'], data['music_name'], data['music_url'])
    history = [data['user_id'], data['music_name'], data['music_url']]
    db.session.add(history)
    db.session.commit()
    # 返回成功信息给前端
    return jsonify({'message': 'success'})

# 收藏音乐文件历史记录
@app.route('/collectHistory', methods=['POST'])
def collectHistory():
    # 获取前端传来的数据
    data = requests.get_json()
    # 查询历史记录
    # history = History.query.filter_by(id=data['history_id']).first()
    # 将历史记录收藏字段置为True
    # history.collected = True
    # 更新数据库
    db.session.commit()
    # 返回成功信息给前端
    return jsonify({'message': 'success'})

# 删除音乐文件历史记录
@app.route('/deleteHistory', methods=['POST'])
def deleteHistory():
    # 获取前端传来的数据
    data = requests.get_json()
    # 查询历史记录
    # history = History.query.filter_by(id=data['history_id']).first()
    # 删除历史记录
    # db.session.delete(history)
    # 更新数据库
    db.session.commit()
    # 返回成功信息给前端
    return jsonify({'message': 'success'})

# 分页搜索
@app.route('/search', methods=['POST'])
def search():
    # 获取前端传来的数据
    data = requests.get_json()
    # 搜索歌曲
    keyword = data['keyword']
    page = data['page']
    page_size = 10
    start = (page-1)*page_size
    end = page*page_size
    data = getSearchResult(keyword)
    # 返回搜索结果给前端
    return jsonify(data[start:end])



