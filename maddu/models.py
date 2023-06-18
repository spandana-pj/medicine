from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Medicine(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    medicine_name=models.CharField(max_length=50)
    medicine_desc=models.TextField()
    medicine_img=models.ImageField(upload_to="medicines")