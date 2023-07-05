from flask import request
import sys
sys.path.append('/path/to/PyJWT')
# import myjwt
from mysql import Music
from mysql import app
from mysql import db
from sqlalchemy import asc
from flask import Blueprint
import fs
import jwt

history = Blueprint('history', __name__)
# 加密key，应该存放在环境变量或者配置文件中，不能明文写在程序中
with open('SECRET_KEY.txt', encoding='utf-8') as file_obj:  # 将秘钥写在配置文件中
    contents = file_obj.read()
SECRET_KEY = contents.rstrip()  # 秘钥

# 删除历史记录
@history.route('/user/history', methods=['DELETE'])
def delete():
    # Authorization = request.headers.get('Authorization')  # 获取
    # if not Authorization:
    #     return fs.fail404("未登录")
    # if not token:
    #     return fs.fail403()  # token检验失败

    data = request.get_json()  # 不知道什么json。应该是body里的
    type = data.get('type')
    id = data.get('id')  # type为0时根据\id删除
    list = data.get('list')  # type为1时删除id为list中的所有数字
    # print(data)
    # print(type)
    # print(id)
    # print(list)
    try:
        if type == 0:  # type为0时根据id删除
            with app.app_context():
                # Working outside of application context
                # 不加上面这句就会疯狂报错，哼！
                try:
                    music = Music.query.filter(Music.id == id)
                    # print(music.first())
                    db.session.delete(music.first())
                    db.session.commit()
                except:
                    pass
        elif type == 1:
            for i in list:
                try:
                    music = Music.query.filter(Music.id == i)
                    db.session.delete(music.first())
                    db.session.commit()
                except:
                    pass  # 此处，查不到id时，说明不存在，报错则忽略
                    # 可查到id时，则正常删除
        return fs.suc0()
    except:
        return fs.fail404(fs.dlt_fail)


# 获取历史记录
@history.route('/user/history', methods=['GET'])
def get_hisroty():
    Authorization = request.headers.get('Authorization')  # 获取
    if not Authorization:
        return fs.fail404("未登录")
    token = myjwt.authorized_user(Authorization)
    if not token:
        return fs.fail403()  # token检验失败

    page = int(request.args.get('page'))  # query请求函数
    per_page = 10  # 每10条获取一次

    # length = Music.query.count()    # 表长度-正常获取
    # start = (page-1)*10+1   # 起始条数
    # end = page*10   # 终止条数

    music_list = Music.query.order_by(asc(Music.id)).paginate(page=page, per_page=per_page)
    count = music_list.pages  # 获取总共的页数

    # 这里使用`paginate()`方法进行分页查询
    # 参数`page`表示要获取的页数
    # `per_page`表示每页显示的记录数
    # `order_by()`方法接收一个按照id属性升序排序的函数，在这里我们使用的是`asc()`方法。

    # 以下是整合数据拼成返回格式
    list = fs.mk_history(music_list)  # list
    data_dic = {"list": list, "count": count}  # data
    return_dic = fs.suc(data_dic)  # return

    # 返回
    return return_dic


# 修改历史记录收藏
@history.route('/user/history/lc', methods=['PUT'])  # lc啥意思？
def lc():
    Authorization = request.headers.get('Authorization')  # 获取
    print(Authorization)
    payload = jwt.decode(Authorization, SECRET_KEY, algorithms=["HS256"])
    print(payload)
    if not Authorization:
        return fs.fail404("未登录")
    token = myjwt.authorized_user(Authorization)    # return payload
    print(token)
    if not token:
        return fs.fail403()  # token检验失败

    data = request.get_json()  # body里的
    fav = data.get('fav')
    id = data.get('id')  # type为0时根据id删除

    music = Music.query.filter(Music.id == id).first()  # 找到信息.因为只有1条，所以取【0】就行（不太会用get）
    music.fav = fav  # 更改
    db.session.commit()  # 保存

    return fs.suc(fs.mk_song2(music))  # 返回