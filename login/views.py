from django.shortcuts import render,redirect
from django import forms
from django.conf import settings
from . import models
import hashlib,datetime,pytz
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username=forms.CharField(label='User Name',max_length=128)
    password=forms.CharField(label='Password',max_length=256,widget=forms.PasswordInput)
    captcha=CaptchaField(label='Captcha')

class RegisterForm(forms.Form):
    username=forms.CharField(label='User Name',max_length=128)
    password1=forms.CharField(label='Password',max_length=256,widget=forms.PasswordInput)
    password2=forms.CharField(label='Password',max_length=256,widget=forms.PasswordInput)
    email=forms.EmailField(label='Email Address',widget=forms.EmailInput)
    captcha=CaptchaField(label='Captcha')

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

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/user/index/')
    if request.method=='POST':
        login_form=UserForm(request.POST)
        message='All the attribute should be written.'
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            #print(username,password)
            try:
                user=models.User.objects.get(name=username)
                #print(user,user.has_confirmed)

                if user.has_confirmed==False:
                    message='This account has not accomplished email confirmation.'
                    return render(request,'login/login.html',locals())

                if user.password==hash_code(password):
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name']=user.name
                    return redirect('/user/index/')
                else:
                    message='Wrong password.'
            except:
                message='Username not existed.'
        return render(request,'login/login.html',locals())
    login_form=UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):#Register while logged in is not permitted
        return redirect('/user/index/')
    if request.method=='POST':
        register_form=RegisterForm(request.POST)
        message='Please check your input.'
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            password1=register_form.cleaned_data['password1']
            password2=register_form.cleaned_data['password2']
            email=register_form.cleaned_data['email']
            if password1!=password2:
                message='Two password input do not match.'
                return render(request,'login/register.html',locals())
            else:
                same_name_user=models.User.objects.filter(name=username)
                if same_name_user:
                    message='Username already existed.'
                    return render(request,'login/register.html',locals())
                same_email_user=models.User.objects.filter(email=email)
                if same_email_user:
                    message='This email address has been used.'
                    return render(request,'login/register.html',locals())

                new_user=models.User.objects.create(
                    name=username,
                    password=hash_code(password1),
                    email=email
                )

                code=makeConfirmString(new_user)
                send_email(email,code)
                message='Please enter your email account to accomplish the confirmation.'
                return render(request,'login/confirm.html',locals())
    register_form=RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/user/index/')
    request.session.flush()
    return redirect('/user/index/')

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
