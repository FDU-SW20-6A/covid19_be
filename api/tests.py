from django.test import TestCase, Client
from . import models
import unittest, json

# Create your tests here.

class APITest(TestCase):

    def test_sina_api(self):
        resp = self.client.get('/api/sina_api/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
    
    def test_province(self):
        resp = self.client.get("/api/province/?province='zhejiang'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json",encoding='utf-8'))
        pro = 'zhejiang'
        pro_num = 0
        for i in range(len(data['data']['list'])):
            if data['data']['list'][i]['name']==pro or data['data']['list'][i]['ename']==pro:
                pro_num = i
        data = data['data']['list'][pro_num]
        self.assertEqual(code, 200)   
        self.assertEqual(content['value'], data['value'])
    
    def test_province_error(self):
        resp = self.client.get("/api/province/?province='jiangzhe'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(code, 200)   
        self.assertEqual(content, {})
    
    def test_country(self):
        resp = self.client.get("/api/country/?code='SCUS0001'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/country/SCUS0001.json",encoding='utf-8'))
        self.assertEqual(code, 200) 
        self.assertEqual(content, data)
    
    def test_country_error(self):
        resp = self.client.get("/api/country/?code='********'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(code, 200) 
        self.assertEqual(content, {})
    
    def test_overall_China(self):
        resp = self.client.get('/api/overall_China/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))      
        self.assertEqual(code, 200)
        self.assertEqual(content['gntotal'], int(data['data']['gntotal']))
        self.assertEqual(content['addcon'], int(data['data']['add_daily']['addcon'])) 
        
    def test_overall_world(self):
        resp = self.client.get('/api/overall_world/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))
        data = data['data']['othertotal']
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
        
    def test_province_list(self): 
        resp = self.client.get('/api/province_list/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))
        dic = data['data']['list']
        for i in range(len(dic)):
            dic[i].pop('city')
            dic[i].pop('hejian')
        self.assertEqual(code, 200)
        self.assertEqual(content, dic)

    def test_country_list(self):
        resp = self.client.get('/api/country_list/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))
        dic = data['data']['otherlist']
        for i in range(len(dic)):
            dic[i].pop('is_show_entrance')
            dic[i].pop('is_show_map')
        self.assertEqual(code, 200)
        self.assertEqual(content, dic)
    
    def test_history(self):
        resp = self.client.get('/api/history/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))
        data = data['data']['historylist']
        dic = []
        n = len(data)
        for i in range(n-1,-1,-1):
            dic.append(data[i]['cn_conadd'])
        self.assertEqual(code, 200) 
        self.assertEqual(content['conadd'], dic)
    
    def test_rate(self):
        resp = self.client.get('/api/rate/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/sina.json", encoding='utf-8'))
        data = data['data']['list']
        dic = {}
        dic['name'] = data[0]['name']
        dic['ename'] = data[0]['ename']
        x = 100.0*float(data[0]['cureNum'])/float(data[0]['value'])
        dic['cureRate'] = format(x,'.2f')
        x = 100.0*float(data[0]['deathNum'])/float(data[0]['value'])
        dic['deathRate'] = format(x,'.2f')     
        self.assertEqual(code, 200) 
        self.assertEqual(content[0], dic)
        
    def test_continent(self):
        resp = self.client.get('/api/continent/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/continent_list.json",encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
    
    def test_scatter_diagram(self):
        resp = self.client.get('/api/scatter_diagram/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/scatter_diagram.json", encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
    
    def test_news(self):
        resp = self.client.get('/api/news/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/news.json", encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
    
    def test_rumor0(self):
        resp = self.client.get('/api/rumor0/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/rumor0.json", encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
        
    def test_rumor2(self):
        resp = self.client.get('/api/rumor2/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/rumor2.json", encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
    
    def test_rumor(self):
        resp = self.client.get('/api/rumor/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/rumor.json", encoding='utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, data)
           
    def test_countries_history(self):
        resp = self.client.get('/api/countries_history/')
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/country/SCUS0001.json",encoding='utf-8'))
        data = data['data']['historylist']
        dic = []
        n = len(data)
        for i in range(n-1,-1,-1):
            dic.append(data[i]['conadd'])
        self.assertEqual(code, 200)
        self.assertEqual(content['USA']['conadd'], dic) 

    def test_country_history(self):
        resp = self.client.get("/api/country_history/?code='SCUS0001'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/country/SCUS0001.json",encoding='utf-8'))
        data = data['data']['historylist']
        dic = []
        n = len(data)
        for i in range(n-1,-1,-1):
            dic.append(data[i]['conadd'])
        self.assertEqual(code, 200) 
        self.assertEqual(content['conadd'], dic)
        
    def test_country_history_error(self):
        resp = self.client.get("/api/country_history/?code='********'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(code, 200) 
        self.assertEqual(content, {})
    
    def test_province_history(self):  
        resp = self.client.get("/api/province_history/?name='浙江'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        data = json.load(open("data/province/zhejiang.json",encoding='utf-8'))
        data = data['timeline'] 
        dic = []
        n = len(data)
        for a,b in data['cases'].items():
            dic.append(data['cases'][a])
        self.assertEqual(code, 200)
        self.assertEqual(content['conNum'], dic)
    
    def test_province_history_error(self):  
        resp = self.client.get("/api/province_history/?name='江浙'")
        code = resp.status_code
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(code, 200)
        self.assertEqual(content, {})
    
    