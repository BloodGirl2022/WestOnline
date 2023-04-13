from flask import Flask, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
#==============================================================#
# 创建链接数据库
pymysql.install_as_MySQLdb()
app = Flask(__name__)
#==============================================================#
class Config():
    DEBUG=True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/tdl?charset=utf8" # 手动创建数据库
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config.from_object(Config)
#==============================================================#
# 不太明白上面代码的意思，但不敢动它，一不小心就报错
#==============================================================#

# 链接数据库
db = SQLAlchemy(app)
# 创建表
class TDL(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer,primary_key=True) # 主键
    content = db.Column(db.String(256),nullable=False) # 内容非空
    status = db.Column(db.Enum("否","是"),nullable=False) # 状态默认为未完成
    start = db.Column(db.Integer,nullable=False)
    end = db.Column(db.Integer,nullable=False)
#==============================================================#
url_stt="http://"+"127.0.0.1:5000"  # 前缀 随便取的名字
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
# 函数
# 增
def a(id,ctt,stts,stt,end):
    task = TDL(id=id, content=ctt, status=stts, start=stt, end=end)
    db.session.add(task)  # 能成功添加到数据库
    db.session.commit()
    return task
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
# 查 filter(条件) 条件查询（查状态是否完成）
def s_stts(stts):
    return TDL.query.filter(TDL.status==stts)
# 查 全部
def s_all():
    return TDL.query.all()
# 查 id
def s_id(id):
    return TDL.query.get(id) # 用get
# 查 关键字
def s_key(key):
    return TDL.query.filter(TDL.content.contains(key)).all()    # 查询所有content字段中包含key的
# get(id)查1个 all()查全部
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
# 改
def m(id,stts): # m表示modify,0表示标记为未完成,1表示标记为已完成
    TDL.query.filter(TDL.id==id).update({"status":stts})
    db.session.commit()
def m_all(stts): # m表示modify,0表示标记为未完成
    TDL.query.filter().update({"status":stts})
    db.session.commit()
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
# 删id 成功
def d(id): # d表示delete
    db.session.delete(TDL.query.get(id))
    db.session.commit()
# 删一群
def d_lot(tasks):
    for i in tasks:
        db.session.delete(i)
    db.session.commit()
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
# 把东西转化为json格式（list套dict）
def trans1(tasks):
    list=[]
    for i in tasks:
        dic={"id":i.id,"content":i.content,"status":i.status,"start":i.start,"end":i.end}
        list.append(dic)
    return list
# 把东西转化为json格式（list套dict）
def trans2(i):
    dic={"id":i.id,"content":i.content,"status":i.status,"start":i.start,"end":i.end}
    return dic
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
def judge_stts(stts):
    if stts!="是" and stts!="否":
        return 0
    else:
        return 1
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
def cp (list1):
    dic={"code":200, "msg":"success","data":list1}
    return dic
def cp_f ():
    dic={"code":404, "msg":"该活动不存在"}
    return dic
# ==============================================================#
# 初始化 建库链接库 初始化库
if __name__ == '__main__':
    with app.app_context():  # debug的时候加这句不会错
        db.drop_all()  # 删除所有表
        db.create_all()  # 创建所有表
        db.session.add(TDL(id=1,content="python三轮",status="否",start=20220111,end=20220112))
        db.session.add(TDL(id=2, content="美术三轮", status="是", start=20220111, end=20220112))
        db.session.commit()
# ==============================================================#
# 初始页面
@app.route("/")
def index():
    return 'begin!'
# ==============================================================#
# 增 test 127.0.0.1:5000/add/3/2/是/3/4 成功
@app.route('/add/<id>/<ctt>/<stts>/<stt>/<end>', methods=['POST'])
def add(id,ctt,stts,stt,end):
    try:# 检查主键是否存在以及输入是否有误
        a(id,ctt,stts,stt,end)
        url = url_stt + "/sear/all"
        return redirect(url)  # 页面跳转
        # return jsonify(id=task.id,content=task.content,status=task.status,start=task.start,end=task.end)
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# ==============================================================#
# 查全部 成功
@app.route('/sear/all', methods=['GET','POST'])
def sear_all():
    try:
        return jsonify(cp(trans1(s_all())))# 展示数据库中所有事项
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# 查已完成/未完成 成功
@app.route('/sear/stts/<string:stts>', methods=['GET','POST'])
def sear_stts(stts):
    try:
        return jsonify(cp(trans1(s_stts(stts))))
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# 查id 成功
@app.route('/sear/id/<int:id>', methods=['GET','POST'])
def sear_id(id):
    try:
        return jsonify(cp(trans2(s_id(id))))
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# 查关键字
@app.route('/sear/key/<string:key>', methods=['GET','POST'])
def sear_key(key):
    try:
        return jsonify(cp(trans1(s_key(key))))
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# ==============================================================#
# 改
# 改一条 成功
@app.route('/modi/id/<int:id>/<string:stts>', methods=['POST'])
def modi_id(id, stts):
    if judge_stts(stts):    # 判断状态输入是否正确
        m(id, stts)
        url=url_stt+"/sear/id/"+str(id)
        return redirect(url)  # 页面跳转
        #===================================#
        # 不知道为什么这两句不行，哎，明明在add里可以
        # 诶，好像是因为跳转到该id信息下，信息已被删除所以无法查找
        # 不对这不是删除呀
        # 哦,因为刚刚手动更改了url，这里没改过来
        # return jsonify(cp(trans1(s_all())))  # 展示数据库中所有事项
        #===================================#
    else:
        return jsonify(cp_f())
# 改全部 成功
@app.route('/modi/all/<string:stts>', methods=['POST'])
def modi_all(stts):
    if judge_stts(stts):   # 判断状态输入是否正确
        m_all(stts)
        url=url_stt+"/sear/all"
        return redirect(url) # 跳转成功
    else:
        return jsonify(cp_f())
# ==============================================================#
# 删一条 成功
@app.route('/del/id/<int:id>', methods=['DELETE'])
def del_id(id):
    try:
        d(id)
        # url = url_stt + "/sear/all"
        # return redirect(url)  # 跳转成功
        # ===================================#
        # 不知道为什么这两句不行，哎
        # 405 Method Not Allowed
        # ===================================#
        return jsonify(cp(trans1(s_all())))  # 展示数据库中所有事项
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# 删状态全部 成功
@app.route('/del/stts/<string:stts>', methods=['DELETE'])
def del_stts(stts):
    try:
        if(judge_stts(stts)):  # 判断状态输入是否正确
            tasks = TDL.query.filter(TDL.status == stts)
            d_lot(tasks)
            # url = url_stt + "/sear/all"
            # return redirect(url)  # 跳转成功
            # ===================================#
            # 不知道为什么这两句不行，哎
            # 405 Method Not Allowed
            # ===================================#
            return jsonify(cp(trans1(s_all())))  # 展示数据库中所有事项
    except Exception as e:
        print(e)
        return jsonify(cp_f())
# 删全部 因为库空了会报错 成功
@app.route('/del/all', methods=['DELETE'])
def del_all():
    try:
        tasks = TDL.query.all()
        d_lot(tasks)
        # url = url_stt + "/sear/all"
        # return redirect(url)  # 跳转成功
        # ===================================#
        # 不知道为什么这两句不行，哎
        # 405 Method Not Allowed
        # ===================================#
        return jsonify(cp(trans1(s_all())))  # 展示数据库中所有事项
    except Exception as e:
        print(e)
        return jsonify(cp_f())
#==============================================================#
#                      以上代码成功
app.run(debug=True,port=8001)

#==============================================================#