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
# music
import prettytable as pt # 取别名
import fs,requests

from werkzeug.security import check_password_hash

'''
python 是引用传递
'''

userr = Blueprint('userr', __name__)

# 登录
@userr.route('/user/login',methods=['GET','POST'])
# @app.route('/user/login',methods=['GET','POST'],endpoint='a')
# endpoint，别名，如果不写的话
# 【用来redirect(url_for(a))】
def login( ):
    # return '登录'   # HttpResponse
    # 直接返回一个字符串'登录'
    # 这相当于 'HttpResponse('登录')
    # 浏览器将会显示出"登录”这个文本;
    # return render_template('login.html')  # render

    # if request.method == 'GET':
    #     return redirect("http://localhost:5173/#/login")
    # 正常访问网址时就打开界面，前端界面
    # 不确定

    # data = request.get_json()
    '''问题1：获取的是表单数据，而不是get_json，大家都用get_json，我不知道这俩啥区别具体咋搞'''

    # post表单数据时，处理数据，以下是处理数据
    info = request.form  # 获取表单数据
    get_username = info.get('username')
    get_password = info.get('password') # 拿到的是password不是hash_password
    # fs.get_form(info,get_username,get_password,'')
    hash_password = fs.hash(get_password)    # 将get到的密码hash处理
    # print('-TEST-GET获取到的用户名和密码如下:',end='')
    # print(fs.show_uandp(get_username, get_password))  # 检查是否正确得到用户名和密码
    # print('-TEST-the type of username is:',end='')
    # print(type(username))

    # print(get_hash_password)
    # print()

    # 因为把username设置为了主键，所以这里可以直接查到信息
    user = User.query.get(get_username) # 在数据库中查找username，以及对应id
    '''
    问题3：是否可以查到信息。为什么查不到呢，明明username是主键
        解答：
            查得到。查不到可能有以下几个原因：
        <1> 数据库未保存
        <2> 未将其设置为主键
    '''
    # print('-TEST-User.query.get("admin")是',end='')
    # print(user)

    if(user==None): # 查询是否存在用户信息（username）
        return jsonify(fs.fail404("用户信息不存在,请注册！"))
    else:   # 用户信息存在
        store_id=user.id    # 查询到的id

        # login = user.check_password_hash(get_password)  # 通过hash校验密码
        # print(login)

        store_password=user.hash_password

        # print(get_hash_password)  # 正常
        # print(store_password)

        # 不用存token
        # 用封装好的函数生成token
        token = myjwt.crt_token(get_username, user.hash_password)
        user.token=token    # 存token
        db.session.commit()

        # （TEST）数据库中的
        # print(fs.show_iuandp(store_id, get_username, store_password))  # 检查是否正确得到用户名和密码,数据库中的
        if myjwt.ckpwd(store_password,hash_password): # 判断这俩家伙是否相等
            return jsonify(fs.suc(fs.lgin_suc(store_id, user.username, token)))  # 成功    链接数据库
        else:   # 密码哈希值不正确
            # print(store_password)                                                                                                                                                                                          print(get_hash_password)
            return jsonify(fs.fail404("密码错误"))

# 注册 test 成功
@userr.route('/user', methods=['POST'])
def register():
    # if request.method == 'GET':
    #     return redirect("http://localhost:5173/#/login")
    # 正常访问网址时就打开界面，前端界面

    # post表单数据时，处理数据，以下是处理数据
    info = request.form  # 获取表单数据
    get_username = info.get('username')
    # print(get_username)#test
    get_password = info.get('password')  # 注意拿到的是password不是hash_password!不要写错了
    get_checkPassword=info.get('checkPassword')
    # print(get_username,get_password,get_checkPassword)    # 正确获得

    with app.app_context():  # 任何与数据库有关的操作都要在数据库app的下面
        user = User.query.get(get_username)# 在数据库中查找username
        # print(user)#test
        if (user != None):  # 查询是否存在用户信息（username）
            return jsonify(fs.fail404("用户名已存在,请重新注册！"))
#         # 用户信息可以注册
#         # 问题4：密码长度和密码是否相同前端已经确认了，这里需要再次确认吗？
        if(get_password!=get_checkPassword):
            return jsonify(fs.fail404("两次密码输入不同,请重新注册！"))

        # 数据库处理
        hash_password=fs.hash(get_password)
        # print(fs.hash(str(123456)))   # 123456的哈希
        # 密码合理
        mysql.add_user(get_username,hash_password)  # 增添一条信息，密码用哈希处理

        # 问题6：自增的id不知道能不能直接获得
        user = User.query.get(get_username)  # 在数据库中查找username，以及对应id
        # User.query.filter_by(username=get_username).all()
        store_id = user.id  # 查询到的id

        return fs.suc(fs.regi_suc(store_id,get_username))
        # return redirect(url_for('login'))
#     return "redirect"



# # 登录
# @userr.route('/user/login',methods=['GET','POST'])
# def login( ):
#     if request.method == 'GET':
#         return redirect("http://localhost:5173/#/login")
#     info = request.form
#     get_username = info.get('username')
#     get_password = info.get('password')
#     get_hash_password = fs.hash(get_password)
#     user = User.query.get(get_username)
#     if(user==None):
#         return jsonify(fs.fail404("用户信息不存在,请注册！"))
#     else:
#         store_id=user.id
#         store_password=user.hash_password
#         token = myjwt.crt_token(get_username, user.hash_password)
#         user.token=token
#         if myjwt.ckpwd(store_password,get_hash_password):
#             return jsonify(fs.suc(fs.lgin_suc(store_id, user.username, token)))
#         else:
#             return jsonify(fs.fail404("密码错误"))
