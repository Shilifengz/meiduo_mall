from django.shortcuts import render,redirect
from django.views import View
from django import http
import re
from .models import User
from django.contrib.auth import login
from meiduo_mall.utils.response_code import RETCODE

# Create your views here.
class RegisterView(View):

    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        # 接收
        username=request.POST.get('user_name')
        password=request.POST.get('pwd')
        password2=request.POST.get('cpwd')
        mobile=request.POST.get('mobile')
        sms_code=request.POST.get('sms_code')
        allow=request.POST.get('allow')

        # 驗證
        #1.非空
        if not all([username,password,password2,mobile,sms_code,allow]):
            return http.HttpResponseForbidden('填写数据不完整')
        #2.用户名
        if re.match('^[a-zA-Z0-9]{5,20}$',username):
            return http.HttpResponseForbidden('用户名不正确')
        if User.objects.fillter(username=username).count()>0:
            return http.HttpResponseForbidden('用户名已经存在')
        # 密码
        if not re.match('^[0-9A-Za-z]{8,20}$',password):
            return http.HttpResponseForbidden('密码为8-20个字符')
        # 确认密码
        if password!=password2:
            return http.HttpResponseForbidden('两个密码不一致')
        #手机号
        if not re.match('^1[345789]\d{9}$',mobile):
            return http.HttpResponseForbidden('手机号错误')
        if User.objects.fillter(mobile=mobile).count()>0:
            return http.HttpResponseForbidden('手机号已经存在')
        # 短信验证

        # 处理
        #1.创建用户对象
        user=User.objects.create_user(
            username=username,
            password=password,
            mobile=mobile
        )
        #2.状态保持
        login(request,user)
        # 响应
        return redirect('/')

class UsernameCountView(View):
    def get(self,request,username):
        # 接受
        # 验证
        # 处理
        count=User.objects.filter(username=username).count()
        # 响应
        return http.JsonResponse({
            'count':count,
            'code':RETCODE.OK,
            'errmsg':'OK'
        })

class MobileCountView(View):
    def get(self,request,mobile):
        #1.接收
        #2.验证
        #3.处理
        count=User.objects.filter(mobile=mobile).count()
        #4.响应
        return http.JsonResponse({
            'count':count,
            'code':RETCODE.OK,
            'errmsg':"OK"
        })
        pass