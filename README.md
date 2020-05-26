# covid19_be

official back-end repo

## 项目运行方法

先决条件：安装Django框架，Python 3.x，django-cors-headers，djangorestframework，validators。

### 安装方法

```bash
#Windows:
pip3 install django              #django安装命令
pip3 install django-cors-headers #django-cors-headers安装命令
pip3 install djangorestframework #django rest framework安装命令
pip3 install validators          #validators安装命令

#Mac(未尝试):
sudo easy_install pip            #安装pip（如果已安装可跳过）
pip3 install django              #django安装命令
pip3 install django-cors-headers #django-cors-headers安装命令
pip3 install djangorestframework #django rest framework安装命令
pip3 install validators          #validators安装命令
```

### 运行方法

```bash
covid19_be>$ python3 manage.py runserver <端口名># 后端目前使用端口8001
```

随后访问`http://localhost:<端口名>`即可。<br>
建议前端在无痕模式下启动npm。

## 附近疫情

### 路径

covid19_be/nearby

### 完成进度

已完成。

前后端联调基本完成。存在一些玄学错误（地图信息红点有时不显示）。

### 调用方法

例如：经纬坐标为`(30.05,120.66)`（前端事先调用高德地图API得知该地点位于绍兴市，城市代码为330600）的用户查询附近疫情时，前端输入的URL为

```
/nearby/?lat=30.05&lon=120.66&citycode=330600
```

后端返回一个json字符串：

```json
{
    "mapCenter": {"longitude": 120.66, "latitude": 30.05}, 
    "address": "绍兴市", 
    "markers": [
        {
            "position": {"longitude": 120.988632, "latitude": 30.154519}, 
            "title": "南岭新村"
        },
        {
            "position": {"longitude": 120.994444, "latitude": 30.148293}, 
            "title": "板桥西路"
        }, 
        {
            "position": {"longitude": 120.379159, "latitude": 30.284556}, 
            "title": "宋都·晨光国际"
        }, 
        {
            "position": {"longitude": 120.389487, "latitude": 30.300031},
            "title": "朗诗·国际街区"
        }, 
        {
            "position": {"longitude": 120.31792, "latitude": 30.295629},
            "title": "七格小区"
        }, 
        {
            "position": {"longitude": 121.130834, "latitude": 30.048196}, 
            "title": "锦绣家园(二高路)"
        },
        {
            "position": {"longitude": 121.147633, "latitude": 30.026232}, 
            "title": "伊顿国际城"
        }, 
        {
            "position": {"longitude": 121.133954, "latitude": 30.178446}, 
            "title": "平王社区"
        }, 
        {
            "position": {"longitude": 121.10753, "latitude": 30.245701},
            "title": "建五村"
        },
        {
            "position": {"longitude": 120.814055, "latitude": 30.468319},
            "title": "三友村"
        }
    ], 
    "city": "绍兴市",
    "totalCase": "42", 
    "currentCase": "0", 
    "nearDis": 33.68,
    "nearLoc": "南岭新村",
    "case1": 0,
    "case3": 0, 
    "case5": 0
}
```

其中每个字段的含义见附近疫情API文档：

https://mubu.com/doc/506MXg39K3t

### marker数量修改方法

在covid19_be/nearby/views.py中，第41行数定义变量`markersNum`，目前值为10。修改该变量的值可以控制前端显示marker的数量。

## 新浪API

### 文档

https://share.mubu.com/doc/2kTqfaDApY7

https://share.mubu.com/doc/2YKmJ6mXsh7

## 注册登录

### 路径

covid19_be/login

### 完成进度

后端RESTful接口的注册登录部分已写好。前后端联调已完成。

修改密码和邮件验证（注册、重置密码）的接口已写好。下一步准备前后端联调。

注册登录部分的测试已完成。

### 调用方法

#### 登录

URL：http://localhost:8001/user/login/

http方法：POST

目前前端fakeAccountLogin函数采用的是通过POST传递json参数。设登录时输入的用户名和密码分别为admin和ant.design，则前端发送的json参数为：

```json
{
    "userName":"admin",                 
    "password":"ant.design",
    "type":"account"
}
```

前端接收的返回值同样为json格式，当登录成功时，内容如下：

```json
{
    "status":"ok",                      /*状态有ok和error两种，对应登录成功与登录失败。*/
    "type":"",                          /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为account*/
    "currentAuthority":"user"/"admin"   /*当前用户权限，（似乎）分为user,admin,guest三种。*/
}
```

其中currentAuthority猜测与权限有关。

#### 注册

