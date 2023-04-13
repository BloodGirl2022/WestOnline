### 工作进度

* ==用户注册登录==：已完成

  需要编写以下函数：<u>**register()、login()、logout()**，分别用于**用户注册、用户登录、用户登出**。</u>

  

#### 数据库设计

##### 1. users（用户类）

| 列名          | 数据类型     | 是否允许为空 | 中文注释     |
| ------------- | ------------ | ------------ | ------------ |
| id            | int          | NOT NULL     | 用户ID       |
| username      | varchar(15)  | NOT NULL     | 用户名       |
| hash_password | varchar(511) | NULL         | 哈希后的密码 |
| email         | varchar(31)  | NULL         | 邮箱         |
| phone_number  | int          | NULL         | 手机号码     |
| real_name     | varchar(50)  | NULL         | 真实姓名     |
| register_time | datetime     | NOT NULL     | 注册时间     |
| last_time     | datetime     | NOT NULL     | 上次登录时间 |

2. merchandise（商品类）

#### 接口文档示例

用户注册登录接口文档应该包括<u>请求地址、请求参数、响应参数、错误码</u>等信息。例如：

+ 请求地址：/user/register
+ 请求参数：{ "username": "xxx", "password": "xxx", "email": "xxx", "phone": "xxx", "nickname": "xxx", "avatar": "xxx" }
+ 响应参数：{ "code": 200, "msg": "注册成功" }
+ 错误码：{ "4001": "用户名已存在", "4002": "邮箱已被注册", "4003": "手机号已被注册", "5001": "服务器内部错误" }





### 沟通疑问

1. **输入用户密码时要用表单吗？**如果不用，我就要设置header：在 `raw` 格式下，需要手动设置请求头，**告知后端**传递的数据类型，例如：`Content-Type: application/json`。此外，传递的数据需要以指定格式的字符串形式出现在请求体中，例如：`{"name": "John", "age": 30}`。==**记得手动设置请求头**==

   ![image-20230414001723412](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414001723412.png)

   不知道这样行不行

2. **登录成功后要返回哪些数据？**我应该时全都返回了

3. 关于密码长度，前端在输入时就不允许密码长度等不符。后端就不检验了，麻烦

   ![image-20230414003040052](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414003040052.png)

4. 





### 接口测试成功

#### 登录

##### 1. 登录成功

![image-20230414000946831](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414000946831.png)

##### 2. 密码错误

![image-20230414001750723](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414001750723.png)

##### 3. 用户名不存在

![image-20230414002342926](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414002342926.png)

#### 注册

##### 1. 成功

![image-20230414011342888](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414011342888.png)

##### 2.失败-用户名已存在

![image-20230414011554371](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414011554371.png)

##### 3. 两次输入密码不同

![image-20230414011700703](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414011700703.png)

##### 4. 手机号已被注册

![image-20230414012007716](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414012007716.png)

##### 5. 邮箱已被注册

![image-20230414012046125](C:\Users\Hong Langchen\AppData\Roaming\Typora\typora-user-images\image-20230414012046125.png)