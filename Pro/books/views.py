from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from users.models import User
from books.models import Book
from comments.models import Comment
from collects.models import Collection
import os
import uuid
import re
from books.enums import BOOKS_TYPE
import json
import xlrd
from django.db import transaction

def index(request):
    #session 获得user
    user_name = request.session.get('account',None)

    if user_name!=None:
        user = User.objects.filter(user_name=user_name)[0]
    else:
        user = None
    
    books_li = Book.objects.all()
    all_book_li_by_hot = Book.objects.get_all_ranking(limit=10,sort='view-hot')

    #每种类型按new分类返回
    category1_new = Book.objects.get_books_by_type(1, limit=7, sort='new') #仙侠玄幻
    category2_new = Book.objects.get_books_by_type(2,limit= 7, sort='new')#历史纵横
    category3_new = Book.objects.get_books_by_type(3, 7, sort='new')#都市言情

    context = {
        'user':user,
        "book_li":books_li,
        'all_book_li_by_hot':all_book_li_by_hot,
        'types_book':[  ['仙侠玄幻',category1_new],
                        ['历史纵横',category2_new],
                        ['都市言情',category3_new]
                    ],
    }
    
    return render(request,'books/index.html',context)

def go2index(request):
    return redirect('/books/index/')

def read_json(name):
    path = 'static/books/json/' + name + '.json'
    with open(path) as f:
        string = f.read()
    dict = json.loads(string)
    return dict

def chapters(request, bookname):
    content = read_json(bookname)
    chapters_list = list(content.keys())
    #id_list = [i for i in range(len(chapters_list))]
    chapters = []
    for i in range(len(chapters_list)):
        chapters.append({'chapters_id': i,'chapters_name':chapters_list[i],})
    
    chapters_dic = {
        'bookname':bookname,
        'chapters':chapters
    }

    return render(request,'books/chapters.html',chapters_dic)

def read(request, bookname, chapters_id):
    '''
    阅读界面
    :param request:
    :param id:书籍ID
    :param book_id:源ID
    :param titleID: 章节ID
    :return:
    '''
    # session 获得user
    user_name = request.session.get('account',None)
    if user_name:
        is_login = True
    else:
        is_login = False

    content = read_json(bookname)
    chapters_list =  list(content.keys())
    
    last_chapter = int(chapters_id) - 1
    book_content = content[chapters_list[int(chapters_id)]]
    next_chapter = int(chapters_id) + 1
    # 获得书名
    title = chapters_list[chapters_id]
    
    book_content = book_content.replace('上一页', '')
    book_content = book_content.replace('下一页', '')
    book_content = book_content.replace('-', '')

    content = re.findall('.*\n', book_content)

    context = {
        'body':content,
        'next': next_chapter,
        'last':last_chapter,
        'bookname':bookname,
        'title':title,
        'is_login':is_login,
    }

    return render(request,'books/read.html',context=context)

#后端上传书籍接口
def uploadBooks(request):
    '''
    班级信息导入
    :param request:
    :return:
    '''
    if request.method == 'POST':
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx','xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            name_list = ['yfy','jyf','hx','smy','twz','lg','lb','hmx','cgz','mxy','hkh','xmh','qx']
            user_list = []
            for i in range(13):
                flag = i%13
                user_name = name_list[flag]
                user = User.objects.get(user_name=user_name,password="123456")
                user_list.append(user)
            with transaction.atomic():  # 控制数据库事务交易
                for i in range(1,rows):
                    flag = i%13
                    rowVlaues = table.row_values(i)
                    path = '\\books\\picture\\' + str(i-1) + '.jpg'
                    rowVlaues[4] = rowVlaues[4][:40]
                    print(rowVlaues[0])
                    book = Book(title=rowVlaues[1],author=rowVlaues[2],uploader=user_list[flag],type_id=int(rowVlaues[0]),description=rowVlaues[4],image_path=path,view_number=rowVlaues[5],collection_number=rowVlaues[6])
                    book.save()
                    print(book)
            return render(request,'books/shangchuan.html')
        else:
            return render(request,'books/shangchuan.html')

def shangchuan(request):
    return render(request, 'books/shangchuan.html')    

