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
        save_pwd = request.POST.get('save_pwd', '')
        #数据库查找
        cur_user = User()
        all_user = User.objects.all()
        for user in all_user:
            if user.account == account and user.password == pwd:
                cur_user = user
                break
        else:
            data = {}
            data['msg'] = '账号或密码错误'
            return render(request,'login.html',data)
        #成功
        response = render(request,'blog.html',{'account':account,'src':cur_user.headpic_path})
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
        acc = request.POST.get('account',None)
        name = request.POST.get('name',None)
        headpic_name = request.POST.get('headpic_name',None)
        password = request.POST.get('password',None)
        # name
        # gender
        # city
        # headpic   //头像文件,重复提交
        # signature
        # return render(request,'login.html',{'msg':"{0},注册成功，请登录。".format(name)})
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
                upload_path = os.path.join(os.getcwd(),'blog/static/img/headpic/')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                #上传文件全路径
                file_u_name = str(uuid.uuid1()) + postfix
                upload_file_full_path = os.path.join(upload_path,file_u_name)
                #上传
                with open(upload_file_full_path,'wb+') as fp:
                    for chunck in headpic.chunks():
                        fp.write(chunck)
                src = 'img/headpic/'+ file_u_name
        
        user = User(account = acc,password = password,name = name, headpic_path = src)
        user.save()

        return render(request,'success.html',{'account': acc, 'src': src})
    else:
        return render(request,'register.html')