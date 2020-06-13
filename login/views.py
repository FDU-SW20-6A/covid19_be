from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from . import models
import hashlib,datetime,pytz,json,csv,time,validators
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def dictFail(s):
    return {'status':'error','type':s}

def dictFailLogin(s):
    return {'status':'error','type':s,'currentAuthority':'guest'}

def myJsonResponse(ret):
    json_data=json.dumps(ret,ensure_ascii=False)
    response=HttpResponse(json_data)
    '''
    response['Access-Control-Allow-Origin']='http://127.0.0.1:8000'
    response['Access-Control-Allow-Methods']='POST,GET,OPTIONS'
    response['Access-Control-Max-Age']='2000'
    response['Access-Control-Allow-Headers']='*'
    '''
    return response

def hash_code(s,salt='login_hash'):
    h=hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()

def makeConfirmString(user):
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code=hash_code(user.name,now)
    models.ConfirmString.objects.create(code=code,user=user,)
    return code

def sendRegisterEmail(email,username,code):
    from django.core.mail import EmailMultiAlternatives
    subject='Registration Confirm: {}'.format(username)
    textContent='This is a registration confirmation.'
    htmlContent='<p>Click <a href="http://{}/user/confirm/?code={}" target="blank">this</a> to accomplish the confirmation.</p>'.format('localhost:8001',code,settings.CONFIRM_DAYS)
    msg=EmailMultiAlternatives(subject,textContent,settings.DEFAULT_FROM_EMAIL,[email])
    msg.attach_alternative(htmlContent,'text/html')
    msg.send()

def sendResetEmail(email,username,psw):
    from django.core.mail import EmailMultiAlternatives
    subject='Reset Password: {}'.format(username)
    textContent='This includes a reset password for user {}'.format(username)
    htmlContent='''<p>This includes a reset password for user {}.</p>
    <p>Your temporary password is {}. Please change it after login.'''.format(username,psw)
    msg=EmailMultiAlternatives(subject,textContent,settings.DEFAULT_FROM_EMAIL,[email])
    msg.attach_alternative(htmlContent,'text/html')
    msg.send()

def postContent(user,content):
    regionsSet=set([x for x in user.regions.all()])
    regionsPostSet=set()
    for adcode in content:
        try:
            region=models.Region.objects.get(adcode=adcode)
        except:
            #print(adcode)
            return False
            #return myJsonResponse(dictFail('Adcode {} not existed.'.format(adcode)))
        regionsPostSet.add(region)
    for region in regionsPostSet-regionsSet: user.regions.add(region)
    for region in regionsSet-regionsPostSet: user.regions.remove(region)
    return True

@csrf_exempt
def login(request):
    if request.session.get('is_login',None):
        return myJsonResponse(dictFailLogin('Already logined.'))
    if request.method=='POST':
        data=json.loads(request.body)
        username=data['userName']
        password=data['password']
        try:
            user=models.User.objects.get(name=username)
            if user.has_confirmed==False:
                message='This account named {} has not accomplished email confirmation.'.format(username)
                return myJsonResponse(dictFailLogin(message))
            if user.password==hash_code(password):
                request.session['is_login']=True
                request.session['user_id']=user.id
                request.session['user_name']=user.name
                ret={'status':'ok','type':'account','currentAuthority':user.authority}
                return myJsonResponse(ret)
            else:
                message='Wrong password. Username: {}'.format(username)
                return myJsonResponse(dictFailLogin(message))
        except:
            message='Username not existed.'
            return myJsonResponse(dictFailLogin(message))
    else:
        return myJsonResponse(dictFailLogin('Request method is not POST.'))

