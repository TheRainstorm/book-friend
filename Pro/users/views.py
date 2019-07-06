from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse

from users.models import User
import os
import uuid
# Create your views here.
def login(request):
    if(request.method=='POST'):
        account = request.POST.get('account', '')
        pwd = request.POST.get('password', '')
        save_pwd = request.POST.get('save_pwd', '') #是否保存密码
        #数据库查找
        user_li = User.objects.filter(user_name=account)
        # cur_user = User()
        # all_user = User.objects.all()
        # for user in all_user:
        #     if user.account == account and user.password == pwd:
        #         cur_user = user
        #         break
        if len(user_li)==0:
            data = {}
            data['msg'] = '账号或密码错误'
            return render(request,'users/login.html',data)
        else:
            #成功
            response = render(request,'users/success.html',{'account':account,'src':user_li[0].image})
            response.set_signed_cookie('account',account,salt='aaa')
            if(save_pwd=='on'):
                response.set_signed_cookie('password',pwd,salt='bbb')

            request.session['account'] = account
            return response
    else:
        account = request.get_signed_cookie('account','','aaa')
        password = request.get_signed_cookie('password','','bbb')
        return render(request,'users/login.html',{'account':account,'password':password})

def register(request):
    if request.POST:
        usr_name = request.POST.get('usr_name',None)
        password = request.POST.get('password',None)
        '''头像上传'''
        headpic = request.FILES.get('headpic',None)
        if headpic==None:
            src = 'img/yuxiaoqin.jpg'
        else:
            #检测文件类型（要求为图片）
            postfix = os.path.splitext(headpic.name)[1]
            # print(os.path.splitext(headpic.name))
            accept_postfix = ['.jpg','.jpeg','.png','.PNG','.bmp','.gif']
            if postfix not in accept_postfix:
                return HttpResponse('not picture')
            else:
                #设置上传文件夹
                upload_path = os.path.join(os.getcwd(),'static/image/headpic/')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                #上传文件全路径
                file_u_name = str(uuid.uuid1()) + postfix
                upload_file_full_path = os.path.join(upload_path,file_u_name)
                #上传
                with open(upload_file_full_path,'wb+') as fp:
                    for chunck in headpic.chunks():
                        fp.write(chunck)
                src = 'image/headpic/'+ file_u_name
        
        user = User(user_name = usr_name,password = password,image = src)
        user.save()

        return render(request,'users/success.html',{'account': usr_name, 'src': src})
    else:
        return render(request,'users/register.html')

def check_account(request,user_name):
    user_li = User.objects.filter(user_name=user_name)
    if len(user_li)==0:
        return HttpResponse('True')
    else:
        return HttpResponse('False')