'''functions'''

import datetime
import jwt
from DAL.mysql import app,User
import hashlib
import os
import configparser

# ==============================================================#
# 加密key，应该存放在环境变量或者配置文件中，不能明文写在程序中
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构造 SECRET_KEY.txt 文件的路径
secret_key_path = os.path.join(project_root, 'configs/SECRET_KEY.txt')
with open(secret_key_path, 'r', encoding='utf-8') as file_obj:  # 将秘钥写在配置文件中
    contents = file_obj.read()
SECRET_KEY = contents.rstrip()  # 秘钥

# # 加载密钥
# config = configparser.ConfigParser()
# config.read('configs.ini')
# SECRET_KEY = config.get('App', 'SECRET_KEY')

# # 获取当前脚本所在的目录
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # 构造 configs.ini 文件的路径
# config_path = os.path.join(current_dir, 'configs/configs.ini')
# # 创建 ConfigParser 实例
# configs = configparser.ConfigParser()
# # 读取配置文件
# configs.read(config_path)
# # 获取 SECRET_KEY
# SECRET_KEY = configs.get('App', 'SECRET_KEY')

# ==============================================================#

# 用来将密码用哈希算法加密的算法
def hash(password:str):
    # 使用SHA-256算法对密码进行哈希，并将结果转换为十六进制字符串。
    hash_obj = hashlib.sha256(password.encode('utf-8'))
    hash_password = hash_obj.hexdigest()
    return hash_password

# 失败
def fail(code,msg):
    return {"code":code, "msg":msg}

# 密码校验.看看get值与数据库中的值（哈希值）是否相等
def ckpwd(get_password,store_password):
    return get_password==store_password

# 可以使用如下代码来生成token
def crt_token(username,password):
    # 定义jwt的过期时间。前一个是获取当前时间
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    # 定义jwt的payload，这里可以存储一些必要的用户信息或者其他验证信息
    # 例如用户ID、用户名、权限、角色等等
    user = User.query.filter_by(username=username).first()
    if user:
        userid = user.id
    payload = {
        # 'id': userid,  # 在数据库查
        'username': username,
        'password': password,
        'iat': datetime.datetime.utcnow(),
        # 'iat'是一个JWT (ISONWeb Tokens)中的标准声明，表示"issued at"，即生成token的时间。
        # 这个时间戳可以用来验证token的有效期，以及防止token被重放攻击。
        # iat,是使用`daterime dateiome.utcnow()函救生成的，表示当前的UTC时间。这个时间戳会被加入到JWT的负载信息中，作为token的一个声明，用于验证token是否合法。
        'exp': expire
    }
    # 调用jwt encode方法生成token.测试成功
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # token生成，返回前端
    return token
    # 其中，payload是一个字典，用于存储一些必要的用户信息或者其他验证信息。iat字段表示jwt的签发时间，exp字段表示jwt的过期时间。算法使用HS256可以保证加密安全性。
    # 最后得到的token可以发送给客户端，并在后续的请求中作为身份验证凭据传递。在服务端接收到请求时，可以使用jwt.decode方法对token进行解码和验证，判断token是否合法和过期。
    # payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

# 鉴权
def authorized_user(token):  # 校验token的函数
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("username")
        # print(username)
        with app.app_context():
            name = User.query.filter(User.username == username).first() # 获取用户名
        if name:    # 用户存在
            # print(payload)
            return payload  # 返回id，username，password等
    except Exception as e:
        return False






# # 检查用户是否已登录
#     Authorization = request.headers.get('Authorization')
#     # 未登录
#     if not Authorization:
#         return jsonify({'message': '未提供token，请先登录！', "code": 408})
#     try:
#     # 已登录
#         payload = jwt.decode(Authorization, SECRET_KEY, algorithms=["HS256"])
#         print(payload)
#     except Exception :
#         return jsonify({'message': 'JWT签名检验失败！', "code": 410})  # token检验失败
#
#     # 解码
#     payload = util.authorized_user(Authorization)  # return payload
#     print(payload)# 返回id，username，password等
#
#     if not payload:
#         return jsonify({'message': 'token检验失败(用户不存在)！',"code":409}) # token检验失败
