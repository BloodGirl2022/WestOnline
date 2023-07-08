# from flask import Blueprint
# from BLL.chatroom.server_chat import MsbServer
# from BLL.chatroom.client_chat import MsbClient
# from flask import request
# import threading
# from socket import socket, AF_INET, SOCK_STREAM
# import wx
# from flask import jsonify
#
# # 蓝图
# chat_ = Blueprint('chat_', __name__)
#
# # 打开服务器
# @chat_.route('/chat', methods=['POST'])
# def chat():
#     try:
#         info = request.get_json()  # 获取表单数据
#         user1 = info.get('user1')
#         user2 = info.get('user2')
#         print(user1, user2)
#         app = wx.App()
#         MsbServer().Show()
#         # MsbClient(user1).Show()
#         # MsbClient(user2).Show()
#         app.MainLoop()# 循环刷新显示
#         return jsonify(code=200, msg='success', data=None)
#     except Exception as e:
#         return jsonify(code=412, msg='无法获取用户信息或连接失败', data=None)

from flask import Blueprint, request
from flask import current_app as app
from flask import jsonify

# 引入 WebSocket 相关模块
from flask_socketio import SocketIO, emit

# 蓝图
chat_ = Blueprint('chat_', __name__)

# 创建 SocketIO 实例
socketio = SocketIO()

# 定义 WebSocket 事件
@socketio.on('connect', namespace='/chat')
def handle_connect():
    # 当有客户端连接时的处理逻辑
    print('Client connected')
    emit('server_response', {'data': 'Connected'})  # 向客户端发送数据

@socketio.on('disconnect', namespace='/chat')
def handle_disconnect():
    # 当有客户端断开连接时的处理逻辑
    print('Client disconnected')

@chat_.route('/chat', methods=['POST'])
def chat():
    try:
        info = request.get_json()  # 获取表单数据
        user1 = info.get('user1')
        user2 = info.get('user2')
        print(user1, user2)

        # 运行 Flask 应用并启用 SocketIO
        socketio.init_app(app)
        socketio.run(app)

        return jsonify(code=200, msg='success', data=None)
    except Exception as e:
        return jsonify(code=412, msg='无法获取用户信息或连接失败', data=None)
