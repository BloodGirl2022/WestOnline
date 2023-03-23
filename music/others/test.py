from flask import request
from mysql import db,Music,app
# from

# data = request.get_json()  # 不知道什么json。应该是body里的
# type = data.get('type')
# id = data.get('id')     # type为0时根据\id删除
# list = data.get('list') # type为1时删除id为list中的所有数字
# print(data)
# print(type)
# print(id)
# print(list)

type=0
id=10
list=[2,3]

if type==0: # type为0时根据id删除
    # print(Music.query.filter(Music.id==id))
    with app.app_context():
        music = Music.query.filter(Music.id==id)
        print(music)
        db.session.delete(music[0])
        db.session.commit()
elif type==1:
    for i in list:
        db.session.delete(Music.objects.filter(id=i))
        db.session.commit()

