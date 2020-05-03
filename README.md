# covid19_be

official back-end repo

## 项目运行方法

先决条件：安装Django框架，Python 3.x，django-cors-headers

### 安装方法

```bash
#Windows:
pip3 install django              #django安装命令
pip3 install django-cors-headers #django-cors-headers安装命令

#Mac(未尝试):
sudo easy_install pip            #安装pip（如果已安装可跳过）
pip3 install django              #django安装命令
pip3 install django-cors-headers #django-cors-headers安装命令
pip3 install djangorestframework #django rest framework安装命令
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
{"mapCenter": {"longitude": 120.66, "latitude": 30.05}, "address": "绍兴市", "markers": [{"position": {"longitude": 120.988632, "latitude": 30.154519}, "title": "南岭新村"}, {"position": {"longitude": 120.994444, "latitude": 30.148293}, "title": "板桥西路"}, {"position": {"longitude": 120.379159, "latitude": 30.284556}, "title": "宋都·晨光国际"}, {"position": {"longitude": 120.389487, "latitude": 30.300031}, "title": "朗诗·国际街区"}, {"position": {"longitude": 120.31792, "latitude": 30.295629}, "title": "七格小区"}, {"position": {"longitude": 121.130834, "latitude": 30.048196}, "title": "锦绣家园(二高路)"}, {"position": {"longitude": 121.147633, "latitude": 30.026232}, "title": "伊顿国际城"}, {"position": {"longitude": 121.133954, "latitude": 30.178446}, "title": "平王社区"}, {"position": {"longitude": 121.10753, "latitude": 30.245701}, "title": "建五村"}, {"position": {"longitude": 120.814055, "latitude": 30.468319}, "title": "三友村"}], "city": "绍兴市", "totalCase": "42", "currentCase": "0", "nearDis": 33.68, "nearLoc": "南岭新村", "case1": 0, "case3": 0, "case5": 0}
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

后端RESTful接口的注册登录部分已写好。登录部分已完成前后端联调。目前正在等待前端注册部分明确需求。

下一步准备完成修改密码和邮件验证的接口。

### 调用方法

#### 登录部分

URL：http://localhost:8001/user/login/

目前前端fakeAccountLogin函数采用的是通过POST传递json参数。设登录时输入的用户名和密码分别为admin和ant.design，则前端发送的json参数为：

```json
{
    userName:"admin",                 
    password:"ant.design",
    type:"account"
}
```

前端接收的返回值同样为json格式，当登录成功时，内容如下：

```json
{
    status:"ok",                      //状态有ok和error两种，对应登录成功与登录失败。
    type:"account",                   //前端代码中出现的参数，意义不明。
    currentAuthority:"user"/"admin"   //当前用户权限，（似乎）分为user,admin,guest三种。
}
```

其中currentAuthority猜测与权限有关。

#### 注册部分

URL：http://localhost:8001/user/register/

前端需要提供json格式的参数，格式如下：

```json
{
    username:           //用户名
    password1:          //密码
    password2:          //重复密码，两个密码不一致返回注册失败
    email:              //邮箱，一个邮箱只能注册一个账号（后期可加入邮箱验证功能）
    authority:          //用户权限（目前根据前端代码，分为admin和user两种权限）
}
```

后端返回的json参数为：

```json
{
    status:             //状态有ok和error两种，对应注册成功与注册失败
    type:register       //仿照登录部分设置的参数，无具体意义
}
```