@csrf_exempt
def register(request):
    request.session.clear_expired()
    if request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logined.'))
    if request.method=='POST':
        data=json.loads(request.body)
        username=data['username']
        password1=data['password1']
        password2=data['password2']
        authority=data['authority']
        email=data['email']
        if username=='':
            message='Username cannot be null.'
            return myJsonResponse(dictFail(message))
        if not validators.email(email):
            message='Invalid email address.'
            return myJsonResponse(dictFail(message))
        if authority not in {'user','admin'}:
            message='Invalid authority.'
            return myJsonResponse(dictFail(message))
        if password1!=password2:
            message='Two password input do not match.\nusername:{}\npassword1:{}\npassword2:{}'.format(username,password1,password2)
            return myJsonResponse(dictFail(message))
        elif password1=='':
            message='Password cannot be null.'
            return myJsonResponse(dictFail(message))
        else:
            same_name_user=models.User.objects.filter(name=username)
            if same_name_user:
                message='Username \'{}\' already existed.'.format(username)
                return myJsonResponse(dictFail(message))
            else:
                same_email_user=models.User.objects.filter(email=email)
                if same_email_user:
                    message='The email address \'{}\' has been used.'.format(email)
                    return myJsonResponse(dictFail(message))
                else:
                    new_user=models.User.objects.create(
                        name=username,
                        password=hash_code(password1),
                        email=email,
                        authority=authority,
                        has_confirmed=False,
                    )
                    code=makeConfirmString(new_user)
                    sendRegisterEmail(email,username,code)
                    return myJsonResponse({'status':'ok','type':'register'})
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))

