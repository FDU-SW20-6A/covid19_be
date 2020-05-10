from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from . import models
import hashlib,datetime,pytz,json,csv
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def dictFail(s):
    return {'status':'error','type':s}

def myJsonResponse(ret):
    json_data=json.dumps(ret,ensure_ascii=False)
    response=HttpResponse(json_data)
    response['Access-Control-Allow-Origin']='*'
    response['Access-Control-Allow-Methods']='POST,GET,OPTIONS'
    response['Access-Control-Max-Age']='2000'
    response['Access-Control-Allow-Headers']='*'
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

def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives
    subject='Registration Confirm'
    textContent='This is a registration confirmation.'
    htmlContent='<p>Click <a href="http://{}/user/confirm/?code={}" target="blank">this</a> to accomplish the confirmation.</p>'.format('localhost:8001',code,settings.CONFIRM_DAYS)
    msg=EmailMultiAlternatives(subject,textContent,settings.DEFAULT_FROM_EMAIL,[email])
    msg.attach_alternative(htmlContent,'text/html')
    msg.send()

@csrf_exempt
def login(request):
    fail={'status':'error','type':'account','currentAuthority':'guest'}
    if request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logined.'))
    if request.method=='POST':
        #request.session.flush()
        data=json.loads(request.body)
        print(data)
        username=data['userName']
        password=data['password']
        ret=fail
        #print(username,password)
        try:
            user=models.User.objects.get(name=username)
            if user.has_confirmed==False:
                message='This account named {} has not accomplished email confirmation.'.format(username)

            if user.password==hash_code(password):
                request.session['is_login']=True
                request.session['user_id']=user.id
                request.session['user_name']=user.name
                ret={'status':'ok','type':'account','currentAuthority':user.authority}
            else:
                message='Wrong password. username:{}'.format(username)
        except:
            message='Username not existed.'
        #print(message)

        return myJsonResponse(ret)

@csrf_exempt
def register(request):
    request.session.clear_expired()
    if request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logined.'))
    if request.method=='POST':
        ret=fail
        data=json.loads(request.body)
        username=data['username']
        password1=data['password1']
        password2=data['password2']
        authority=data['authority']
        email=data['email']
        if password1!=password2:
            message='Two password input do not match.\nusername:{}\npassword1:{}\npassword2:{}'.format(username,password1,password2)
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
                        has_confirmed=True,
                    )
                    return myJsonResponse({'status':'ok','type':'register'})

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

def inputdata(request):
    fp=open(r'login/data/AMap_adcode.csv','r',encoding='gbk',errors='ignore')
    dictReader=csv.DictReader(fp)
    for row in dictReader:
        models.Region.objects.get_or_create(
            name=row['中文名'],
            adcode=row['adcode']
        )
        print(row['中文名'],row['adcode'])
    return myJsonResponse({'status':'ok'})

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
def addSubscribe(request):
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
        for adcode in content:
            try:
                region=models.Region.objects.get(adcode=adcode)
            except:
                return myJsonResponse(dictFail('Adcode {} not existed.'.format(adcode)))
            user.regions.add(region)
        regionsList=[{'name':x.name,'adcode':x.adcode} for x in user.regions.all()]
        return myJsonResponse({
            'status':'ok',
            'type':'subscribe',
            'content':regionsList,
        })
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))

@csrf_exempt
def delSubscribe(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    if request.method=='POST':
        data=json.loads(request.body)
        username=request.session['user_name']
        isClear=eval(data['isClear'])
        content=data['content']
        try:
            user=models.User.objects.get(name=username)
        except:
            return myJsonResponse(dictFail('User {} not existed.'.format(username)))
        if isClear:
            user.regions.clear()
        else:
            regions=user.regions.all()
            for adcode in content:
                try:
                    region=models.Region.objects.get(adcode=adcode)
                except:
                    return myJsonResponse(dictFail('Adcode {} not existed.'.format(adcode)))
                if region not in regions:
                    return myJsonResponse(dictFail('adcode {} not in user {}\'s subscribe list.'.format(adcode,username)))
                user.regions.remove(region)
        regionsList=[{'name':x.name,'adcode':x.adcode} for x in user.regions.all()]
        return myJsonResponse({
            'status':'ok',
            'type':'subscribe',
            'content':regionsList,
        })
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))

@csrf_exempt
def getCurrentUser(request):
    if not request.session.get('is_login',None):
        return myJsonResponse(dictFail('Already logouted.'))
    return myJsonResponse({'status':'ok','username':request.session['user_name']})
