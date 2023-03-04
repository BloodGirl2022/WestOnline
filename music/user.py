import fs
from init import app,User

# 其他
id=1
# 注册 test 成功
@app.route('/user', methods=['GET','POST'])
def add():
    try:# 检查主键是否存在以及输入是否有误
        # 获取前端传来的数据

        # 1.发送请求 返回响应
        # Request Method: GET  所以request后为get

        # username = st.text_input("请输入用户名:")
        # pwd = st.text_input("请输入密码", type='password')

        # # ============================================================== #
        # MIDDLEWARE = [
        #     'django.middleware.security.SecurityMiddleware',
        #     'django.contrib.sessions.middleware.SessionMiddleware',
        #     'django.middleware.common.CommonMiddleware',
        #     # 'django.middleware.csrf.CsrfViewMiddleware',
        #     'django.contrib.auth.middleware.AuthenticationMiddleware',
        #     'django.contrib.messages.middleware.MessageMiddleware',
        #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
        #     'drfdemo.cors.CORSMiddleware',    # 文件路径
        # ]
        #
        # # 表示所有的ip 都能访问
        # ALLOWED_HOSTS = ['*',]
        # # ============================================================== #

        # resp = requests.get(url=vue_url)
        # username = request
        # getData = request.args.to_dict()  # 利用request对象获取GET请求数据
        # print(getData)
        # return render_template('http://localhost:5173/#/login')
        # print(render_template('http://localhost:5173/#/login'))
        # resp.encoding = 'utf-8'
        # register_json = request.get_json()  # 获取json数据
        # print(register_json)

        # print(resp.request.body)
        # print(username)
        # print(resp.text)
        # html_json=resp.json()   # 返回的response
        # print(html_json)  # test

        # data = request.args
        # print(data)
        # data=data['body']
        # print(data)
        # user_dic = {'id': 1, 'name': 'hehe', 'psw': 'www'}
        # a(user_dic, 'Users')
        # url = url_stt + "/sear/all"
        # return redirect(url)  # 页面跳转
        username = ''
        password = ''
        '''对接失败，无法找到注册时提交的表单。这里先用空字符串替代'''
        # 传到数据库
        fs.a(fs.regi_info(id,username,password),'User')
        id+=1
        # 返回
        return jsonify(fs.regi_suc(id,username))

    except Exception as e:
        print(e)
        return jsonify(fs.fail(fs.regi_fail))

# 登录 test 成功
@app.route('/user/login', methods=['GET','POST'])
def add():
    '''对接失败，无法找到注册时提交的表单。这里先用空字符串替代'''
    # 假设从前端得到密码password
    password=''
    try:
        User.query.get(id)
        if(fs.hash(password)==id.password):
            return  jsonify(fs.suc())
        else:
            print("账号密码不符！")
            return jsonify(fs.fail(fs.lgin_fail))
    except Exception as e:
        print(e)
        return jsonify(fs.fail(fs.lgin_fail))