from rest_framework import serializers
from .models import AndroidApp,CompletedTask
from users.models import CustomUser

class AndroidAppSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.get_image_url()
    
    class Meta:
        model = AndroidApp
        fields = ['id','name','app_link','category','sub_category','points','created_at','updated_at','image','image_url']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','phone_number','first_name','last_name','total_points','role']
        read_only_fields = ['email','total_points','role']


class CompletedTaskSerilizer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name',read_only=True)
    app_points = serializers.IntegerField(source='app.points',read_only=True)
    user_name = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email',read_only=True)
    screenshot_url = serializers.SerializerMethodField()



    def get_user_name(self, obj):
        return f"{obj.user.first_name} ".strip() or obj.user.email
    

    def get_screenshot_url(self, obj):
        return obj.get_screenshot_url()


    class Meta:
        model = CompletedTask
        fields = ['id', 'app', 'app_name', 'app_points', 'screenshot',' screenshot_url', 'is_verified', 'completed_at','user_name','user_email']
        read_only_fields = ['is_verified']
