'''functions'''
from mysql import db,User,Music
import hashlib,random,string

                    # 《databse》
#==============================================================#
# 增-用户信息增加到数据库
def add_user(name,psw):
    info = User(username=name, password=psw) # 密码已用哈希加密,id自动
    db.session.add(info)  # 能成功添加到数据库
    db.session.commit()

# 增-用户信息增加到音乐库
def add_music(list):
    info = Music(rid=list[0],name=list[1],mus_url=list[2],artist=list[3],album=list[4],duration=list[5],isFee=list[6])
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
#==============================================================#
# # 用来将密码用哈希算法加密的算法
# def hash(s: str):
#     # 随机生成长度为4的盐值
#     salt = "".join([random.choice(string.ascii_lowercase) for i in range(4)])
#     # 拼接原始密码和盐值
#     s = s + salt
#     # 对加入盐值的字符串加密
#     _md5 = hashlib.md5()
#     _md5.update(s.encode("utf-8"))
#     return salt + "$" + _md5.hexdigest()    # 返回 盐值+哈希值 的字符串

# 用来将密码用哈希算法加密的算法
def hash(password:str):
    # 使用SHA-256算法对密码进行哈希，并将结果转换为十六进制字符串。
    hash_obj = hashlib.sha256(password.encode('utf-8'))
    hash_password = hash_obj.hexdigest()
    return hash_password

#==============================================================#
                    # 《back》
#==============================================================#
# 成功
def suc0():  # 无data
    return {"code": 200,"message": "success"}
def suc(data:dict): # 有data
    return {"code": 200,"message": "success","data":data}
# 失败
def fail404(msg):
    return {"code":404, "msg":msg}
def fail403():
    return {"code":403, "msg":"无法检验token"}  # 专门为获取数据准备
#==============================================================#
# 注册-成功
def regi_suc(id,username):
    return {"id": id,"username": username}
# 登录-成功
def lgin_suc(id,username,token):
    return {"id": id,"username":username,"token":token}
# 搜索-成功,获取-成功
def mk_song(name, artist, album, duration, rid):   # make_dic
    return {"name":name,"artist":artist, "album":album, "duration":duration, "rid":rid}
def mk_song2(music):   # make_dic
    return {"name":music.name,"artist":music.artist, "album":music.album, "duration":music.duration, "rid":music.rid}
# 获取历史记录
def mk_history(list):
    return_list=[] # 多首歌的信息
    for i in list:
        dic_list = {}   # 一首歌的信息
        dic_list["name"]=i.name
        dic_list["artist"] = i.artist
        dic_list["album"] = i.album
        dic_list["duration"] = i.duration
        dic_list["rid"] = i.rid
        dic_list["id"] = i.id
        dic_list["fav"]=i.fav

        return_list.append(dic_list)
    # return data{}
    return return_list # 此为data

# 歌曲收藏
def fav_data(song:dict,fav): #fav是后来修改的，所以单独拎出来
    return {"id":song['id'],"rid":song['rid'],"name":song['name'],'fav':fav}
#==============================================================#
regi_fail="注册失败"    # 注册-错误
lgin_fail="登录失败"    # 登录-失败
sear_fail="搜索失败"    # 搜索-失败
dnld_fail="下载失败"
dlt_fail="删除失败"
#==============================================================#
                    # <polish_str>
# 用户信息
def regi_info(id, username, password):
    return {'id':id,'username':username,'password':password}
def music_info(cnt, rid, name, mus_url, art, alb, dur, isFee):
    return {'cnt':cnt,'rid':rid,'name':name,'mus_url':mus_url,'art':art,'alb':alb,'dur':dur,'isFee':isFee}
#==============================================================#
def show_uandp(username, password):    # username and password
    return {'username':username,'password':str(password)}
def show_iuandp(id,username, password):    # id ,username and password
    return {'id':id,'username':username,'hash_password':password}
# def get_form(info:dict,username,password,checkPassword):
#     username=info.get('username')
#     password=info.get('password')
#     if 'checkPassword' in info:
#         checkPassword=info.get('checkPassword') # 注册时第4个参数就随便填
#     return