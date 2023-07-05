# # 导入所需的库
# import requests
# import json
# from flask import Flask, request,Blueprint
#
# pay = Blueprint('pay', __name__)
#
# # 支付宝登录部分代码
# @pay.route('/pay/login', methods=['POST'])
# def login():
#     # 获取用户名和密码
#     username = request.get_json().get('username')
#     password = request.get_json().get('password')
#
#     # 在此处进行登录验证
#     # 如果验证失败，则返回错误信息
#     if not verify_login(username, password):
#         return '登录失败', 401
#
#     # 登录成功后返回用户信息
#     return get_user_info(username)
#
# # 支付宝扫描二维码付款部分代码
# @pay.route('/paying', methods=['POST'])
# def paying():
#     # 获取付款参数
#     qrcode_url = request.form.get('qrcode_url')
#     amount = request.form.get('amount')
#
#     # 调用支付宝 API 进行付款操作
#     result = do_pay(qrcode_url, amount)
#     # result=1
#     # 返回付款结果
#     return result
#
# # 验证登录信息的函数
# def verify_login(username, password):
#     # 构造请求头和请求体
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#     data = {
#         'account': username,
#         'password': password
#     }
#
#     # 发送 POST 请求，进行登录验证
#     response = requests.post('https://authsrv.alipay.com/login/enterprise.htm', headers=headers, data=data)
#
#     # 判断登录是否成功
#     if 'my' in response.url:
#         return True
#     else:
#         return False
#
# # 获取用户信息的函数
# def get_user_info(username):
#     # 构造请求头和请求体
#     headers = {
#         'Content-Type': 'application/json',
#         'Referer': 'https://my.alipay.com/portal/i.htm' # 支付宝
#     }
#     data = {
#         'params': json.dumps({
#             '_input_charset': 'utf-8',
#             'service': 'userUserBaseInfo',
#             'userId': username
#         })
#     }
#
#     # 发送 POST 请求，获取用户信息
#     response = requests.post('https://mbillexprod.alipay.com/enterprise/service.do', headers=headers, data=data)
#
#     # 解析返回结果，提取所需信息
#     info = json.loads(response.text)['userBaseInfo']
#     result = {
#         'username': info['realName'],
#         'mobile': info['mobile']
#     }
#
#     # 返回用户信息的 JSON 格式字符串
#     return json.dumps(result, ensure_ascii=False)
#
# # 调用支付宝 API 进行付款的函数
# def do_pay(qrcode_url, amount):
#     # 从二维码 URL 中提取订单号
#     order_no = qrcode_url.split('?')[1].split('&')[0].split('=')[1]
#
#     # 构造请求体
#     data = {
#         'outTradeNo': order_no,
#         'transAmount': amount,
#         'productCode': 'QUICK_MSECURITY_PAY'
#     }
#
#     # 构造请求头
#     headers = {
#         'Content-Type': 'application/json;charset=UTF-8',
#         'Referer': 'https://render.alipay.com/p/f/fd-j6lzqrgm/guiderofmklvtvw.html?scene=offlinePaymentNewSns',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0'
#     }
#
#     # 发送 POST 请求，生成付款二维码
#     response = requests.post('https://qr.alipay.com/gateway.do', headers=headers, json=data)
#
#     # 解析返回结果，提取所需信息
#     qr_code_url = json.loads(response.text)['qrCode']
#
#     # 返回付款结果的 JSON 格式字符串
#     return json.dumps({
#         'result': 'success',
#         'qr_code_url': qr_code_url
#     }, ensure_ascii=False)