# 前言：

采用当今主流的语言加框架加测试报告进行接口测试，其中不足，请大家多多指出并协助更改。 这里非常感谢一位老哥：[https://gitee.com/zy7y](https://gitee.com/zy7y)  QQ:396667207
感谢老哥耐心指教

语雀版：https://www.yuque.com/docs/share/dff93b31-cce0-4a7a-8d06-1540e659c32f?# 《Python-接口自动化(Request+pytest+allure)》

# 功能：

1. get/post请求(上传文件)，支持restful接口规范
1. 压缩测试报告
1. 生成allure漂亮的测试报告
1. 发送邮件(后续会集成jenkins)
1. 数据依赖

# 运行机制

1. 通过读取配置文件，获取到host地址、提取token的jsonpath表达式，提取实际响应结果用来与预期结果对比的jsonpath表达式
1. 读取excel用例文件数据，组成一个符合pytest参数化的用例数据，根据每列数据进行数据处理(token操作、数据依赖)
1. token的写需要使用一个正常的登陆接口，并且接口中要返回token数据，才能提取；token的读需要请求携带有token的header，token无数据将不携带token
1. 数据依赖处理，从excel中读取出来的格式**{"用例编号":["jsonpath表达式1":"jsonpath表达式2"]}**
   ，通过用例编号来获取对应的case的实际响应结果，通过jsonpath表达式提取对应的依赖参数字段，以及对应的值，最终会返回一个存储接口需要依赖数据的字典**{"userid":500,"username":"ranyong"}**
   ,在发送请求时与请求数据进行合并，组成一个新的data放在请求中
1. ~~每次请求完之后将回写实际的响应结果到excel中~~
1. 根据配置文件中配置的jsonpath表达式提取实际响应内容与excel中预期结果的数据对比
1. 生成测试报告
1. 压缩测试报告文件夹
1. 发送邮件

# 环境依赖

| 名称 | 版本 | 作用 |
| --- | --- | --- |
| python | 3.7.8+ | 写代码核心工具 |
| pytest | 6.0.1 | 底层单元测试框架,用来实现参数化，自动执行用例 |
| allure-pytest | 2.8.17 | allure与pytest的插件可以生成allure的测试报告 |
| jsonpath | 0.82 | 用来进行响应断言操作 |
| loguru | 0.54 | 记录日志 |
| PyYAML | 5.3.1 | 读取yml/yaml格式的配置文件 |
| Allure | 2.13.5 | 要生成allure测试报告必须要在本机安装allure并配置环境变量 |
| xlrd | 1.2.0 | 用来读取excel中用例数据 |
| yagmail | 0.11.224 | 测试完成后发送邮件 |
| requests | 2.24.0 | 发送请求 |

# 目录结构

```shell
├─api
│  ├─__init__.py # 初始化	
│  └─base_requests.py	# 请求封装
├─config
│  └─config.yaml	# 配置文件
├─data
│  └─test_data.xls	# Excel用例文件
├─test
│  ├─conftest.py	# 依赖对象初始化
│  └─test_api.py	# 测试文件
├─log
│  └─run...x.log	# 日志文件
├─report
│  ├─data
│  └─html			# allure报告
├─tools		# 工具包
│  ├─__init__.py		# 常用方法封装
│  ├─data_process.py	# 依赖数据处理
│  ├─db.py				# 数据库连接对象
│  ├─hooks.py			# 自定义扩展方法(可配合用例)文件 
│  ├─read_file.py		# 用例、配置项读取
│  └─send_email.py		# 邮件发送、报告压缩
├─requirements.txt		 # 项目依赖库文件
└─run.py	# 主启动文件(一键运行)
```

## 代码实现

首先了解下yaml文件的基础知识
**Yaml文件初识：**
以下为yaml文件的一个示例：

```
student:
    name: chen
    age: 18
    sex: 男
    class: 11
```

转换为json格式时：

```yaml
{
  "student": {
    "name": "chen",
    "age": 18,
    "sex": "男",
    "class": 11
  }
}
```

以上可以看出，yaml的基本写法是比较简单的，注意的是，**同一级的字段要对齐，冒号后面要带上空格。**切记！切记！
**yaml基础语法：**

- 大小写敏感
- 使用缩进表示层级关系
- 缩进不能使用tab，只允许空格
- 缩进的空格数不重要，只要相同层级的元素左对齐即可
- '#'表示注释

详细了解请移步：[https://www.runoob.com/w3cnote/yaml-intro.html](https://www.runoob.com/w3cnote/yaml-intro.html)

## 初始化安装

1. 安装最新的 [Pycharm](https://www.jetbrains.com/pycharm/download) 社区版

1. 安装[Python](https://www.python.org/getit/) ，版本3.7+

1. 安装[allure2](https://github.com/allure-framework/allure2/releases) ，点击链接内的Links---Download，解压到任意目录，并配置好环境变量

1. 安装[git](https://git-scm.com/downloads) ，完成后鼠标右键打开git bash，输入：

1. 找一个目录，打开git
   bash，输入：  `git clone [https://gitee.com/ran_yong/api-auto.git](https://gitee.com/ran_yong/auto_uiautomator2.git) `

1. 打开Pycharm，打开上一步拉取下来的apiAutoTest文件夹，导入工程，点击settings---Project---Project Interpretor---add...---New
   environment---Location中在当前工程名后确认是否有/venv，没有的话手动输入，基本编译器选择python3的安装路径，确认即可

1. Pycharm需要先配置pip的repositories，推荐[https://pypi.tuna.tsinghua.edu.cn/simple/](https://pypi.tuna.tsinghua.edu.cn/simple/)
   ，Pycharm的Terminal中，输入：  `pip3 install -r requirements.txt`  （若下载超时：pip install
   -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple) -r requirements.txt）
   等待安装完成后，环境就配置完成了，后续执行测试只要执行下面的第8步即可

1. 直接运行对应应用目录下的`run.py`即可

# Excel用例展示

| 用例编号 | 用例标题 | Header自定义会被追加到基准header | 接口地址(/&....表示可变路径参数，实际值从响应字典读取) | 是否执行 | 请求方式 | 入参关键字 | 上传文件({文件接受参数对象: 上传文件的路径}) | 请求数据（&语法&，提取前面依赖数据字典中对应key的值） | 后置sql | 预期结果(实际:预期- 其中预期支持请求参数一样的提取语法) | 保存响应(建议在该用例的实际响应结果会被其他用例使用时，才保存) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| case_001 | get请求实现登录 | {"num":"@sum_data(1,2)@"} | login | 是 | get | params |  | {"username": "admin", "password": ""} |  | {"$.meta.status":400} | 是 |
| case_002 | post请求实现登录 |  | login | 是 | post | data |  | {"username": "admin", "password": "123456"} | select * from user where id=&$.case_002.data.id&; | {"$.meta":{ "msg": "登录成功", "status": 200 }} | 是 |
| case_003 | get请求查询用户数据列表 | {"Authorization": "&$.case_002.data.token&"} | users | 是 | get | params |  | {"pagenum": 1, "pagesize": "12", "meta": &$.case_002.meta&, "userId": &$.case_002.data.id&} |  | {"$.meta":{"msg": "获取管理员列表成功", "status": 200}} | 是 |
| case_004 | get请求查询用户数据列表 |  | users | 是 | get | data |  | {"pagenum": 1, "pagesize": "12"} |  | {"$.meta":{"msg": "获取管理员列表成功", "status": 200}} | 是 |
| case_005 | 添加用户正常接口数据 | {"Authorization": "&$.case_002.data.token&"} | users | 是 | post | data |  | {"username": "tery1321131","password": "123456"} |  | {"$.meta":{"msg":"创建成功","status":201}} | 是 |
| case_006 | 修改用户状态接口 | {"Authorization": "&$.case_002.data.token&"} | users/&$.case_005.data.id&/state/&$.case_005.data.careate_time& | 是 | put | data |  |  |  | {"$.meta":{"msg": "设置状态成功", "status": 200}} | 是 |
| case_007 | 修改用户状态为2 | {"Authorization": "&$.case_002.data.token&"} | users/&$.case_005.data.id&/state/2 | 是 | put | data |  |  |  | {"$.meta":{"msg": "设置状态成功", "status": 200}} | 是 |
| case_008 | win10-本地测试上传单文件接口 |  | upload_file/ | 否 | post | data | {"file_excel":"C:\\\\Users\\\\ranyong\\\\Desktop\\\\a.txt"} |  |  | {"$.meta":{"msg": "ok"}} | 是 |
| case_009 | win10-本地测试上传多文件接口 |  | upload_files/ | 否 | post | data | {"files":["C:\\\\Users\\\\ranyong\\\\Desktop\\\\b.jpg", "C:\\\\Users\\\\ranyong\\\\Desktop\\\\c.jpg"]} |  |  | {"$.meta":{"msg": "ok"}} | 是 |
| case_001 | 百度收录查询 | @md5_encode2()@ | api-baidu_entry | 是 | get | params |  | {"url": "abeim.cn"} |  | { "code": 200 } | 是 |

|            | case_data.xlsx部分字段格式说明(解析)                         |
| ---------- | ------------------------------------------------------------ |
| 接口地址   | 这里的接口地址是不加主机地址的，其中若路径中需要其他接口返回的数据写法如下users/&$.case_005.data.id&/state/2 其中 &$.case_005.data.id& 表示从响应结果字典中取到用例编号005的实际响应中的data下面id的值，假设现在实际响应字典内容如下{"case_005": {     "data": {       "id": 511,       "create_time": 1605711095 }, }} 那么上方内容提取的结果就是 511/state/2， 最终的请求地址 基准地址+ users/511/state/2 |
| Header     | {"Authorization": "&$.case_002.data.token&", "num":"@sum_data(1,2)@"} 支持使用自定义函数,其他参数返回内容,来扩展之前的版本的token操作(已移除) |
| 请求方式   | get/post/put/delete/head/options/patch                       |
| 入参关键字 | 1. params：类似这种：url?参数名=参数值&参数名1=参数值1 2. data：请求头content-type是from表单类型。 3. json：请求头content-type：application/json。 |
| 上传文件   | 1. 单个文件上传,实例 windows -- {"file_excel":"C:\\Users\\zy7y\\Desktop\\a.txt"}, file_excel是接口中接受文件内容的参数名称, C:\\Users\\zy7y\\Desktop\\a.txt 文件所在路径， 注意 Windows路径使用 \\ 与Mac不一样 / 2. 多个文件上传windows -- {"files":["C:\\Users\\zy7y\\Desktop\\b.jpg", "C:\\Users\\zy7y\\Desktop\\c.jpg"]} 3. mac 多文件上传: {"files":["/Users/zy7y/Desktop/vue.js","/Users/zy7y/Desktop/jenkins.war"]}, 这里的files是接口中接收文件内容的参数 可查看最开始的用例文档中的：case_009, case_010, case_011 |
| 请求数据   | 语法：&$.case_002.data.id&, 意为从响应字典中提取到用例编号case_002的实际响应中data子字典中的id的值 实例：{"pagenum": 1, "pagesize": "12", "meta": &$.case_002.data.meta&, "userId": &$.case_002.data.id&},其中&$.case_002.data&， &$.case_002.data.id& 代表是动态变量（具体值从实际响应结果字典去取-取其他接口返回的响应中的字段值），假设响应字典内容如下{"case_002": {     "data": {       "id": 500,       "username": "admin",       "mobile": "12345678", }}，则上方内容解析出来之后，最终的请求数据--> {"pagenum": 1, "pagesize": "12", "meta": {       "id": 500,       "username": "admin",       "mobile": "12345678", }, "userId": 500} |
| 后置sql    | 2020/12/08日更新： sql的结果将被写入到响应字典中共同存储 sql中可以使用变量如select * from user where id=&$.case_002.data.id&;/最终的执行的sql如下 select * from user where id = 500;（前提case_002的实际响应结果下的data下的id为500） |
| 预期结果   | 语法格式： {"jsonpath提取语法": 预期结果内容}, 假设登录接口访问后响应如下{"data": {"userId": 21},"meta":{"msg":"成功"}},预期结果栏写入{"$.meta": {"msg":"失败"}},表示，从该接口响应中提取meta下面的内容-提取结果应该是{"msg":"成功"}， 而我们的预期结果是{"msg":"失败"}，故这里会断言失败。多断言实例{"$.data.userId":21,"$.meta": {"msg":"失败"}}其中第一条数据会断言成功，第二条{"msg":"失败"} 会断言失败 预期结果内容可以使用变量的形式如：{"$.data.id":&$.id&}， 这里的&$.id&就是个预期结果，他表示从整个响应字典中取key为id的value（个人认为也算是初步实现了，数据库断言） |

## 查看测试报告

运行run.py完成测试后会自动处理报告并使用默认浏览器打开报告，若关闭后想再次打开，请在pycharm中找到对应报告的目录下的index.html，右击--Open in Browser

# 其他

## base64编码和解码

题外话：将数据加密成密文然后在传出去 此加密不能用字典类型的 需要将类型转换为字节

```python
# 编码数据
import base64
import json

json_data = {
    "tag": "movie",
    "type": "华语"
}

str_json = json.dumps(json_data)

print(type(str_json), str_json)

b_str_json = str_json.encode()
print(type(b_str_json))
# 数据加密
print(base64.b64encode(b_str_json))
```

```python
# 解码数据
import base64
import json

json_data = {
    "tag": "movie",
    "type": "华语"
}

encode_data = b'eyJ0YWciOiAibW92aWUiLCAidHlwZSI6ICJcdTUzNGVcdThiZWQifQ=='

print(base64.b64decode(encode_data))
b_str_json = base64.b64decode(encode_data)  # b'{"tag": "movie", "type": "\\u534e\\u8bed"}'
# 字节类型转换为字符串
str_json = b_str_json.decode()
print(type(str_json), str_json)  # <class 'str'> {"tag": "movie", "type": "\u534e\u8bed"}
print(json.loads(str_json))  # {'tag': 'movie', 'type': '华语'}
```
