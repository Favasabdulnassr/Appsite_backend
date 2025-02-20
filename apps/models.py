from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
import os

User = get_user_model()


class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image', folder='android_apps')
    app_link  = models.URLField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    points = models.IntegerField(validators=[MinValueValidator(0)],null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.image:
            return f"https://res.cloudinary.com/{os.getenv('CLOUD_NAME')}/{self.image}"
        return None
    

class CompletedTask(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    app = models.ForeignKey(AndroidApp,on_delete=models.CASCADE)
    screenshot =  CloudinaryField('screenshot', folder='screenshots') 
    is_verified = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','app')

    def get_screenshot_url(self):
        if self.screenshot:
            return f"https://res.cloudinary.com/{os.getenv('CLOUD_NAME')}/{self.screenshot}"
        return None    
        
