from django.db import models
import datetime
import uuid
from django.contrib.auth.models import User
# Create your models here.
# class UserAdministrators(models.Model):
    # name = models.CharField(max_length=20)
    # username = models.CharField(max_length=50)
    # email = models.CharField(max_length=100)
    # phone = models.CharField(max_length=12)
    # adress = models.TextField()
    # date_create = models.DateTimeField(default=datetime.datetime.now())
    
    
#*************************************************** MODEL VỀ SẢN PHẨM VÀ LOẠI SẢN PHẨM *************************************************************************************

class Category(models.Model):
    name = models.CharField(null=False,blank=False,max_length=20)
    def __str__(self) -> str:
        return f'{self.name}-{self.id}'
        
class Product(models.Model):
    title = models.CharField(default='',max_length=100)
    selling_price = models.FloatField(default='',blank=True,null=True)
    discounted_price = models.FloatField(default='')
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    product_image = models.ImageField(upload_to='product')
    def __str__(self) -> str:
        return f'{self.id}-{self.title}'
class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    adress = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    def __str__(self) -> str:
        return f'{self.name}'
# ***************************************************token reset password**************************************************************
class TokenReset(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User,related_name='token_reset',on_delete=models.CASCADE)
# ****************************************************        CART       ***************************************************************************
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
# *******************************************************   TOKEN REGISTER  ************************************************************
class TokenRegister(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)