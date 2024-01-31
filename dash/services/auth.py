
from contextlib import closing
import datetime
import random

from django.db import connection
from dash.models import User, OtpToken
from django.shortcuts import render, redirect
from methodism import generate_key, code_decoder
from django.contrib.auth import login as dj_login, logout, authenticate

def sign_in(request):
    ctx = {}
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        pas = data.get('parol')

        user = User.objects.filter(username=username).first()

        if not user:
            return render(request, 'auth/login.html', {'error':'Login yoki parol xato!'})
        if not user.is_active:
            return render(request, 'auth/login.html', {'error':'User BAN holatda!'})
        if not user.check_password(pas):
            return render(request, 'auth/login.html', {'error':'Login yoki parol xato!'})
        code = random.randint(100_000, 999_999)
        # sms chiqib ketadi
        token = generate_key(20)+ f"##{code}##" + generate_key(20)
        otp = OtpToken.objects.create(key=token, by=2, extra={'user_id':user.id})

        request.session['otp-token'] = otp.key
        request.session['user_id'] = user.id
        request.session['code'] = code
        return redirect('otp')
    return render(request, 'auth/login.html', ctx)
        


def sign_up(request):
    ctx = {}
    if request.POST:
        pas = request.POST.get('pas')
        repas = request.POST.get('re-pas')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fio = request.POST.get('fio')

        #   user chek
        user_sql = f'''
            select id from dash_user
            where email = '{email}' or  username='{username}'
        '''
        with closing(connection.cursor()) as cursor:
            cursor.execute(user_sql)
            user = cursor.fetchone()
        if user:
            return render(request, 'auth/regis.html', {'error':'Ushbu username yoki email allaqachon foydalanilmoqda'})
        if pas != repas:
            return render(request, 'auth/regis.html', {'error':'Parollar mos kelmadi'})
        
        # otp
        
        code = random.randint(100_000, 999_999)
        # sms chiqib ketadi
        token = generate_key(20) + f"##{code}##" + generate_key(20)
        # shifrlab qoyiladi
        otp = OtpToken.objects.create(key=token, by=1,
                                      extra={
                                          'username':username, 'email':email, 'password':pas, 'fio':fio
                                      })
        request.session['otp-token'] = otp.key
        request.session['code'] = code
        return redirect('otp')

    return render(request, 'auth/regis.html', {})

def sign_out(request):
    logout(request)
    return redirect('sign-in')

def step_two(request):
    token = request.session.get('otp-token')
    if not token:
        return redirect('sign-in')
    if request.POST:
        kod = request.POST.get('code')
        otp = OtpToken.objects.filter(key=token).first()
        if not otp:
            return redirect('sign-in')
        if otp.is_expired or otp.is_verified:
            return render(request, 'auth/otp.html', {'error':'Ushbu token yaroqsiz'})
        now = datetime.datetime.now()
        if (now-otp.created).total_seconds() > 120:
            return render(request, 'auth/otp.html', {'error':'Tokenga ajratilgan vaqt tugadi'})
        
        code = str(token).split('##')[1]
        if str(code) != str(kod):
            otp.tries += 1
            otp.save()
            return render(request, 'auth/otp.html', {'error':'Xato kod'})
        
        if otp.by == 2:
            if str(otp.extra['user_id']) != str(request.session.get('user_id')):
                return redirect('sign-in')
            user = User.objects.filter(id=request.session.get('user_id')).first()
            if not user:
                return redirect('sign-in')
            dj_login(request, user)
            otp.is_expired = True
            otp.is_verified = True
            otp.save()
            try:
                del request.session['otp_token']
                del request.session['user_id']
                del request.session['code']
            except:
                pass
            return redirect('index')
        
        elif otp.by == 1:
            user = User.objects.create_user(**otp.extra)
            dj_login(request, user)
            authenticate(request)
            
            otp.is_expired = True
            otp.is_verified = True
            otp.extra = {}
            otp.save()
            try:
                del request.session['otp-token']
                del request.session['code']
            except:
                pass
            return redirect('index')
        
    return render(request, 'auth/otp.html')

def re_otp(request):
    old_token = request.session.get('otp_token')
    if not old_token:
        return redirect('sign-in')
    old_otp = OtpToken.objects.filter(key=old_token).first()
    if not old_otp:
        return redirect('sign-in')
    old_otp.is_verified = True
    old_otp.save()
    new_code = random.randint(100_000, 999_999)
        # sms chiqib ketadi
    new_token = generate_key(20)+ f"##{new_code}##" + generate_key(20)
    otp = OtpToken.objects.create(key=new_token, by=old_otp.by, extra={'user_id':old_otp.extra})

    request.session['otp-token'] = otp.key
    if otp.by == 2:
        request.session['user_id'] = old_otp.extra['user_id']
        old_otp.extra = {}
        old_otp.save()
    request.session['code'] = new_code
    return redirect('otp')

