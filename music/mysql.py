import pymysql
from flask_sqlalchemy import SQLAlchemy
# from all import app
from flask import Flask
# ==============================================================#
app = Flask(__name__)
# ==============================================================#
# 创建链接数据库
pymysql.install_as_MySQLdb()
# 初始化 建库链接库 初始化库
class Config():
    DEBUG = True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/music?charset=utf8"  # 手动创建数据库
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config.from_object(Config)
# 链接数据库
db = SQLAlchemy(app)
# ==============================================================#

# ==============================================================#
# 创建表-用户信息
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,autoincrement=True)  # 序号：内容非空,不重复,自增 # 问题5：明明已经设置为自增长，但是创建数据库的时候依然不是自增
    username = db.Column(db.String(15), nullable=False, primary_key=True, unique=True)  # 用户名：内容非空,主键
    hash_password = db.Column(db.String(511), nullable=False)  # 密码：内容非空
    token = db.Column(db.String(511), nullable=False)  # 密码：内容非空
# 创建表-音乐信息
class Music(db.Model):   # cnt, rid, name, mus_url, art, alb, dur, isFee 7
    __tablename__ = "music"
    id = db.Column(db.Integer, nullable=False, autoincrement=True,unique=True )  # 序号：内容非空,主键,不重复，自增
    rid = db.Column(db.Integer, nullable=False,primary_key=True)  # 用户名：内容非空,主键
    name = db.Column(db.String(255), nullable=False)  # 歌名：内容非空
    mus_url=db.Column(db.String(255), nullable=True)  # 下载地址：内容非空
    artist=db.Column(db.String(255), nullable=False)  # 歌手：内容非空
    album=db.Column(db.String(255), nullable=False)  # 专辑：内容非空
    duration=db.Column(db.String(255), nullable=False)  # 时长：内容非空
    isFee=db.Column(db.String(255), nullable=False)  # 会员：内容非空
    fav=db.Column(db.Integer, nullable=False,default=0)  # 收藏：内容非空,默认未收藏
# fav 收藏信息
class Fav(db.Model):
    __tablename__ = "fav"
    id = db.Column(db.Integer, nullable=False,primary_key=True)  # 序号：内容非空,主键
    rid = db.Column(db.Integer, nullable=False, primary_key=True)  # 用户名：内容非空,主键
    name = db.Column(db.String(15), nullable=False)  # 密码：内容非空
# ==============================================================#

# ==============================================================#
# 执行
# with app.app_context():  # debug的时候加这句不会错
#     db.drop_all()  # 删除所有表
#     db.create_all()  # 创建所有表
#     db.session.commit()
# ==============================================================#

# 增-用户信息增加到数据库
def add_user(name,psw):
    info = User(username=name, hash_password=psw) # 密码已用哈希加密,id自动
    db.session.add(info)  # 能成功添加到数据库
    db.session.commit()

# 增-用户信息增加到音乐库
def add_music(list:list):
    info = Music(rid=list[1], name=list[2], mus_url=list[3], artist=list[4], album=list[5], duration=list[6],
                 isFee=list[7])
    # 密码已用哈希加密,id自动
    db.session.add(info)  # 能成功添加到数据库
    db.session.commit()
    '''
    "name": "兰亭序", //歌名
    "artist": "周杰伦", //歌手
    "album": "魔杰座", //专辑
    "duration": "04:13", //时长
    "rid": 1 //下载id
    '''