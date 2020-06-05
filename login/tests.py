from django.test import TestCase,Client
from django.core import mail
from .models import User,Region
from .views import hash_code,dictFail,dictFailLogin,postContent
import unittest,json,csv

def createUser(name='testname',psw='testpsw',email='testname@test.com',auth='user',hasConf=True):
    user=User(name=name,password=hash_code(psw),email=email,authority=auth,has_confirmed=hasConf)
    user.save()
    return user

def getSubBytesContent(content):
    regionList=[]
    for adcode in content:
        region=Region.objects.get(adcode=adcode)
        regionList.append({'name':region.name,'adcode':region.adcode})
    data={
        'status':'ok',
        'type':'subscribe',
        'content':regionList,
    }
    jsonstr=bytes(json.dumps(data),encoding='utf-8').decode('unicode_escape')
    return bytes(jsonstr,encoding='utf-8')

def getSubBytesUser(user):
    regionsList=[{'name':x.name,'adcode':x.adcode} for x in user.regions.all()]
    #print(regionsList)
    data={
        'status':'ok',
        'type':'subscribe',
        'content':regionsList,
    }
    jsonstr=bytes(json.dumps(data),encoding='utf-8').decode('unicode_escape')
    return bytes(jsonstr,encoding='utf-8')

def createRegionBase():
    fp=open(r'login/data/AMap_adcode.csv','r',encoding='gbk',errors='ignore')
    dictReader=csv.DictReader(fp)
    for row in dictReader:
        #name=bytes(row['中文名'],encoding='utf-8')
        Region.objects.get_or_create(
            name=row['中文名'],
            adcode=row['adcode']
        )

def getUser(username):
    try:
        user=User.objects.get(name=username)
    except:
        return None
    return user

def dictFailBytes(s):
    data=bytes(json.dumps(dictFail(s)),encoding='utf-8')
    return data

def dictFailLoginBytes(s):
    data=bytes(json.dumps(dictFailLogin(s)),encoding='utf-8')
    return data

def loginInput(name,psw):
    return {'userName':name,'password':psw}

def loginPost(self,data):
    return self.client.post(path='/user/login/',data=data,content_type='application/json')

def regInput(name,psw1,psw2,email,auth):
    return {
        'username':name,
        'password1':psw1,
        'password2':psw2,
        'email':email,
        'authority':auth,
    }

def regPost(self,data):
    return self.client.post(path='/user/register/',data=data,content_type='application/json')

def chpswInput(oldpsw,newpsw):
    return {'oldpsw':oldpsw,'newpsw':newpsw}

def chpswPost(self,data):
    return self.client.post(path='/user/change/',data=data,content_type='application/json')

def resetInput(name):
    return {'username':name}

def resetPost(self,data):
    return self.client.post(path='/user/reset/',data=data,content_type='application/json')

def postSubInput(content):
    return {'content':content}

def postSubPost(self,data):
    return self.client.post(path='/user/subscribe/post/',data=data,content_type='application/json')

class LoginTest(TestCase):
    def setUp(self):
        createUser()
        createUser('test1','testpsw','test1@test.com','user',False)
        self.client=Client()

    def testNormal(self):
        data=loginInput('testname','testpsw')
        resp=loginPost(self,data)
        self.assertEqual(resp.status_code,200)
        respdata=bytes(json.dumps({"status":"ok","type":"account","currentAuthority":"user"}),encoding='utf-8')
        self.assertEqual(resp.content,respdata)

    def testRelogin(self):
        data=loginInput('testname','testpsw')
        loginPost(self,data)
        resp=loginPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailLoginBytes('Already logined.'))

    def testGetMethod(self):
        data=loginInput('testname','testpsw')
        resp=self.client.get('/user/login/',data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailLoginBytes('Request method is not POST.'))

    def testNotConfirmed(self):
        data=loginInput('test1','testpsw')
        resp=loginPost(self,data)
        msg='This account named test1 has not accomplished email confirmation.'
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailLoginBytes(msg))

    def testUserNotExist(self):
        data=loginInput('xhs7700','123456')
        resp=loginPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailLoginBytes('Username not existed.'))

    def testWrongPsw(self):
        data=loginInput('testname','wrongpsw')
        resp=loginPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailLoginBytes('Wrong password. Username: testname'))