@csrf_exempt
def logout(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    request.session.flush()
    return myJsonResponse({'status':'ok','type':'logout'})

def userConfirm(request):
    code=request.GET.get('code',None)
    message=''
    try:
        confirm=models.ConfirmString.objects.get(code=code)
    except:
        message='Invalid confirm request!'
        return render(request,'login/confirm.html',locals())

    created_time=confirm.created_time
    now=datetime.datetime.now()
    now=now.replace(tzinfo=pytz.timezone('UTC'))
    cmp=created_time+datetime.timedelta(settings.CONFIRM_DAYS)
    #print(cmp.tzinfo)
    if now>cmp:
        confirm.user.delete()
        message='Your email expired. Please register again.'
        return render(request,'login/confirm.html',locals())
    else:
        confirm.user.has_confirmed=True
        confirm.user.save()
        confirm.delete()
        message='Successfully confirmed.'
        return render(request,'login/confirm.html',locals())

@csrf_exempt
def getSubscribe(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    username=request.session['user_name']
    try:
        user=models.User.objects.get(name=username)
    except:
        return myJsonResponse(dictFail('User {} not existed.'.format(username)))
    regionsList=[{'name':x.name,'adcode':x.adcode} for x in user.regions.all()]
    return myJsonResponse({
        'status':'ok',
        'type':'subscribe',
        'content':regionsList,
        })

@csrf_exempt
def postSubscribe(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    if request.method=='POST':
        data=json.loads(request.body)
        username=request.session['user_name']
        content=data['content']
        try:
            user=models.User.objects.get(name=username)
        except:
            return myJsonResponse(dictFail('User {} not existed.'.format(username)))
        if not postContent(user,content):
            return myJsonResponse(dictFail('Adcode not existed.'))
        regionsList=[{'name':x.name,'adcode':x.adcode} for x in user.regions.all()]
        return myJsonResponse({
            'status':'ok',
            'type':'subscribe',
            'content':regionsList,
        })
    return myJsonResponse(dictFail('Request method is not POST.'))

@csrf_exempt
def getCurrentUser(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    return myJsonResponse({'status':'ok','username':request.session['user_name']})

def getWeekly(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    username=request.session['user_name']
    #username=request.GET['username']
    try:
        user=models.User.objects.get(name=username)
    except:
        return myJsonResponse(dictFail('User {} not existed.'.format(username)))

    regionsList=[{'name':x.name,'adcode':x.adcode} for x in user.regions.all()]
    cityList=[]
    isProvince={}
    treeData={}
    provfileList={}
    startday=datetime.date(2020,1,19)
    provstr=json.load(open(r'data/provincecode.json','r',errors='ignore'))
    newsdata=json.load(open(r'data/localnews.json','r',encoding='utf-8',errors='ignore'))
    for key in provstr.keys():
        provname=models.Region.objects.get(adcode=key+'0000').name
        provfileList[provname]=[]
    for week in range(13):
        dateList=[]
        day=startday+datetime.timedelta(week*7)
        for i in range(15):
            dx=(day+datetime.timedelta(i)).timetuple()
            ds='{}/{}/{}'.format(dx.tm_mon,dx.tm_mday,str(dx.tm_year)[2:])
            dateList.append(ds)
        lastdate=[(day+datetime.timedelta(i)).strftime('%m.%d')for i in range(1,8)]
        thisdate=[(day+datetime.timedelta(i)).strftime('%m.%d')for i in range(8,15)]

        provfile={}
        conNumList,econNumList,cureNumList,deathNumList,conNumAddList,econNumAddList,cureNumAddList,deathNumAddList=[],[],[],[],[],[],[],[]
        for key,value in provstr.items():
            provname=models.Region.objects.get(adcode=key+'0000').name
            filestr=r'data/province/'+value+r'.json'
            provdata=json.load(open(filestr,'r'))['timeline']
            cases=[provdata['cases'].get(x,0) for x in dateList]
            deaths=[provdata['deaths'].get(x,0) for x in dateList]
            recovered=[provdata['recovered'].get(x,0) for x in dateList]
            newsList=[]
            lastday=day+datetime.timedelta(14)
            for news in newsdata[key]:
                cmpdate=datetime.date.fromtimestamp(eval(news['pubDate'][:-3]))
                if cmpdate>lastday:continue
                newsList.append(news)

            provfile[provname]={
                'city':provname,
                'date':lastday.strftime('%Y-%m-%d'),
                'conNum':cases[-1],
                'econNum':cases[-1]-deaths[-1]-recovered[-1],
                'cureNum':recovered[-1],
                'deathNum':deaths[-1],
                'conNumAdd':cases[-1]-cases[-2],
                'econNumAdd':(cases[-1]-deaths[-1]-recovered[-1])-(cases[-2]-deaths[-2]-recovered[-2]),
                'cureNumAdd':recovered[-1]-recovered[-2],
                'deathNumAdd':deaths[-1]-deaths[-2],
                'Conadd':{
                    'thisweek':[cases[i]-cases[i-1] for i in range(8,15)],
                    'lastweek':[cases[i]-cases[i-1] for i in range(1,8)],
                    'lastdate':lastdate,
                    'thisdate':thisdate
                },
                'ConNum':{
                    'thisweek':[cases[i] for i in range(8,15)],
                    'lastweek':[cases[i] for i in range(1,8)],
                    'lastdate':lastdate,
                    'thisdate':thisdate
                },
                'CureNum':{
                    'thisweek':[recovered[i] for i in range(8,15)],
                    'lastweek':[recovered[i] for i in range(1,8)],
                    'lastdate':lastdate,
                    'thisdate':thisdate
                },
                'DeathNum':{
                    'thisweek':[deaths[i] for i in range(8,15)],
                    'lastweek':[recovered[i] for i in range(1,8)],
                    'lastdate':lastdate,
                    'thisdate':thisdate
                },
                'news':newsList,
            }
            tmp=provfile[provname]
            conNumList.append((provname,tmp['conNum']))
            conNumAddList.append((provname,tmp['conNumAdd']))
            econNumList.append((provname,tmp['econNum']))
            econNumAddList.append((provname,tmp['econNumAdd']))
            cureNumList.append((provname,tmp['cureNum']))
            cureNumAddList.append((provname,tmp['cureNumAdd']))
            deathNumList.append((provname,tmp['deathNum']))
            deathNumAddList.append((provname,tmp['deathNumAdd']))

        conNumList=sorted(conNumList,key=lambda x:-x[1])
        conNumAddList=sorted(conNumAddList,key=lambda x:-x[1])
        econNumList=sorted(econNumList,key=lambda x:-x[1])
        econNumAddList=sorted(econNumAddList,key=lambda x:-x[1])
        cureNumList=sorted(cureNumList,key=lambda x:-x[1])
        cureNumAddList=sorted(cureNumAddList,key=lambda x:-x[1])
        deathNumList=sorted(deathNumList,key=lambda x:-x[1])
        deathNumAddList=sorted(deathNumAddList,key=lambda x:-x[1])

        for i in range(len(conNumList)):
            provname=conNumList[i][0]
            provfile[provname]['conNumRank']=i+1
        for i in range(len(econNumList)):
            provname=econNumList[i][0]
            provfile[provname]['econNumRank']=i+1
        for i in range(len(cureNumList)):
            provname=cureNumList[i][0]
            provfile[provname]['cureNumRank']=i+1
        for i in range(len(deathNumList)):
            provname=deathNumList[i][0]
            provfile[provname]['deathNumRank']=i+1
        for i in range(len(conNumAddList)):
            provname=conNumAddList[i][0]
            provfile[provname]['conNumRankAdd']=i+1
        for i in range(len(econNumAddList)):
            provname=econNumAddList[i][0]
            provfile[provname]['econNumRankAdd']=i+1
        for i in range(len(cureNumAddList)):
            provname=cureNumAddList[i][0]
            provfile[provname]['cureNumRankAdd']=i+1
        for i in range(len(deathNumAddList)):
            provname=deathNumAddList[i][0]
            provfile[provname]['deathNumRankAdd']=i+1

        for key in provstr.keys():
            provname=models.Region.objects.get(adcode=key+'0000').name
            provfileList[provname].append(provfile[provname])

    for region in regionsList:
        adcode=region['adcode']
        provcode=adcode[:2]
        #if adcode[2:]=='0000':continue
        cityList.append(region['name'])
        if isProvince.get(provcode,None):continue
        isProvince[provcode]=1
        provname=models.Region.objects.get(adcode=provcode+'0000').name
        treeData[provname]=provfileList[provname]
    ans={
        'city':cityList,
        'treeData':treeData,
        'history':{},
        'index':'',
        'pages':[],
        'historyPages':[],
        'pagination':1,
    }
    return myJsonResponse(ans)

@csrf_exempt
def changePassword(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    if request.method=='POST':
        data=json.loads(request.body)
        username=request.session['user_name']
        oldpsw,newpsw=data['oldpsw'],data['newpsw']
        if newpsw=='':
            return myJsonResponse(dictFail('Invalid new password.'))
        if newpsw==oldpsw:
            return myJsonResponse(dictFail('New password cannot be the same with old password.'))
        try:
            user=models.User.objects.get(name=username)
        except:
            return myJsonResponse(dictFail('Username not existed.'))
        if user.password==hash_code(oldpsw):
            user.password=hash_code(newpsw)
            user.save()
            request.session.flush()
            return myJsonResponse({'status':'ok','type':'changePassword'})
        else:
            return myJsonResponse(dictFail('Wrong Password.'))
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))

@csrf_exempt
def resetPassword(request):
    if request.method=='POST':
        data=json.loads(request.body)
        username=data['username']
        try:
            user=models.User.objects.get(name=username)
        except:
            return myJsonResponse(dictFail('Username {} not existed.'.format(username)))
        if user.has_confirmed==False:
            return myJsonResponse(dictFail('This account named {} has not accomplished email confirmation.'.format(username)))
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newpsw=hash_code(username,now)[:16]
        sendResetEmail(user.email,username,newpsw)
        user.password=hash_code(newpsw)
        user.save()
        return myJsonResponse({'status':'ok','type':'resetPassword'})

    else:
        return myJsonResponse(dictFail('Request method is not POST.'))
