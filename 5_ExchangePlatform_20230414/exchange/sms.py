from flask import request,Flask
import sys
sys.path.append('/path/to/PyJWT')
import random
from qcloudsms_py import SmsSingleSender,SmsMultiSender
from qcloudsms_py.httpclient import HTTPError
from pyngrok import ngrok

sms = Flask(__name__)

# 参考 https://www.jianshu.com/p/d18ced9d0682
# 参考 https://cloud.tencent.com/document/product/382/11672 腾讯云文档
# 准备工作：pip install qcloudsms_py 下载讯云提供的SDK

class Captcha():
    # 以下设置变量是按照腾讯云文档指导设置
    # 短信应用 SDK AppID
    appid = 1400836303 # SDK AppID 以1400开头
    # 短信应用 SDK AppKey
    appkey = 'c10f0cc531864332fda786e427ad56aa'
    # 短信模板ID，需要在短信控制台中申请
    template_id = 1854941
    # 签名，# 短信模板ID，需要在短信控制台中申请
    sms_sign = '小棋说三坊七巷公众号'
    # 短信模板中的参数
    # params是一个消息列表，短信模板里面有几个占位符就需要写几个参数
    params = []

    def create_captcha(self):
        """创建一个6位随机数"""
        captcha = '' # 验证码的创建
        for i in range(6):
            now_number = str(random.randint(0, 9))
            captcha += now_number
        return captcha # 验证码创建完毕 以6位字符返回

    def create_ssender(self):
        """创建单发送对象（我猜意思大概是创建那个发送短信的号码，这个对象）
        与短信服务提供商的API进行交互，通过提供有效的 appid 和 appkey 进行身份验证，并提供发送短信的功能
        """
        ssender = SmsSingleSender(self.appid, self.appkey)
        return ssender
    def create_msender(self):
        """创建多发送对象（我猜意思大概是创建那个发送短信的号码，这个对象）
        与短信服务提供商的API进行交互，通过提供有效的 appid 和 appkey 进行身份验证，并提供发送短信的功能
        """
        msender = SmsMultiSender(self.appid, self.appkey)
        return msender

    def send_single_message(self, phone_number):
        """利用发送对象发送短信"""
        ssender = self.create_ssender() # 创建对象
        captcha = self.create_captcha() # 创建验证码
        self.params.append(captcha) # 我的模板里只有1个验证码占位
        try:
            result = ssender.send_with_param(86,    # 指定目标手机号码的国际区号，所以只能给国内手机发送
                                             phone_number,  # 发送给phone_numbers
                                             self.template_id,  # 模板
                                             self.params,   # 模板参数
                                             sign=self.sms_sign,    # 签名
                                             extend="", # 在发送短信时传递额外的信息或标识。通常用于自定义业务需求，例如指定特定的回调URL、记录日志等
                                             ext="") # 一个扩展字段，通常用于传递额外的参数或标识。
            return result['result']
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

    def send_multi_message(self, phone_numbers):
        """利用发送对象发送短信"""
        msender = self.create_msender() # 创建对象
        captcha = self.create_captcha() # 创建验证码
        self.params.append(captcha) # 我的模板里只有1个验证码占位
        try:
            result = msender.send_with_param(86,    # 指定目标手机号码的国际区号，所以只能给国内手机发送
                                             phone_numbers,  # 发送给phone_numbers
                                             self.template_id,  # 模板
                                             self.params,   # 模板参数
                                             sign=self.sms_sign,    # 签名
                                             extend="", # 在发送短信时传递额外的信息或标识。通常用于自定义业务需求，例如指定特定的回调URL、记录日志等
                                             ext="") # 一个扩展字段，通常用于传递额外的参数或标识。
            return result['result']
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

# 测试失败
@sms.route('/sms/callback', methods=['POST'])
def handle_sms_callback():
    # 接收回调数据
    data = request.get_json()
    # 返回响应
    return data

# 测试失败
@sms.route('/sms/response_callback', methods=['POST'])
def handle_sms_response_callback():
    # 接收回调回复数据
    data = request.get_json()
    # 返回响应
    return data

me0='18705056717'
# mei='18705056367'
# hyk='18663114530'
# lyy='18959064470'
# yz0='18750164753'
zyb_new='19835522962'
# cyh='13067243943'
# gy0='13685030068'
# cp='13696840957'
# hxj = 13599050395

if __name__ == '__main__':
    # 验证码登录
    captcha = Captcha()

    # 群发测试
    # phone_numbers =[me0,mei,hyk,lyy,yz0,cyh,gy0]   # 填入您的手机号码
    # captcha.send_multi_message(phone_numbers)

    # 单发测试
    captcha.send_single_message(zyb_new)

    # phone_number = me0
    # captcha.send_single_message(phone_number)

    sms.run()

'''
1. SDK是什么？
SDK是软件开发工具包（Software Development Kit）的缩写
2. API是什么
API是后台服务器端后台的接口
3. captcha是什么意思？
（Completely Automated Public Turing test to tell Computers and Humans Apart）
表示验证码
'''