class RegisterTest(TestCase):
    def setUp(self):
        createUser()
        self.client=Client()

    def testNormal(self):
        data=regInput('xhs7700','123456','123456','xhs7700@126.com','user')
        resp=regPost(self,data)
        respdata=bytes(json.dumps({'status':'ok','type':'register'}),encoding='utf-8')
        email=mail.outbox[0]
        #print(mail.outbox[0].from_email,mail.outbox[0].subject,mail.outbox[0].body,mail.outbox[0].to,mail.outbox[0].alternatives)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,respdata)
        self.assertEqual(email.from_email,'covid19_mailapi@qq.com')
        self.assertEqual(email.to,['xhs7700@126.com'])
        self.assertEqual(email.subject,'Registration Confirm: xhs7700')

    def testAlreadyLogin(self):
        logindata=loginInput('testname','testpsw')
        loginPost(self,logindata)
        regdata=regInput('xhs7700','123456','123456','xhs7700@126.com','user')
        resp=regPost(self,regdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Already logined.'))

    def testGetMethod(self):
        data=regInput('xhs7700','123456','123456','xhs7700@126.com','user')
        resp=self.client.get('/user/register/',data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Request method is not POST.'))

    def testWrongPsw(self):
        data=regInput('xhs7700','123456','12346','xhs7700@126.com','user')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Two password input do not match.\nusername:xhs7700\npassword1:123456\npassword2:12346'))

    def testNullPsw(self):
        data=regInput('xhs7700','','','xhs7700@126.com','user')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Password cannot be null.'))

    def testSameName(self):
        data=regInput('testname','123456','123456','xhs7700@126.com','user')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes("Username 'testname' already existed."))

    def testSameEmail(self):
        data=regInput('xhs7700','123456','123456','testname@test.com','user')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('The email address \'testname@test.com\' has been used.'))

    def testInvalidAuth(self):
        data=regInput('xhs7700','123456','123456','xhs7700@126.com','asdf')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Invalid authority.'))

    def testNullName(self):
        data=regInput('','123456','123456','xhs7700@126.com','user')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Username cannot be null.'))

    def testInvalidEmail(self):
        data=regInput('xhs7700','123456','123456','oiasf','user')
        resp=regPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Invalid email address.'))

class LogoutTest(TestCase):
    def setUp(self):
        createUser()
        self.client=Client()

    def testNormal(self):
        data=loginInput('testname','testpsw')
        loginPost(self,data)
        resp=self.client.post('/user/logout/')
        respdata=bytes(json.dumps({'status':'ok','type':'logout'}),encoding='utf-8')
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,respdata)

    def testAlreadyLogout(self):
        resp=self.client.post('/user/logout/')
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Already logouted.'))

