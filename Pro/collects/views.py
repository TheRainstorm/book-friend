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
        path = '/books/' + str(book_id)
        return redirect(path)
    else:
        return HttpResponse('False')

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
    
    comment_li = Comment.objects.filter(bookName=book).order_by('-create_time') 
    comment_li = comment_li[0:3]
    
    L=[]
    for i in range(3):
        dic={}
        dic['image_path']=comment_li[i].userName.image
        dic['user_name']=comment_li[i].userName.user_name
        dic['content']=comment_li[i].content
        dic['date']=str(comment_li[i].create_time)
        L.append(dic)

    return HttpResponse(json.dumps({'comment_li':L}))
    
#取消收藏
def collect_del(request,book_id):
    #session 获得用户
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]

    book = Book.objects.get(book_id=book_id)
    #取消收藏
    Collection.objects.filter(user=user,book=book).delete()
    #收藏次数减1
    #收藏次数总大于1
    if book.collection_number > 0:
        collection_number = book.collection_number - 1
    else:
        collection_number = 0

    Book.objects.filter(book_id=book_id).update(collection_number=collection_number)
    return redirect('/users/my_collects/')
