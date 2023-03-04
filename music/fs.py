from init import db,User
import hashlib,random,string
import jwt
                    # 《databse》
#==============================================================#

# 增-用户信息增加到数据库
def a(dic: dict, type: str):
    if type == 'Users':
        info = User(id=dic['id'], username=dic['name'], password=hash(dic['psw'])) # 密码用哈希加密
        db.session.add(info)  # 能成功添加到数据库
        db.session.commit()
#==============================================================#
# 用来将密码用哈希算法加密的算法
def hash(s: str):
    # 随机生成长度为4的盐值
    salt = "".join([random.choice(string.ascii_lowercase) for i in range(4)])

    # 拼接原始密码和盐值
    s = s + salt

    # 对加入盐值的字符串加密
    _md5 = hashlib.md5()
    _md5.update(s.encode("utf-8"))
    return salt + "$" + _md5.hexdigest()    # 返回 盐值+哈希值 的字符串

# JWT鉴权的函数：验证token  # (看不懂)
def authorized_user(data):
    try:
        token = data["token"]
        input_username = data["username"]
        payload = jwt.decode(token,'123456', algorithms=['HS256'])  # 不确定
        username: str = payload.get("sub")
        print(username)
        if username == input_username:
            return suc(data)
    except Exception as e:
        print(e)
        return jsonify(fail())    # 失败
#==============================================================#
                    # 《back》
#==============================================================#
# 成功
def suc():  # 无data
    return {"code": 200,"message": "success"}
def suc(data:dict): # 有data
    return {"code": 200,"message": "success","data":data}
# 失败
def fail(msg:str):
    return {"code":404, "msg":msg}
def fail():
    return {"code":403, "msg":"无法检验token"}  # 专门为获取数据准备
#==============================================================#
# 注册-成功
def regi_suc(id,username):
    return {"id": id,"username": username}
# 登录-成功
def lgin_suc(id,username,token):
    return {"id": id,"username":username,"token":token}
# 搜索-成功,获取-成功
def mk_dic(name, art, alb, dur, rid):   # make_dic
    return {"name":name,"artist":art, "album":alb, "duration":dur, "rid":rid}
# 歌曲收藏
def fav_dic(song:dict,fav): #fav是后来修改的，所以单独拎出来
    return {"id":song['id'],"rid":song['rid'],"name":song['name'],'fav':fav}
#==============================================================#
regi_fail="注册失败"    # 注册-错误
lgin_fail="登录失败"    # 登录-失败
sear_fail="搜索失败"    # 搜索-失败
dnld_fail="下载失败"
#==============================================================#
                    # <polish_str>
# 用户信息
def regi_info(id, username, password):
    return {'id':id,'username':username,'password':password}
def music_info(cnt, rid, name, mus_url, art, alb, dur, isFee):
    return {'cnt':cnt,'rid':rid,'name':name,'mus_url':mus_url,'art':art,'alb':alb,'dur':dur,'isFee':isFee}