from django.test import TestCase,Client
from django.core import mail
from .models import User,Region
from .views import hash_code,dictFail,dictFailLogin
import unittest,json

def createUser(
    name='testname',
    psw='testpsw',
    email='testname@test.com',
    auth='user',
    hasConf=True
    ):
    User.objects.create(name=name,password=hash_code(psw),email=email,authority=auth,has_confirmed=hasConf)

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
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,respdata)
        self.assertEqual(mail.outbox[0].from_email,'covid19_mailapi@qq.com')
        self.assertEqual(mail.outbox[0].to,['xhs7700@126.com'])
        self.assertEqual(mail.outbox[0].subject,'Registration Confirm: xhs7700')
        #print(mail.outbox[0].from_email,mail.outbox[0].subject,mail.outbox[0].body,mail.outbox[0].to,mail.outbox[0].alternatives)

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
