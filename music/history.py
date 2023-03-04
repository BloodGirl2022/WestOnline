import fs
from init import app,Music
from flask import request
from init import db

# 获取历史记录(传num用来分页)
@app.route('/user/history:page<nuum>', methods=['GET'])
def get_history(num):
    # JWT
    judge = fs.authorized_user(request.headers.get("Authorization"))
    if not judge:
        return fs.fail()
    #get
    return jsonify(fs.suc(Music.query.all()))   # 按照成功示例返回

# 删除历史记录(看不懂那个删除id和list啥区别呀)
@app.route('/user/history', methods=['GET'])
def dlt_history(num):
    # JWT
    judge = fs.authorized_user(request.headers.get("Authorization"))
    if not judge:
        return fs.fail()
    #get
    id=input()  # 输入id
    db.session.delete(Music.query.get(id))
    db.session.commit()
    return jsonify(fs.suc())   # 按照成功示例返回

# 收藏历史记录(不会写)
@app.route('/user/history', methods=['GET'])
def dlt_history(num):
    # JWT
    judge = fs.authorized_user(request.headers.get("Authorization"))
    if not judge:
        return fs.fail()

    # get-ID
    id=input()  # 输入id
    fav=bool(input())   # 选择收藏或取消
    try:
        song=Music.query.get(id)    # 如果是字典
        song=fs.fav_dic(song,fav)   # song现在是表fav的格式
        db.session.add(song)  # 能成功添加到数据库
        db.session.commit()
        return jsonify(fs.suc(song))
    except:
        return jsonify(fs.suc())   # 按照成功示例返回
