from flask import request, jsonify, Blueprint
from DAL.mysql import db, Merchandise
from datetime import datetime
import jwt
# sys.path.append('/path/to/PyJWT')
from configs import util

SECRET_KEY = util.SECRET_KEY

merchandise = Blueprint('merchandise', __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return jsonify({'message': '未提供token，请先登录！', "code": 408})
        try:
            payload = jwt.decode(Authorization, SECRET_KEY, algorithms=["HS256"])
            print(payload)
        except Exception:
            return jsonify({'message': 'JWT签名检验失败！', "code": 410})  # token检验失败

        payload = util.authorized_user(Authorization)  # return payload
        print(payload)  # 返回id，username，password等

        if not payload:
            return jsonify({'message': 'token检验失败(用户不存在)！', "code": 409})  # token检验失败

        return func(*args, **kwargs)
    return wrapper


# 添加商品
# add_merchandise()方法接收前端传递的json数据，解析出商品的各个属性值，
# 创建一个Merchandise对象，将其添加到数据库中，实现商品的上传。
@merchandise.route('/merchandise/upload', methods=['POST'])
def add_merchandise():

    data = request.get_json()  # 从前端获取JSON数据
    name = data['name']  # 从JSON数据中获取商品名称
    price = data['price']  # 从JSON数据中获取商品价格
    category = data['category']  # 从JSON数据中获取商品分类
    stock = data['stock']  # 从JSON数据中获取商品库存
    description = data['description']  # 从JSON数据中获取商品描述
    image = data['image']  # 从JSON数据中获取商品图片

    # 创建一个Merchandise对象，传入商品各个属性值
    merchandise = Merchandise(name=name, price=price, category=category, stock=stock,
                              description=description, image=image, create_time=datetime.now())

    # 将Merchandise对象添加到数据库中
    db.session.add(merchandise)
    db.session.commit()

    # 返回JSON格式的响应，表示商品添加成功
    return jsonify({'message': '添加成功！',"code":203})

# 查询商品
# search_merchandise()方法接收前端传递的查询条件，使用query对象动态生成查询语句，
# 查询出符合条件的商品，并进行分页处理。
@merchandise.route('/merchandise/search', methods=['GET'])
def search_merchandise():

    # 从前端获取查询条件
    id = request.args.get('id')  # 获取商品id
    name = request.args.get('name')  # 获取商品名称
    category = request.args.get('category')  # 获取商品类别
    page = request.args.get('page', default=1, type=int)  # 获取页码，默认为第一页
    per_page = request.args.get('per_page', default=10, type=int)  # 获取每页展示的商品数量，默认为10个商品

    # 创建Merchandise查询对象
    query = Merchandise.query

    # 查询指定id的商品对象
    merchandise = Merchandise.query.get(id)
    # 判断是否查询到了商品对象
    if merchandise is None:
        # 返回JSON格式的响应信息
        return jsonify({'message': '查询失败，商品不存在！', "code": 411})

    # 根据查询条件动态生成查询语句（按照优先级）
    if id:# 如果请求参数中有商品名称，则添加 name 过滤条件到查询语句中
        query = query.filter_by(id=id)
    if name: # 如果请求参数中有商品名称，则添加 name 过滤条件到查询语句中。
        query = query.filter(Merchandise.name.like('%'+name+'%'))
    if category:# 如果请求参数中有商品类别，则添加 category 过滤条件到查询语句中
        query = query.filter_by(category=category)

    # 进行分页处理，返回分页结果
    result = query.paginate(page=page, per_page=per_page)
    # 调用 query.paginate() 方法进行分页处理，返回一个 Pagination 对象，其中 page 表示当前页码，per_page 表示每页展示的商品数量。
    # page和per_page分别表示当前页数和每页显示的商品数量，这两个参数均由前端传递过来，如果前端未传递，则默认值为1和10

    # 返回JSON格式的响应，包括查询结果和商品总数
    return jsonify({'data': [i.serialize() for i in result.items], 'total': result.total,'code':204})

# 修改商品信息
# 使用PUT方法请求'/merchandise/update/<int:id>'路由，其中<int:id>表示动态路由，id是商品的唯一标识符
@merchandise.route('/merchandise/update/<int:id>', methods=['POST'])
def update_merchandise(id):

    # 获取请求体中传递的JSON数据，并解析其中的商品属性
    data = request.get_json()
    name = data['name']
    price = data['price']
    category = data['category']
    stock = data['stock']
    description = data['description']
    image = data['image']

    # 查询指定id的商品对象
    merchandise = Merchandise.query.get(id)
    # 判断是否查询到了商品对象
    if merchandise is None:
        # 返回JSON格式的响应信息
        return jsonify({'message': '修改失败，商品不存在！',"code":411})

    # 查询指定id的商品对象
    merchandise = Merchandise.query.get(id)
    # 更新商品对象的属性
    merchandise.name = name
    merchandise.price = price
    merchandise.category = category
    merchandise.stock = stock
    merchandise.description = description
    merchandise.image = image
    merchandise.update_time = datetime.now()

    # 将更新后的商品信息保存到数据库
    db.session.commit()

    # 返回JSON格式的响应信息
    return jsonify({'message': '修改成功！','code':205})

# 删除商品
# 使用DELETE方法请求'/merchandise/delete/<int:id>'路由，其中<int:id>表示动态路由，id是商品的唯一标识符
@merchandise.route('/merchandise/delete', methods=['DELETE'])
def delete_merchandise():
    # 获取请求体中传递的JSON数据，并解析其中的商品属性
    data = request.get_json()
    id=data["id"]

    # 查询指定id的商品对象
    merchandise = Merchandise.query.get(id)

    # 判断是否查询到了商品对象
    if merchandise is None:
        # 返回JSON格式的响应信息
        return jsonify({'message': '修改失败，商品不存在！',"code":411})

    # 从数据库中删除商品对象
    db.session.delete(merchandise)
    # 将删除操作保存到数据库
    db.session.commit()

    # 返回JSON格式的响应信息
    return jsonify({'message': '删除成功！',"code":206})

# @merchandise.route('/merchandise/pay/<int:id>', methods=['POST'])
# def pay_merchandise(id):
#     # 获取请求体中传递的JSON数据，并解析其中的商品属性
#     data = request.get_json()
#     amount = data['amount']  # 支付金额
#     payment_method = data['payment_method']  # 支付方式
#
#     # 查询指定id的商品对象
#     merchandise = Merchandise.query.get(id)
#     # 判断是否查询到了商品对象
#     if merchandise is None:
#         # 返回JSON格式的响应信息
#         return jsonify({'message': '支付失败，商品不存在！', "code": 411})
#
#     # 检查支付金额是否正确
#     if amount != merchandise.price:
#         return jsonify({'message': '支付失败，支付金额不正确！', "code": 412})
#
#     # 调用第三方支付接口，获取支付状态
#     payment_status = call_payment_api(amount, payment_method)
#
#     # 判断支付状态是否成功
#     if payment_status == 'SUCCESS':
#         # 更新商品库存
#         merchandise.stock -= 1
#         # 将更新后的商品信息保存到数据库
#         db.session.commit()
#         # 返回JSON格式的响应信息
#         return jsonify({'message': '支付成功！'})
#     else:
#         # 返回JSON格式的响应信息
#         return jsonify({'message': '支付失败！', "code": 413})
#
# def call_payment_api(amount, payment_method):
#     # 模拟支付接口的调用过程
#     # 假设支付方式为微信支付，成功的概率为90%
#     if payment_method == 'wechat_pay':
#         if random.random() < 0.9:
#             return 'SUCCESS'
#         else:
#             return 'FAIL'
#     # 假设支付方式为支付宝支付，成功的概率为80%
#     elif payment_method == 'alipay':
#         if random.random() < 0.8:
#             return 'SUCCESS'
#         else:
#             return 'FAIL'
#     # 如果支付方式不支持，则返回失败
#     else:
#         return 'FAIL'
