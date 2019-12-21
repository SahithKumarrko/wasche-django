from django.db import models

# Create your models here.
class College(models.Model):
    college_name = models.CharField(max_length=254,primary_key=True,unique=True)
    college_address = models.CharField(max_length = 254)
    college_phone_number = models.CharField(max_length = 20)
    college_zip_code = models.CharField(max_length = 15)
    college_country = models.CharField(max_length=100)
    college_state = models.CharField(max_length = 100)
    
    class Meta:
        verbose_name_plural = "Colleges"
    