def find_chaps(name, bookname):
    chapters = {}
    patterns = re.compile('第[一二三四五六七八九]*千*[一二三四五六七八九]*百*零*[一二三四五六七八九]*十*[一二三四五六七八九]*章\s.*\n')
    encoding = ['utf-8', 'gbk', 'gb2312', 'iso-8859-1']
    filename = os.getcwd() + '\\static\\books\\text\\' + name
    for e in encoding:
        try:
            with open(filename, encoding=e) as f:
                text = f.read()
        except UnicodeDecodeError:
            pass
        else:
            break
    res = re.findall(patterns, text)
    title = res[0]
    text = text.replace(title, '')
    for i in range(len(res)):
        if i == (len(res) - 1):
            content = text
            title = title.replace('\n', '')
            chapters[title] = content
        else:
            ind = text.index(res[i + 1])
            content = text[:ind]
            text = text[ind:]
            title = title.replace('\n', '')
            chapters[title] = content
            title = res[i + 1]
            text = text.replace(title, '')
    name = name.replace('.txt', '.json')
    with open(os.getcwd() + '\\static\\books\\json\\' + bookname + '.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(chapters))
    return chapters


def add(request):
    if request.POST:
        title = request.POST.get('title',None)
        author = request.POST.get('author',None)
        #session 获得user
        user_name = request.session.get('account',None)
        user = User.objects.filter(user_name=user_name)[0]

        type_id = request.POST.get('type_id',None)
        description = request.POST.get('description',None)

        '''上传文本'''
        objtext = request.FILES.get('upfiletxt',None)  #先拿到文件   然后需要把文件存入一个地方
        uploadDirPath = os.path.join(os.getcwd(),'static/books/text')
        if not os.path.exists(uploadDirPath):
            os.mkdir(uploadDirPath)  # 是否存在  不存在则添加文件夹
        # 拼接要上传的文件在服务器上的全路径
        postfix = os.path.splitext(objtext.name)[1]

        accept_type = ['.txt','.text']
        if not postfix in accept_type:
            return render(request,'users/add.html',{'msg':'文件类型不符'})

        objtext_u_name = str(uuid.uuid1())+postfix
        content_path = uploadDirPath + os.sep + objtext_u_name
 
        # 上传文件
        with open(content_path, 'wb+') as fp:
            for chunk in objtext.chunks():
                fp.write(chunk)      
        find_chaps(objtext_u_name,title)
        '''上传图片'''
        objimage = request.FILES.get('upfileimg',None)
        uploadDirPath = os.path.join(os.getcwd(),'static/books/picture')
        if not os.path.exists(uploadDirPath):
            os.mkdir(uploadDirPath)  # 是否存在  不存在则添加文件夹
        # 拼接要上传的文件在服务器上的全路径
        postfix = os.path.splitext(objimage.name)[1]

        accept_type = ['.jpg', '.jpeg', '.png','.PNG']
        if not postfix in accept_type:
            return render(request,'users/add.html',{'msg':'封面类型不符'})

        objimage_u_name = str(uuid.uuid1())+postfix
        content_path = uploadDirPath + os.sep + objimage_u_name
        # 上传文件
        with open(content_path, 'wb+') as fp:
            for chunk in objimage.chunks():
                fp.write(chunk)
        #路径
        text_path = 'books/text/'+ objtext_u_name
        picture_path = 'books/picture/'+ objimage_u_name

        Book.objects.create(
            title=title,
            author=author,
            uploader=user,
            type_id=type_id,
            description=description,
            content_path=text_path,
            image_path=picture_path
        )

        return render(request,'users/add.html',{'msg':'上传成功'})
    else:
        return render(request,'users/add.html')

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
    #获得当前浏览的书的对象
    book = Book.objects.get(book_id=book_id)
    #浏览加1
    view_number = book.view_number
    # book.update(view_number=view_number+1)
    Book.objects.filter(book_id=book_id).update(view_number=view_number+1)
    #获得评论
    comment_li = Comment.objects.filter(bookName=book).order_by('-create_time') 

    #获得当前用户对象
    user_name = request.session.get('account',None)
    if user_name!=None:
        user = User.objects.filter(user_name=user_name)[0]
        #更新用户的浏览记录
        L = json.loads(user.recent_read)
        for e in L:
            if e==book.book_id:
                L.remove(e)
                break
        L = [book.book_id]+L[:15]

        User.objects.filter(user_name=user.user_name).update(
            recent_read=json.dumps(L)
        )

        collection_li = Collection.objects.filter(user=user,book=book)
    else:
        user = None
        collection_li = [1] #没有用户的情况下，非空，不能收藏
    
    #上传者信息
    uploader = book.uploader

    download_number = uploader.download_number
    comment_number = len(Comment.objects.filter(userName=uploader))
    collect_number = len(Collection.objects.filter(user=uploader))

    if len(collection_li)==0:
        is_collected=0
    else:
        is_collected=1
    
    book_type = BOOKS_TYPE[int(book.type_id)]

    paginator = Paginator(comment_li,3) #每页显示6本
    #接受客户端发送的页码:
    page = request.GET.get('page',1)
    #
    try:
        comment_li=paginator.page(page)
    except EmptyPage:
        comment_li= paginator.page(1)
    except PageNotAnInteger:
        comment_li = paginator.page(paginator.num_pages)

    context = {
        'user':user,
        # 'uploader':uploader,
        'book':book,
        'book_type':book_type,
        'comment_li':comment_li,
        'is_collected':is_collected,
        'download_number':download_number,
        'comment_number':comment_number,
        'collect_number':collect_number
    }
    return render(request,'books/eachbook.html',context)

def filedownload(request, book_id):
    #增加下载量
    user_name = request.session.get('account',None)
    if user_name:
        user = User.objects.filter(user_name=user_name)[0]
        download_number = user.download_number
        User.objects.filter(user_name=user_name).update(
            download_number = download_number+1
        )
    else:
        return redirect('/users/login/')
    
# 定义一个内部函数分块读取下文件数据
    def fileIterator(downloadFilePath, chunkSize=512):
        # 读取二进制文件
        with open(downloadFilePath, 'rb') as fp:
            while True:
                content = fp.read(chunkSize)
                if content:
                    yield content
                else:
                    break

    #获得下载对象
    book = Book.objects.get(book_id = book_id)
    # 获取下载文件的全路径
    downloadFilePath = os.getcwd() + '/static/' + book.content_path

    #获得文件名
    filename = book.title + os.path.splitext(book.content_path)[1]

    # 响应客户端
    rep = StreamingHttpResponse(fileIterator(downloadFilePath))
    # 设置响应对象的关键值选项
    rep['Content-Type'] = 'application/octet-stream'
    rep['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return rep

def paihang(request):
    #session 获得user
    user_name = request.session.get('account',None)
    if user_name:
        user = User.objects.filter(user_name=user_name)[0]
    else:
        user = None

    new_list = Book.objects.get_all_ranking(limit=10,sort='new')
    n_new_list = new_list[3:]
    nn_new_list =  enumerate(n_new_list)
    nnn_new_list = [(k+4,v) for k,v in nn_new_list]
    view_list = Book.objects.get_all_ranking(limit=10,sort='view-hot')
    v_view_list = view_list[3:]
    vv_new_list = enumerate(v_view_list)
    vvv_view_list = [(k+4,v) for k,v in vv_new_list]
    collect_list = Book.objects.get_all_ranking(limit=10,sort='collect-hot')
    c_collect_list = collect_list[3:]
    cc_collect_list = enumerate(c_collect_list)
    ccc_collect_list = [(k+4,v) for k,v in cc_collect_list]
    context = {
        'user':user,
        'nnn_new_list': nnn_new_list,
        'new_list':new_list,
        'vvv_view_list':vvv_view_list,
        'view_list':view_list,
        'ccc_collect_list':ccc_collect_list,
        'collect_list':collect_list,
    }
    return render(request,'books/paihang.html',context)


def go_to_category(request, type_id, order_by):
    #session 获得user
    user_name = request.session.get('account',None)
    if user_name:
        user = User.objects.filter(user_name=user_name)[0]
    else:
        user = None
    if order_by == 'create_time':
        sort = '-create_time'
    elif order_by == 'view_number':
        sort = '-view_number'
    elif order_by == '-collection_number':
        sort = '-collection_number'
    else:
        sort ='-collection_number'
    book_li = Book.objects.filter(type_id=type_id).order_by(sort)

    paginator = Paginator(book_li,3) #每页显示6本
    #接受客户端发送的页码:
    page = request.GET.get('page',1)
    #
    try:
        book_li=paginator.page(page)
    except EmptyPage:
        book_li= paginator.page(1)
    except PageNotAnInteger:
        book_li = paginator.page(paginator.num_pages)

    return render(request, "books/class.html", {'user':user,'book_li':book_li, 'type_id': type_id})