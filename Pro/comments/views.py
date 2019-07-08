from django.shortcuts import render,redirect,HttpResponse
import json
from users.models import User
from books.models import Book
from comments.models import Comment
# Create your views here.

def addcom2(request):
    #添加评论
    #需要的前端数据：1、用户id 2、书id 3、评论内容
    #session 获得用户
    user_name = request.session.get('account',None)
    user = User.objects.get(user_name=user_name)
    
    book_id = request.POST.get('book_id',None)
    book = Book.objects.get(book_id=book_id)

    content = request.POST.get('content',None)
    Comment.objects.create(userName=user, bookName=book, content=content)
    return redirect('/books/'+book_id)

def addcom(request):
    #添加评论
    #需要的前端数据：1、用户id 2、书id 3、评论内容
    #session 获得用户
    user_name = request.session.get('account',None)
    if user_name == None:
        return HttpResponse(False)
    user = User.objects.get(user_name=user_name)
    
    book_id = request.POST.get('book_id',None)
    print('book_id',book_id)

    book = Book.objects.get(book_id=book_id)

    content = request.POST.get('content',None)
    
    Comment.objects.create(userName=user, bookName=book, content=content)
    
    comment_li = Comment.objects.filter(bookName=book).order_by('-create_time') 
    comment_li = comment_li[0:3]
    
    L=[]
    for i in range(len(comment_li)):
        dic={}
        dic['image_path']=comment_li[i].userName.image
        dic['user_name']=comment_li[i].userName.user_name
        dic['content']=comment_li[i].content
        dic['date']=str(comment_li[i].create_time)
        L.append(dic)

    return HttpResponse(json.dumps({'comment_li':L}))

def delcom(request,com_id):
    #通过评论的id删除评论
    #需要的前端数据：1、评论id
    com = Comment.objects.filter(commentId=com_id)
    com.delete()
    return redirect('/users/personal_comments/')

