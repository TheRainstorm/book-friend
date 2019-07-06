from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse

from users.models import User
from books.models import Book
import os
import uuid

from books.enums import BOOKS_TYPE

# Create your views here.
def index(request):
    books_li = Book.objects.all()
    return render(request,'books/index.html',{"book_li":books_li})

def add(request):
    if request.POST:
        title = request.POST.get('title',None)
        author = request.POST.get('author',None)
        uploader_id = request.POST.get('uploader_id',None)
        type_id = request.POST.get('type_id',None)
        tag_li = request.POST.get('tag',None)
        description = request.POST.get('description',None)
        path1 = request.POST.get('path1',None)
        path2 = request.POST.get('path2',None)
        view_number = request.POST.get('view_number',None)
        collection_number = request.POST.get('collection_number',None)

        print("typeof(tag_li",type(tag_li))

        #User
        user = User.objects.filter(user_id=uploader_id)[0]
        print("typeof(user)",type(user))
        Book.objects.create(
            title=title,
            author=author,
            uploader=user,
            type_id=type_id,
            # tag= '',
            tag= tag_li,
            description=description,
            content_path=path1,
            image_path=path2,
            view_number=view_number,
            collection_number=collection_number
        )
        book_li = Book.objects.all()

        return render(request,'books/index.html',{'book_li':book_li})
    else:
        return render(request,'books/add.html')

def delete(request,book_id):
    try:
        Book.objects.filter(book_id=book_id).delete()
    except:
        pass
    return redirect('/books/index/')

def goupdate(request,book_id):
    book = Book.objects.filter(book_id=book_id)[0]
    return render(request,'books/update.html',{'book':book})

def update(request):
    book_id = request.POST.get('book_id',None)
    title = request.POST.get('title',None)
    author = request.POST.get('author',None)
    uploader_id = request.POST.get('uploader_id',None)
    type_id = request.POST.get('type_id',None)
    tag_li = request.POST.get('tag',None)
    description = request.POST.get('description',None)
    path1 = request.POST.get('path1',None)
    path2 = request.POST.get('path2',None)
    view_number = request.POST.get('view_number',None)
    collection_number = request.POST.get('collection_number',None)

    user = User.objects.filter(user_id=uploader_id)[0]

    Book.objects.filter(book_id=book_id).update(
        title=title,
        author=author,
        uploader=user,
        type_id=type_id,
        tag= tag_li,
        description=description,
        content_path=path1,
        image_path=path2,
        view_number=view_number,
        collection_number=collection_number
    )

    book_li = Book.objects.all()

    return render(request,'books/index.html',{'book_li':book_li})

def detail(request,book_id):
    #获得当前用户对象
    user_name = request.session.get('account',None)
    user = User.objects.filter(user_name=user_name)[0]
    #获得当前浏览的书的对象
    book = Book.objects.get(book_id=book_id)
    #更新用户的浏览记录
    user.recent_read.add(book)

    book_type = BOOKS_TYPE[int(book.type_id)]
    return render(request,'books/detail.html',{'book':book,'book_type':book_type})