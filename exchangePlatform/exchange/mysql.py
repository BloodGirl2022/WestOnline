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
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/exchangePlatform?charset=utf8"  # 手动创建数据库
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)
# 链接数据库
db = SQLAlchemy(app)
# ==============================================================#
# ==============================================================#
# 创建表-用户存储信息（手机号一定要填）
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)  # 序号：内容非空,不重复,自增,主键 # 问题5：明明已经设置为自增长，但是创建数据库的时候依然不是自增
    username = db.Column(db.String(15), nullable=False, unique=True)  # 用户名：内容非空
    hash_password = db.Column(db.String(511), nullable=True)  # 密码：内容可空
    # token = db.Column(db.String(511), nullable=False)  # token：内容非空 # token前端会给你
    email = db.Column(db.String(31),nullable=True)  # 邮箱：内容可为空
    phone_number = db.Column(db.Integer,nullable=True )  # 手机号：内容可为空
    real_name = db.Column(db.String(50),nullable=True) # 手机号:内容可为空
    register_time = db.Column(db.DateTime,nullable=False)  # 注册时间:内容非空
    last_time = db.Column(db.DateTime, nullable=False)  # 上次登录时间:内容非空

# ==============================================================#
# 执行
# with app.app_context():  # debug的时候加这句不会错
#     db.drop_all()  # 删除所有表
#     db.create_all()  # 创建所有表
#     db.session.commit()
# ==============================================================#