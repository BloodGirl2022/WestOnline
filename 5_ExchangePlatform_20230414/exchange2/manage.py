import sys
sys.path.append('/path/to/exchange2')
from BLL.login.user import user
from BLL.merchandise.merchandise import merchandise
from BLL.chatroom.chatroom import chat_
# from pay import pay
import weakref
from DAL.mysql import app
from flask_socketio import SocketIO


'''
界面层（User Interface layer）
业务逻辑层（Business Logic Layer）
数据访问层（Data access layer）
'''
# ==============================================================#
# 创建一个Flask应用实例对象
# 其中`_name_`是当前模块的名称，用于Flask 知道应该在哪里查找静态文件和模板文件等。
# app = Flask(__name__)
app_ref = weakref.ref(app)
app.register_blueprint(user)  # 注册蓝图
app.register_blueprint(merchandise)
# app.register_blueprint(sms)
app.register_blueprint(chat_)
# app.register_blueprint(pay)
# ==============================================================#
socketio = SocketIO(app)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)#

    # 启动Web服务器
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
    '''问题2：为什么要用0.0.0.0？'''
    # 要放在最后呀！放在前面会报错
    # 启动Web服务器。
    # 其中 'host参数指定服务器监听的地址，默认为`127.0.0.1，即只能本机访问。
    # 这里使用'0.0.0.0"让服务器监听所有的网络接口
    # ==============================================================#

