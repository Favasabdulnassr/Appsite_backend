from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='android_apps/', blank=True, null=True)
    app_link  = models.URLField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    points = models.IntegerField(validators=[MinValueValidator(0)],null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.name
    

class CompletedTask(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    app = models.ForeignKey(AndroidApp,on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screeshots/')
    is_verified = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','app')
        
