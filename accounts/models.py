from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))


class Address(models.Model):
    user=models.ForeignKey(to=User , on_delete=models.CASCADE)
    locality=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    state=models.CharField(choices=STATE_CHOICES,max_length=255)
    pincode=models.PositiveIntegerField()

    class Meta:
        verbose_name_plural='addresses'
    def __str__(self):
        return str(self.user)

PRODUCT_CHOICES = (
    ('Electronics','Electronics'),
    ('Fashion','Fashion'),
    ('Books','Books'),
)

class Product(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=7 , decimal_places=2)
    category=models.CharField(choices=PRODUCT_CHOICES,max_length=255)
    image=models.ImageField(upload_to='productimages')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='products'

class Cart(models.Model):
    user=models.ForeignKey(to=User , on_delete=models.CASCADE , related_name='user_user')
    product=models.ForeignKey(to=Product , on_delete=models.CASCADE,related_name='product_cart')
    qty=models.PositiveIntegerField(default=1)

STATUS_CHOICES=(
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('OnTheWay','OnTheWay'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(to=User , on_delete=models.CASCADE)
    product=models.ForeignKey(to=Product,on_delete=models.CASCADE)
    address=models.ForeignKey(to=Address , on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100 , choices=STATUS_CHOICES , default='Pending')