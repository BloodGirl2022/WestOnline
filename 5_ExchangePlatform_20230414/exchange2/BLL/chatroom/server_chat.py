import threading
import time
import wx
from socket import socket, AF_INET, SOCK_STREAM

class MsbServer(wx.Frame):
    def __init__(self):
        # 创建面板
        # 调用父类的初始化参数
        wx.Frame.__init__(self,None,id=101,title='我的服务器',pos=wx.DefaultPosition,size=(450,470))# 副窗口none，窗口编号，窗口标题,size窗口宽*长
        # 放内容之前放面板
        pl = wx.Panel(self) # 在窗口中初始化一个面板

        # 创建容器
        # 在面板中放按钮、文本框，文本输入框等，把这些对象统一放入容器（box）
        box=wx.BoxSizer(wx.VERTICAL) # 在盒子里面垂直方向自动排版

        # 创建两个按钮
        start_button = wx.Button(pl, size=(133, 40), label="启动")
        record_save_button = wx.Button(pl, size=(133, 40), label="聊天记录保存")
        stop_button = wx.Button(pl, size=(133, 40), label="停止")
        grid1=wx.FlexGridSizer(wx.HORIZONTAL)   # 可伸缩，水平方向网格布局
        grid1.Add(start_button, 0, wx.TOP | wx.LEFT, border=10)  # 设置proportion为0
        grid1.Add(record_save_button, 0, wx.TOP | wx.RIGHT, border=10)  # 设置proportion为0
        grid1.Add(stop_button, 0, wx.TOP | wx.RIGHT, border=10)  # 设置proportion为0
        box.Add(grid1, 0, wx.ALIGN_CENTRE)  # 设置proportion为0

        # 创建只读文本框，显示聊天记录
        self.text = wx.TextCtrl(pl, style=wx.TE_MULTILINE | wx.HSCROLL)
        box.Add(self.text, 1, wx.EXPAND | wx.ALL,border=10)

        pl.SetSizer(box) # 将box放置
        '''以上代码窗口结束'''

        '''服务器准备执行的一些属性'''
        self.isOn = False # 是否后台进行服务
        self.host_port = ("LAPTOP-LBRMLUQR", 443) # 服务器的ip和端设置
        self.server_socket = socket(AF_INET,SOCK_STREAM) # 服务器的socket
        self.server_socket.bind(self.host_port) # 给服务器给ip和端名字
        self.server_socket.listen(5) # 最大进程数量
        self.session_thread_map={} # 存放所有的服务器回话线程

        '''给所有按钮绑定相应的动作'''
        self.Bind(wx.EVT_BUTTON, self.start_server, start_button)   # EVT啥意思
        self.Bind(wx.EVT_BUTTON, self.save_record, record_save_button)  # EVT啥意思

    def start_server(self,event):
        # print("后台服务器启动")    # 成功
        self.show_server_status("后台服务器启动")
        if not self.isOn:
            # 启动服务器主线程
            self.isOn = True    # 后台服务器后台进行服务
            main_thread=threading.Thread(target=self.do_work)
            main_thread.daemon=True # 主线程
            main_thread.start()
            # print("后台服务器进行服务")

    def do_work(self):
        # print("后台服务器开始工作\n")
        self.show_server_status("后台服务器开始工作")
        while self.isOn:
            # 接收客户端名字
            session_socket,client_addr = self.server_socket.accept()
            # 服务首先接受客户端发过来的第一条消息，我们规定第―条消息为客户端的名字
            # print("客户端名字：",session_socket)
            username = session_socket.recv(1024).decode('utf-8')  # 接收客户端名字
            # 创建一个会话线程
            session_thread=Session_thread(session_socket,username,self)
            self.session_thread_map[username]=session_thread  # 创建后台程序，处理客户端名字
            session_thread.start()
            # 服务器欢迎
            self.show_send_client("服务器通知", "欢迎%s进入聊天室! "%username,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

        self.server_socket.close()

    # 在文本中显示聊天信息，并且发送消息给所有客户端
    def show_send_client(self, source, data, data_time):# source信息源，data信息，datatime发送时间
        send_data = '%s : %s\n时间: %s\n'%(source,data,data_time)
        self.text.AppendText( ' ---------------------------\n%s' % send_data)# 在服务器文本框显示信息
        for client in self.session_thread_map.values():
            if client.isOn:# 当前客户端是否活动
                client.client_socket.send(send_data.encode('utf-8'))# 反馈给所有客户端

    # 和上面函数差不多，显示服务器状态
    def show_server_status(self, str):
        # self.text.AppendText( ' ---------------------------\n')# 地服务器文本框是否消息
        self.text.AppendText(str+'\n')  # 地服务器文本框是否消息

    # 保存聊天记录
    def save_record(self,event):
        record=self.text.GetValue()
        with open("save_record/record.log",'w+', encoding='utf-8') as f:# 文件写
            f.write(record)

class Session_thread(threading.Thread):
    def __init__(self,client_socket,username,server):
        threading.Thread.__init__(self)
        self.client_socket=client_socket
        self.username=username
        self.server=server
        self.isOn=True  # 会话线程是否启动

    def run(self):  # 会话线程运行
        print('客户端%s,已经和服务器连接成功，服务器启动一个会话线程' % self.username)
        while self.isOn:
            try:
                data=self.client_socket.recv(1024).decode('utf-8')# 接受客户端的聊天信息
                if not data:# 如果接受到的数据为空，表示连接关闭
                    break
                if data=='A^disconnect^B':#如来客户端点击断开按钮，先发一条消息给服务器:消息的内容我们规定: Adisconnect^B
                    self.isOn=False
                    # 有人离开，通知其他(可删除)
                    self.server.show_send_client("服务器通知", "%s离开聊天室! " %self.username,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

                else:
                    # 其他聊天信息，显示给所有客户端，包括服务器
                    self.server.show_send_client(self.username,data,time.strftime('%Y-%m-%d %H:M:S',time.localtime()))
            except ConnectionError:
                break
        self.client_socket.close()    # 保护客户端会话的socket关掉

# if __name__ == '__main__':
#     app = wx.App()
#     MsbServer().Show()
#     app.MainLoop()