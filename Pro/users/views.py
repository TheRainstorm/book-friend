from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse

from users.models import User
from books.models import Book
from comments.models import Comment
from collects.models import Collection
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
            response = redirect('/books/index/')
            response.set_signed_cookie('account',account,salt='aaa')
            if(save_pwd=='on'):
                response.set_signed_cookie('password',pwd,salt='bbb')

            request.session['account'] = account
            return response
    else:
        account = request.get_signed_cookie('account','','aaa')
        password = request.get_signed_cookie('password','','bbb')
        return render(request,'users/login.html',{'account':account,'password':password})

def logout(request):
    #删除session
    del request.session['account']
    return redirect('/users/login/')

def check_account(request,user_name):
    user_li = User.objects.filter(user_name=user_name)
    if len(user_li)==0:
        return HttpResponse('True')
    else:
        return HttpResponse('False')

import json

def get_recent_read_book(request):
    return json.loads(request.session['recent_read_book'])
    
def home(request):
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]

    '''设置recent_read_book session'''
    recent_read_book = request.session.get('recent_read_book',None)
    if recent_read_book==None:
        L = []
        L.append(book.book_id)
        request.session['recent_read_book']= json.dumps(L)
        request.session.set_expiry(3600*24*365)
    
    recent_read_book_id_li = get_recent_read_book(request)
    recent_read_book_li = [Book.objects.get(book_id=e) for e in recent_read_book_id_li]

    collect_li = Collection.objects.filter(user=user)
    collect_book_li = [e.book for e in collect_li]

    view_num = len(recent_read_book_li) #浏览量
    collect_num = len(collect_book_li) #收藏量

    context = {
        "user":user,
        'headpic_url':user.image,
        'view_num':view_num,
        'collect_num':collect_num,
        'recent_read_book_li':recent_read_book_li,
        'collect_book_li':collect_book_li,
    }

    return render(request,'users/home.html',context)

def recent_read(request):
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]

    book_li = user.recent_read.all()
    return render(request,'users/recent_read.html',{'user':user,'book_li':book_li})

def personal_comments(request):
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]

    comment_li =Comment.objects.filter(userName=user)

    return render(request,'users/personal_comments.html',{'comment_li':comment_li})

def my_collects(request):
    user_name = request.session.get('account',None)
    if user_name==None:
        return redirect('/users/login/')
    user = User.objects.filter(user_name=user_name)[0]

    collection_li = Collection.objects.filter(user=user)

    book_li=[]
    for collect in collection_li:
        book_li.append(collect.book)
    return render(request,'users/shelf.html',{'book_li':book_li,'user':user})

# def collect_view(request):
#     if request.POST:
#         userid = request.POST.get('userid',None)
#         user = User.objects.get(user_id=userid)
#         book_collections = collection.objects.filter(user=user)
#         booklist=[]
#         for collect in book_collections:
#             booklist.append(collect.book)
#         return render(request,'collection/booksInfo.html',{'booklist':booklist})#返回收藏书的信息显示
#     else:
#         return render(request,'collection/booksInfo.html')

def edit_info(request):
    user_name = request.session.get('account',None)
    user_li = User.objects.filter(user_name=user_name)
    if request.POST:
        user_name_change = request.POST.get('user_name',None)
        pwd1 = request.POST.get('pwd1',None)
        pwd2 = request.POST.get('pwd2',None)
        if pwd1!=pwd2:
            msg ="密码两次输入不一致，请确认"
            return render(request,'users/edit2.html',{'user':user_li[0],'msg':msg})
        #上传头像(更新)
        src = upload_headpic(request)

        user_li.update(
            user_name = user_name_change,
            password = pwd1,
            image = src,
        )
        msg ="修改信息成功"
        return render(request,'users/edit.html',{'user':user_li[0],'msg':msg})
    else:
        return render(request,'users/edit.html',{'user':user_li[0]})

def upload_headpic(request):
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
    return src
    
def register(request):
    if request.POST:
        usr_name = request.POST.get('usr_name',None)
        user_li = User.objects.filter(user_name=usr_name)
        if len(user_li)!=0:
            return render(request,'users/register.html',{'msg':'该用户名已被注册'})
        else:
            password = request.POST.get('password',None)
            #上传头像
            src = upload_headpic(request)
            
            user = User(user_name = usr_name,password = password,image = src)
            user.save()

            return render(request,'users/login.html')
    else:
        return render(request,'users/register.html')

def get_headpic(request):
    user_name = request.GET.get('user_name',None)
    user_li = User.objects.filter(user_name = user_name)
    if len(user_li)==0:
        return HttpResponse('False')
    else:
        print(user_li[0].image)
        image_url = '/static/' + user_li[0].image
        return HttpResponse(image_url)