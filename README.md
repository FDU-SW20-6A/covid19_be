# covid19_be

official back-end repo

## 项目运行方法

先决条件：安装Django框架，Python 3.x

```bash
covid19_be>$ python manage.py runserver
```

随后访问`127.0.0.1:8000`即可。

## 附近疫情

### 路径

covid19_be/nearby

### 完成进度

基本完成，下一步加入调用新浪API，实现返回当地疫情数据功能。

已完成。下一步准备前后端联调。

可能存在的问题：所在地为直辖市时返回直辖市信息还是市辖区信息

### 调用方法

例如：经纬坐标为`(30.05,120.66)`（前端事先调用高德地图API得知该地点位于绍兴市，城市代码为330600）的用户查询附近疫情时，前端输入的URL为

```
/api/nearby?lat=30.05&lon=120.66&citycode=330600
```

后端返回一个json字符串：

```json
{"cityName": "绍兴市", "cityTotalNum": "42", "cityExistNum": "0", "isOversea": 0, "minDist": 33.68, "location": "南岭新村", "num1": 0, "num3": 0, "num5": 0}
```

其中每个字段的含义如下：

| 字段         | 含义                |
| ------------ | ------------------- |
| cityName     | 所在城市名称        |
| cityTotalNum | 总计确诊病例数      |
| cityExistNum | 现存确诊病例数      |
| isOversea    | 是否包含境外输入    |
| minDist      | 到最近疫情点的距离  |
| location     | 最近疫情点的名称    |
| num1         | 方圆1km内疫情点数目 |
| num2         | 方圆3km内疫情点数目 |
| num3         | 方圆5km内疫情点数目 |

## 新浪API

### 文档

https://share.mubu.com/doc/2kTqfaDApY7

