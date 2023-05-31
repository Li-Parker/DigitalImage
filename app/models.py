from django.db import models


# Create your models here.
class Users(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', max_length=32, null=False)
    imageCount = models.IntegerField('上传照片数量', default=0)

    class Meta:
        db_table = 'users'


class Images(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('图片名称', max_length=255)
    img = models.ImageField('图片数据', null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column="user_id")

    class Meta:
        db_table = 'images'
