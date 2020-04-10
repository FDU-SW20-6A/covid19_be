# covid19_be

official back-end repo

## 项目运行方法

先决条件：安装Django框架，Python 3.x，django-cors-headers

```bash
covid19_be>$ python manage.py runserver <端口名># 后端目前使用端口8001
```

随后访问`http://localhost:<端口名>`即可。

## 附近疫情

### 路径

covid19_be/nearby

### 完成进度

基本完成，下一步加入调用新浪API，实现返回当地疫情数据功能。

已完成。下一步准备前后端联调。

前后端联调基本完成。存在一些玄学错误（地图信息红点有时不显示）。

可能存在的分歧：

所在地为直辖市时返回直辖市信息还是市辖区信息。

目前根据前端调用API的逻辑，当用户所在地为直辖市时，前端返回市辖区代码，后端查询市辖区疫情信息；当用户所在地不为直辖市时，前端返回所在区县代码，后端查询其所处地级市疫情信息（数据不够细）。

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