URL：http://localhost:8001/user/register/

http方法：POST

前端需要提供json格式的参数，格式如下：

```json
{
    "username":"",           /*用户名*/
    "password1":"",          /*密码*/
    "password2":"",          /*重复密码，两个密码不一致返回注册失败*/
    "email":"",              /*邮箱，一个邮箱只能注册一个账号（后期可加入邮箱验证功能）*/
    "authority":"",          /*用户权限（目前根据前端代码，分为admin和user两种权限）*/
}
```

**注意：**注册时提供的密码**不能为空**。

后端返回的json参数为：

```json
{
    "status":"ok/error",     /*状态有ok和error两种，对应注册成功与注册失败*/
    "type":"",               /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为register*/
}
```

后端会生成一个验证码，并向该账号绑定的邮箱发送一封包含验证链接的邮件。用户点击链接后即可完成验证。

#### 登出

URL：http://localhost:8001/user/logout/

http方法：POST

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

后端返回的json参数格式为：

```json
{
    "status":"ok/error",     /*状态有ok和error两种，对应登出成功与登出失败*/
    "type":"",               /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为logout*/
}
```

#### 修改密码

URL：http://localhost:8001/user/change/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "oldpsw":"",		/*该用户现有密码，用来验证身份*/
    "newpsw":"",		/*修改后的新密码*/
}
```

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

**注意：**修改密码时提供的新密码**不能为空**。

后端返回的json参数格式为：

```json
{
    "status":"ok/error",     /*状态有ok和error两种，对应修改成功与修改失败*/
    "type":"",               /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为changePassword*/
}
```

#### 忘记密码

URL：http://localhost:8001/user/reset/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "username":"",		/*重置密码的账号用户名*/
}
```

后端返回的json参数格式为：

```json
{
    "status":"ok/error",	/*状态有ok和error两种，对应重置成功与重置失败*/
    "type":"",			    /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为resetPassword*/
}
```

后端会将该账号的密码重置为随机值，并向该账号绑定的邮箱发送一封包含随机密码的邮件。

## 地区订阅/生成周报

### 路径

covid19_be/login

### 完成进度

后端RESTful接口的添加订阅、查看订阅、删除订阅接口已写好。下一步准备前后端联调。

### 相关文件地址

地区代码文件：covid19_be/login/data/AMap_adcode.csv

### 调用方法

#### 查看订阅

URL：http://localhost:8001/user/subscribe/get/

http方法：GET

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

后端返回的json参数为：

```json
{
    "status":"ok/error",                /*当状态为error时无content字段*/
    "type":"",                          /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为subscribe*/
    "content":[{"name":"","adcode":"",}]/*返回订阅地区列表，字段分别为名称和地区代码*/
}
```

#### 修改订阅

URL：http://localhost:8001/user/subscribe/post/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "content":["110101",]/*该用户新的订阅地区代码列表*/
}
```

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

后端返回的json参数为：

```json
{
    "status":"ok/error",                /*当状态为error时无content字段*/
    "type":"",                          /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为subscribe*/
    "content":[{"name":"","adcode":"",}]/*返回订阅地区列表，字段分别为名称和地区代码*/
}
```

#### 添加订阅（该接口暂时关闭）

URL：http://localhost:8001/user/subscribe/add/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "content":["110101",]/*添加的订阅地区代码列表*/
}
```

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

后端返回的json参数为：

```json
{
    "status":"ok/error",                /*当状态为error时无content字段*/
    "type":"",                          /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为subscribe*/
    "content":[{"name":"","adcode":"",}]/*返回添加后的订阅地区列表，字段分别为名称和地区代码*/
}
```

#### 删除订阅（该接口暂时关闭）

URL：http://localhost:8001/user/subscribe/delete/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "isClear":"True/False",/*isClear=True时表示清空该用户的订阅列表*/
    "content":["110101",]  /*删除的订阅地区代码列表，如果isClear=True的话无意义*/
}
```

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

后端返回的json参数为：

```json
{
    "status":"ok/error",                /*当状态为error时无content字段*/
    "type":"",                          /*当状态为error时，type字段显示错误信息；当状态为ok时，type字段为subscribe*/
    "content":[{"name":"","adcode":"",}]/*返回删除后的订阅地区列表，字段分别为名称和地区代码*/
}
```

#### 生成周报

URL：http://localhost:8001/user/weekly/get/

http方法：GET

前端在调用该接口时，用户应当处于登录状态，并将用户登录时的cookies传给后端。

后端返回的json参数按照前端要求编写，此处省略。