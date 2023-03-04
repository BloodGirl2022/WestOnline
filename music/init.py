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

import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# 下面是不太了解的（好像是用来鉴权的）东东
# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import streamlit as st
# import pandas as pd   A

'''
修改：
1. 数据库名称
2. 创建表类名，及table_name
'''
# ==============================================================#
# 创建链接数据库
pymysql.install_as_MySQLdb()
app = Flask(__name__)
# ==============================================================#
# 初始化 建库链接库 初始化库
class Config():
    DEBUG = True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/music?charset=utf8"  # 手动创建数据库
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)
# ==============================================================#
# 不太明白上面代码的意思，但不敢动它，一不小心就报错
# ==============================================================#
# 链接数据库
db = SQLAlchemy(app)
# 创建表-用户信息
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, nullable=False,primary_key=True)  # 序号：内容非空,主键
    username = db.Column(db.String(15), nullable=False, primary_key=True)  # 用户名：内容非空,主键
    password = db.Column(db.String(15), nullable=False)  # 密码：内容非空
# 创建表-用户信息
class Music(db.Model):   # cnt, rid, name, mus_url, art, alb, dur, isFee 7
    __tablename__ = "music"
    id = db.Column(db.Integer, nullable=False, primary_key=True)  # 序号：内容非空,主键
    rid = db.Column(db.Integer, nullable=False, primary_key=True)  # 用户名：内容非空,主键
    name = db.Column(db.String(15), nullable=False)  # 密码：内容非空
    mus_url=db.Column(db.String(15), nullable=True)  # 密码：内容非空
    art=db.Column(db.String(15), nullable=False)  # 密码：内容非空
    alb=db.Column(db.String(15), nullable=False)  # 密码：内容非空
    dur=db.Column(db.String(15), nullable=False)  # 密码：内容非空
    isFee=db.Column(db.Bool, nullable=False)  # 密码：内容非空
# fav
class Fav(db.Model):
    __tablename__ = "fav"
    id = db.Column(db.Integer, nullable=False,primary_key=True)  # 序号：内容非空,主键
    rid = db.Column(db.Integer, nullable=False, primary_key=True)  # 用户名：内容非空,主键
    name = db.Column(db.String(15), nullable=False)  # 密码：内容非空
    Fav = db.Column(db.Bool, nullable=False)  # 密码：内容非空
# ==============================================================#
# 网址和头
vue_url = "http://localhost:5173/#/login"
vue_headers = {
    'referer': 'http://localhost:5173/src/router/index.js',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
}
if __name__ == '__main__':
    with app.app_context():  # debug的时候加这句不会错
        db.drop_all()  # 删除所有表
        db.create_all()  # 创建所有表
        db.session.commit()
    # ==============================================================#
    app.run(port=8000,debug=True)
# ==============================================================#
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

