# # async异步函数是一种特殊的函数，允许在执行过程中暂停，并允许其他任务执行，而不会阻塞整个程序的执行
# # 异步函数内部可以包含 await 关键字，用于暂停函数的执行，等待异步操作的完成。
# # 异步函数可以在执行过程中暂停，并允许事件循环（Event Loop）处理其他任务。
import threading
from socket import socket, AF_INET, SOCK_STREAM
import wx

# 客户端面板
class MsbClient(wx.Frame):
    def __init__(self,c_name):# cname客户端名字，比如张三李四，是客户自己规定的
        # 创建面板
        # 调用父类的初始化参数
        wx.Frame.__init__(self,None,id=101,title='%s的客户端界面'%c_name,pos=wx.DefaultPosition,size=(400,470))# 副窗口none，窗口编号，窗口标题,size窗口宽*长
        # 放内容之前放面板
        pl = wx.Panel(self) # 在窗口中初始化一个面板

        # 创建容器
        # 在面板中放按钮、文本框，文本输入框等，把这些对象统一放入容器（box）
        box=wx.BoxSizer(wx.VERTICAL) # 在盒子里面垂直方向自动排版

        # 创建两个按钮
        conn_button = wx.Button(pl, size=(200, 40), label="连接")
        dis_conn_button = wx.Button(pl, size=(200, 40), label="断开")
        grid1=wx.FlexGridSizer(wx.HORIZONTAL)   # 可伸缩，水平方向网格布局
        grid1.Add(conn_button,1,wx.TOP|wx.LEFT) # 链接按钮在左边
        grid1.Add(dis_conn_button, 1, wx.TOP | wx.RIGHT)  # 断开按钮在右边 1是啥意思 1是比例
        box.Add(grid1,1,wx.ALIGN_CENTRE) #居中对齐

        # 创建聊天内容的文本框，不能写消息
        # MULTI——多行，READ只读
        self.text=wx.TextCtrl(pl,size=(400,250),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.text,1,wx.ALIGN_CENTRE)

        # 聊天输入框,可写
        self.input_text =wx.TextCtrl(pl,size=(400,100),style=wx.TE_MULTILINE)
        box.Add(self.input_text,1,wx.ALIGN_CENTRE)

        # 发送和重置按钮
        clear_button = wx.Button(pl, size=(200, 40), label="重置")
        send_button = wx.Button(pl, size=(200, 40), label="发送")
        grid2 = wx.FlexGridSizer(wx.HORIZONTAL)  # 可伸缩，水平方向网格布局
        grid2.Add(clear_button, 1, wx.TOP | wx.LEFT)  # 链钮在左边
        grid2.Add(send_button, 1, wx.TOP | wx.RIGHT)  # 按钮在右边 1是啥意思 1是比例
        box.Add(grid2, 1, wx.ALIGN_CENTRE)  # 居中对齐

        pl.SetSizer(box)
        '''以上代码完成客户端界面（窗口）'''

        '''给所有按钮绑定点击事件'''
        # conn_button.Bind(wx.EVT_BUTTON, self.connect_to_server)
        self.Bind(wx.EVT_BUTTON, self.connect_to_server,conn_button)    # 链接
        self.Bind(wx.EVT_BUTTON, self.send_to_server, send_button)# 发送
        self.Bind(wx.EVT_BUTTON, self.go_out, dis_conn_button)# 发送
        self.Bind(wx.EVT_BUTTON, self.reset, clear_button)# 发送
        '''客户端的属性'''

        self.name=c_name
        self.isConnected=False# 客户端是否链接服务器

    def connect_to_server(self,event):
        print("客户端%s开始连接服务器"%self.name)
        if not self.isConnected:
            server_host_port = ("LAPTOP-LBRMLUQR", 443)
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(server_host_port)
            # 客户端只要链接成功，马上把自己的名字发送给服务器
            self.client_socket.send(self.name.encode("UTF-8"))
            t = threading.Thread(target=self.receive_data)
            t.daemon=True
            self.isConnected=True
            t.start()

    # 客户端发送消息到
    def send_to_server(self,event):
        if self.isConnected:
            info=self.input_text.GetValue()
            if info !='':
                self.client_socket.send(info.encode("UTF-8"))
                # 输入框发送后设置未空
                self.input_text.Clear()
                # self.input_text.Setvalue("")#或者

    # 离开聊天室
    def go_out(self,event):
        if self.isConnected:
            self.client_socket.send('A^disconnect^B'.encode('utf-8'))
            self.isConnected=False

    # 接受聊天室的数据
    def receive_data(self):
        while self.isConnected:
            data = self.client_socket.recv(1024).decode('utf-8')
            self.text.AppendText(data+'\n')

    def reset(self,event):
        self.input_text.Clear()

# if __name__=='__main__':
#     app=wx.App()
#     name=input('客户端名字：')
#     MsbClient(name).Show()
#     app.MainLoop()# 循环刷新显示
'''
1、可以有多个客广端,每个客广端部有自己名字（唯)
3、服务器只有一个，服务单独的十线程启动利管狎服务器。
4、在服务器中如果一个客户端迁接成功之后，开启一个新的线程和当前客户端会话。
5、客户端和服务器端都有界面
首先从客户端开始
1、开发客户端的界面:使用wxpython开发UI。
2、开发了服务器端的界面，初始化一些属性
3、当服务器启动之后，如果客户端连接，则雷要创建对应会话线程
4、客户端来连接服务器
5、服务在收到客户端连接之后，需要在文本框中显示提示信息
6、发送消息

'''

