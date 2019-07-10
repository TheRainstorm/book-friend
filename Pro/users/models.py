from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash

# from books.models import Book

# Create your models here.
class PassportManager(models.Manager):
    def add_one_passport(self, username, password, image):
        '''添加一个账户信息'''
        user = self.create(user_name=username, password=get_hash(password), image=image)
        # 3.返回passport
        return user

    def get_one_passport(self, username, password):
        '''根据用户名密码查找账户的信息'''
        try:
            user = self.get(user_name=username, password=get_hash(password))
        except self.model.DoesNotExist:
            # 账户不存在
            user = None
        return user

class User(BaseModel):
    '''用户模型类'''
    user_id = models.AutoField(primary_key=True, verbose_name='用户的id')
    recent_read = models.CharField(max_length=100,default="[]",verbose_name='最近浏览')
    image = models.CharField(max_length=200)
    user_name = models.CharField(max_length=20, unique=True, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')

    signature = models.CharField(max_length=100,default="",verbose_name='个性签名')
    gender = models.CharField(max_length=10,default="male", verbose_name='性别')

    download_number = models.IntegerField(default=0,verbose_name='下载量')
    #用户的管理表
    objects = PassportManager()
    
    # class Meta:
    #     db_table = 's_user_account'