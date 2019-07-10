from django.db import models
from books.enums import *
from db.base_model import BaseModel

# from users.models import User

# Create your models here.
class BooksManager(models.Manager):
    def get_books_by_id(self, books_id):
        '''根据商品的id获取商品信息'''
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            # 不存在商品信息
            books = None
        return books
    # sort='new' 按照创建时间进行排序
    # sort='hot' 按照商品销量进行排序
    # sort='price' 按照商品的价格进行排序
    # sort='default' 按照默认顺序排序
    def get_books_by_type(self, type_id, limit=None, sort='default'):
        '''根据商品类型id查询商品信息'''
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'view-hot':
            order_by = ('-view_number', )
        elif sort == 'collect-hot':
            order_by = ('-collection_number',)
        else:
            order_by = ('-pk', ) # 按照primary key降序排列。

        # 查询数据
        books_li = self.filter(type_id=type_id).order_by(*order_by)

        # 查询结果集的限制
        if limit:
            books_li = books_li[:limit]
        return books_li

    def get_all_ranking(self, limit=None,sort='default'):
            if sort == 'new':
                order_by = ('-create_time',)
            elif sort == 'view-hot':
                order_by = ('-view_number', )
            elif sort == 'collect-hot':
                order_by = ('-collection_number',)
            else:
                order_by = ('-pk', ) # 按照primary key降序排列。

            # 查询数据
            books_li = self.order_by(*order_by)

            # 查询结果集的限制
            if limit:
                books_li = books_li[:limit]
            return books_li

class Book(BaseModel):
    '''书籍模型类'''
    # 标题
    # 作者
    # 上传者（FK）
    # 上传时间
    # 类别
    # 标签[50]
    # 简介
    # 内容（路径）
    # 封面（路径）
    # 浏览量
    # 收藏量
    books_type_choices = ((k, v) for k,v in BOOKS_TYPE.items())

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, verbose_name='书籍标题')
    author = models.CharField(max_length=20, verbose_name='书籍作者')
    uploader = models.ForeignKey('users.User',on_delete=models.CASCADE, verbose_name='上传者')

    type_id = models.SmallIntegerField(default=1,choices=books_type_choices, verbose_name='书的种类')
    # tag = models.CharField(max_length=1024,verbose_name='标签') #暂时
    description = models.CharField(max_length=128, verbose_name='简介')

    content_path = models.CharField(max_length=200, verbose_name='书籍保存路径')
    image_path = models.CharField(max_length=200, default='static/books/pic.jpg', verbose_name='封面保存路径')

    view_number = models.IntegerField(default=0,verbose_name='浏览量')
    collection_number = models.IntegerField(default=0,verbose_name='收藏量')

    objects = BooksManager()
    # admin显示书籍的名字
    def __str__(self):
        return self.title