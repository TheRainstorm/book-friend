from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from users.models import User
from books.models import Book
from comments.models import Comment
from collects.models import Collection
import os
import uuid

from books.enums import BOOKS_TYPE

# Create your views here.
# def type_ranking(request):
#     python_new = Book.objects.get_books_by_type(PYTHON, sort='new')
#     python_hot = Book.objects.get_books_by_type(PYTHON, sort='hot')

#     context = {
#         'python_new': python_new,
#         'python_hot': python_hot,
#     }

#     return render(request, 'book/index.html', context)

# def all_ranking(request):
#     all_new = Book.objects.get_all_ranking(sort='new')
#     all_hot = Book.objects.get_all_ranking(sort='collect-hot')

#     context = {
#         'all_new': all_new,
#         'all_hot': all_hot,
#     }
    
#     return render(request, 'book/index.html', context)

def index(request):
    books_li = Book.objects.all()
    all_book_li_by_hot = Book.objects.get_all_ranking(limit=10,sort='view-hot')
    context = {
        "book_li":books_li,
        'all_book_li_by_hot':all_book_li_by_hot,
        'type_dic':BOOKS_TYPE
    }
    return render(request,'books/index.html',context)

def add(request):
    if request.POST:
        title = request.POST.get('title',None)
        author = request.POST.get('author',None)
        #session 获得user
        user_name = request.session.get('account',None)
        user = User.objects.filter(user_name=user_name)[0]

        type_id = request.POST.get('type_id',None)
        tag_li = request.POST.get('tag',None)
        description = request.POST.get('description',None)

        '''上传文本'''
        objtext = request.FILES.get('upfiletxt',None)  #先拿到文件   然后需要把文件存入一个地方
        uploadDirPath = os.path.join(os.getcwd(),'static/books/text')
        if not os.path.exists(uploadDirPath):
            os.mkdir(uploadDirPath)  # 是否存在  不存在则添加文件夹
        # 拼接要上传的文件在服务器上的全路径
        postfix = os.path.splitext(objtext.name)[1]
        objtext_u_name = str(uuid.uuid1())+postfix
        content_path = uploadDirPath + os.sep + objtext_u_name
        # 上传文件
        with open(content_path, 'wb+') as fp:
            for chunk in objtext.chunks():
                fp.write(chunk)
        '''上传图片'''
        objimage = request.FILES.get('upfileimg',None)
        uploadDirPath = os.path.join(os.getcwd(),'static/books/picture')
        if not os.path.exists(uploadDirPath):
            os.mkdir(uploadDirPath)  # 是否存在  不存在则添加文件夹
        # 拼接要上传的文件在服务器上的全路径
        postfix = os.path.splitext(objimage.name)[1]
        objimage_u_name = str(uuid.uuid1())+postfix
        content_path = uploadDirPath + os.sep + objimage_u_name
        # 上传文件
        with open(content_path, 'wb+') as fp:
            for chunk in objtext.chunks():
                fp.write(chunk)
        #路径
        text_path = 'books/text/'+ objtext_u_name
        picture_path = 'books/picture/'+ objimage_u_name

        Book.objects.create(
            title=title,
            author=author,
            uploader=user,
            type_id=type_id,
            tag= tag_li,
            description=description,
            content_path=text_path,
            image_path=picture_path
        )

        return render(request,'books/add.html',{'msg':'上传成功'})
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

    book_li = user.recent_read.all()


    #获得评论
    comment_li = Comment.objects.filter(bookName=book) 
    #获得是否收藏
    collection_li =Collection.objects.filter(book=book,user=user)
    #浏览加1
    view_number = book.view_number
    # book.update(view_number=view_number+1)
    Book.objects.filter(book_id=book_id).update(view_number=view_number+1)
    if len(collection_li)==0:
        is_collected=0
    else:
        is_collected=1
    book_type = BOOKS_TYPE[int(book.type_id)]
    context = {
        'book':book,
        'book_type':book_type,
        'comment_li':comment_li,
        'is_collected':is_collected
    }
    return render(request,'books/detail.html',context)

#每一类书的页面
def types(request,type_id):
    typeBooks = Book.objects.get_books_by_type(type_id=type_id,sort='new')

    paginator = Paginator(typeBooks,3) #每页显示6本
    #接受客户端发送的页码:
    page = request.GET.get('page',1)
    #
    try:
        typeBooks=paginator.page(page)
    except EmptyPage:
        typeBooks= paginator.page(1)
    except PageNotAnInteger:
        typeBooks = paginator.page(paginator.num_pages)
    return render(request,'books/category.html',{'book_li' : typeBooks})