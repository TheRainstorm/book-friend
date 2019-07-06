from django.shortcuts import render,redirect

from users.models import User
from books.models import Book
from comments.models import Comment
# Create your views here.

def addcom(request):
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

def delcom(request,com_id):
    #通过评论的id删除评论
    #需要的前端数据：1、评论id
    com = Comment.objects.filter(commentId=com_id)
    com.delete()
    return redirect('/users/personal_comments/')

