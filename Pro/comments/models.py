from django.db import models

from db.base_model import BaseModel
# Create your models here.
class Comment(BaseModel):
    commentId = models.AutoField(primary_key=True) # 主键自动增长
    userName = models.ForeignKey('users.User',on_delete=models.CASCADE) #外键约束
    bookName = models.ForeignKey('books.Book',on_delete=models.CASCADE)#外键约束
    content = models.CharField(max_length=300,verbose_name='评论内容')#内容