from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse

from users.models import User
from books.models import Book
from collects.models import Collection

# Create your views here.
def collect_add(request,book_id):
    #session 获得用户
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]

    book = Book.objects.get(book_id=book_id)
    #判断是否已经收藏
    if len(Collection.objects.filter(user=user,book=book))==0:
        #创建这个收藏数据
        Collection.objects.create(user=user,book=book)
        #这本书被多收藏了一次
        collection_number = book.collection_number + 1
        Book.objects.filter(book_id=book_id).update(collection_number=collection_number)
        return HttpResponse('True')
    else:
        return HttpResponse('False')
    
#取消收藏
def collect_del(request,book_id):
    #session 获得用户
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]

    book = Book.objects.get(book_id=book_id)
    #取消收藏
    Collection.objects.filter(user=user,book=book).delete()
    #收藏次数减1
    collection_number = book.collection_number - 1
    Book.objects.filter(book_id=book_id).update(collection_number=collection_number)
    return redirect('/users/my_collects/')
