from django.db import models

# Create your models here.
class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User',on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book',on_delete=models.CASCADE)