import pymysql
from flask_sqlalchemy import SQLAlchemy
# from all import app
from flask import Flask
import random
from datetime import datetime

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

# 创建表-存储用户信息（手机号一定要填）
class User(db.Model):
    '''
    用户表
    '''
    __tablename__ = "user"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)  # 序号：内容非空,不重复,自增,主键 # 问题5：明明已经设置为自增长，但是创建数据库的时候依然不是自增
    username = db.Column(db.String(15), nullable=False, unique=True)  # 用户名：内容非空
    hash_password = db.Column(db.String(511), nullable=True)  # 密码：内容可空
    # token = db.Column(db.String(511), nullable=False)  # token：内容非空 # token前端会给你
    email = db.Column(db.String(31),nullable=True)  # 邮箱：内容可为空
    phone_number = db.Column(db.Integer,nullable=True )  # 手机号：内容可为空
    real_name = db.Column(db.String(50),nullable=True) # 真实姓名:内容可为空
    register_time = db.Column(db.DateTime,nullable=False)  # 注册时间:内容非空
    last_time = db.Column(db.DateTime, nullable=False)  # 上次登录时间:内容非空
    profile_image= db.Column(db.String(15))  # 头像（应该是图片地址）：内容可为空
    # money = db.Column(db.Integer, default=0)  # 序号：内容非空,不重复,自增,主键 # 问题5：明明已经设置为自增长，但是创建数据库的时候依然不是自增


# 创建表-存储商品信息
class Merchandise(db.Model):
    '''
    商品表
    '''
    __tablename__ = "merchandise"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 商品编号：商品的唯一标识符，通常为数字或字符串。
    name = db.Column(db.String(50), nullable=False, default='商品名称')  # 商品名称：商品的名称或描述，可以是文字、图片等。
    price = db.Column(db.Float, nullable=False, default=random.uniform(1, 1000))  # 商品价格：商品的价格，通常为数字。
    category = db.Column(db.String(50), nullable=False, default='商品分类')  # 商品分类：商品所属的分类，可以是文字、数字等。
    stock = db.Column(db.Integer, nullable=False, default=random.randint(1, 100))  # 商品库存：商品的库存数量，通常为数字。
    total_sales = db.Column(db.Integer, nullable=False, default=0)  # 商品总销量：商品的销售数量，通常为数字。
    month_sales = db.Column(db.Integer, nullable=False, default=0)  # 商品年销量：商品的销售数量，通常为数字。
    year_sales = db.Column(db.Integer, nullable=False, default=0)  # 商品月销量：商品的销售数量，通常为数字。
    description = db.Column(db.Text, nullable=True, default='商品描述')  # 商品描述：对商品的详细描述，包括商品的特点、规格、材质、适用人群等信息。
    image = db.Column(db.String(255), nullable=True, default='商品图片')  # 商品图片：商品的图片或照片，可以帮助顾客更好地了解商品。
    evaluation = db.Column(db.Float, nullable=True, default=random.uniform(0, 5))  # 商品评价：顾客对商品的评价，包括评分、评价内容等。
    status = db.Column(db.Boolean, nullable=False, default=True)  # 商品状态：商品的状态，通常为“上架”或“下架”。
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())  # 商品创建时间：不为空
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())  # 商品最后更新时间：不为空

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

class Order(db.Model):
    """
    订单表
    """
    tablename = "order"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 订单编号：订单的唯一标识符，通常为数字或字符串。
    customer_id = db.Column(db.Integer, nullable=False)  # 顾客编号：顾客的唯一标识符，通常为数字或字符串。
    total_price = db.Column(db.Float, nullable=False)  # 订单总价：购买商品的总价，通常为数字。
    status = db.Column(db.String(10), nullable=False)  # 订单状态：订单的状态，通常为文字，如"待付款"、"已付款"、"已发货"、"已完成"等。
    create_time = db.Column(db.DateTime, nullable=False)  # 订单创建时间：订单创建的时间，通常为日期时间格式。
    update_time = db.Column(db.DateTime, nullable=False)  # 订单更新时间：订单更新的时间，通常为日期时间格式。

class OrderDetail(db.Model):
    """
    订单明细表
    """
    tablename = "orderDetail"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 订单明细编号：订单明细的唯一标识符，通常为数字或字符串。
    # order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)  # 订单编号：订单的唯一标识符，通常为数字或字符串。
    merchandise_id = db.Column(db.Integer, nullable=False)  # 商品编号：商品的唯一标识符，通常为数字或字符串。
    price = db.Column(db.Float, nullable=False)  # 商品单价：商品的价格，通常为数字。
    quantity = db.Column(db.Integer, nullable=False)  # 商品数量：购买商品的数量，通常为数字。
    unit_price = db.Column(db.Float, nullable=False)  # 某商品总价：商品的价格，通常为数字。

'''
在订单明细表中，我们可以使用外键order_id关联到订单表中的id字段，从而实现订单和订单明细之间的关联。同时，我们可以将订单明细表中的unit_price字段和total_price字段去掉，因为它们可以通过计算price和quantity来得到。
'''

# ==============================================================#
# 执行
# with app.app_context():  # debug的时候加这句不会错
#     db.drop_all()  # 删除所有表
#     db.create_all()  # 创建所有表
#     db.session.commit()
# ==============================================================#