class ChangePasswordTest(TestCase):
    def setUp(self):
        createUser('xhs7700','123456','xhs7700@126.com')
        self.client=Client()

    def testNotLogin(self):
        data=chpswInput('123456','12345')
        resp=chpswPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Already logouted.'))

    def testWrongPsw(self):
        logindata=loginInput('xhs7700','123456')
        chpswdata=chpswInput('12345','1234567')
        loginPost(self,logindata)
        resp=chpswPost(self,chpswdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Wrong Password.'))

    def testGetMethod(self):
        logindata=loginInput('xhs7700','123456')
        chpswdata=chpswInput('123456','1234567')
        loginPost(self,logindata)
        resp=self.client.get('/user/change/',chpswdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Request method is not POST.'))

    def testNullPsw(self):
        logindata=loginInput('xhs7700','123456')
        chpswdata=chpswInput('123456','')
        loginPost(self,logindata)
        resp=chpswPost(self,chpswdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Invalid new password.'))

    def testNormal(self):
        logindata=loginInput('xhs7700','123456')
        chpswdata=chpswInput('123456','1234567')
        loginPost(self,logindata)
        resp=chpswPost(self,chpswdata)
        respdata=bytes(json.dumps({'status':'ok','type':'changePassword'}),encoding='utf-8')
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,respdata)

class ResetPasswordTest(TestCase):
    def setUp(self):
        createUser('xhs7700','123456','xhs7700@126.com')
        self.client=Client()

    def testNormal(self):
        data=resetInput('xhs7700')
        resp=resetPost(self,data)
        respdata=bytes(json.dumps({'status':'ok','type':'resetPassword'}),encoding='utf-8')
        email=mail.outbox[0]
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,respdata)
        #print(email.from_email,email.to,email.subject,email.alternatives,email.body)
        self.assertEqual(email.from_email,'covid19_mailapi@qq.com')
        self.assertEqual(email.to,['xhs7700@126.com'])
        self.assertEqual(email.subject,'Reset Password: xhs7700')

    def testGetMethod(self):
        data=resetInput('xhs7700')
        resp=self.client.get('/user/reset/',data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Request method is not POST.'))

    def testNameNotExist(self):
        data=resetInput('hsxia18')
        resp=resetPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Username hsxia18 not existed.'))

    def testNotConfirmed(self):
        createUser('hsxia18','123456','hsxia18@fudan.edu.cn','user',False)
        data=resetInput('hsxia18')
        resp=resetPost(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('This account named hsxia18 has not accomplished email confirmation.'))

class GetSubTest(TestCase):
    def setUp(self):
        createRegionBase()
        user=createUser('xhs7700','123456','xhs7700@126.com')
        self.client=Client()
        content=['310109','320200','510000']
        postContent(user,content)

    def testNormal(self):
        user=getUser('xhs7700')
        data=loginInput('xhs7700','123456')
        loginPost(self,data)
        resp=self.client.get('/user/subscribe/get/')
        self.assertEqual(resp.status_code,200)
        #print(getSubBytesUser(user))
        self.assertEqual(resp.content,getSubBytesUser(user))

    def testAlreadyLogout(self):
        resp=self.client.get('/user/subscribe/get/')
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Already logouted.'))

class PostSubTest(TestCase):
    def setUp(self):
        createRegionBase()
        user=createUser('xhs7700','123456','xhs7700@126.com')
        self.client=Client()
        content=['310109','320200','510000']
        postContent(user,content)

    def testNormal(self):
        content=['310110','320300','510000']
        logindata=loginInput('xhs7700','123456')
        postdata=postSubInput(content)
        loginPost(self,logindata)
        resp=postSubPost(self,postdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,getSubBytesContent(content))

    def testAlreadyLogout(self):
        content=['310110','320300','510000']
        postdata=postSubInput(content)
        resp=postSubPost(self,postdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Already logouted.'))

    def testGetMethod(self):
        content=['310110','320300','510000']
        logindata=loginInput('xhs7700','123456')
        postdata=postSubInput(content)
        loginPost(self,logindata)
        resp=self.client.get('/user/subscribe/post/',postdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Request method is not POST.'))

    def testInvalidAdcode(self):
        content=['310110','320300','207419']
        logindata=loginInput('xhs7700','123456')
        postdata=postSubInput(content)
        loginPost(self,logindata)
        resp=postSubPost(self,postdata)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictFailBytes('Adcode not existed.'))

class GetWeeklyTest(TestCase):
    def setUp(self):
        createRegionBase()
        user=createUser('xhs7700','123456','xhs7700@126.com')
        self.client=Client()
        content=['310109','320200','320300','510000','510100']
        postContent(user,content)

    def testNormal(self):
        data=loginInput('xhs7700','123456')
        loginPost(self,data)
        resp=self.client.get('/user/weekly/get/')
        respdata=json.loads(resp.content,encoding='utf-8')
        self.assertEqual(resp.status_code,200)
        self.assertEqual(len(respdata['city']),5)
        self.assertEqual(len(respdata['treeData'].keys()),3)
