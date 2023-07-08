from django.db import models
from django.utils import timezone
from datetime import date
import datetime
from django.contrib.auth.models import User, Group

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    department  = models.CharField(max_length=30)  #부서
    agency  = models.CharField(max_length=30, default='')  #기관
    phone  = models.CharField(max_length=20, default='')  #연락처

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)  # Set default value to current date and time
    updated_at = models.DateField(auto_now=True)  # Automatically update on each save
    construction_type = models.CharField(max_length=100)
    start_at = models.DateField(null=True)  # DateField for construction start date
    end_at = models.DateField(null=True)  # DateField for construction end date
    content = models.TextField()
    department  = models.CharField(max_length=30, null=True)  #부서
    agency  = models.CharField(max_length=30, null=True)  #기관
    phone  = models.CharField(max_length=20, null=True)  #연락처
    def get_construction_status(self):
        today = timezone.now().date()

        if self.start_at and self.end_at:
            if today < self.start_at:
                return '공사예정'
            elif self.start_at <= today <= self.end_at:
                return '공사중'
            else:
                return '공사완료'
        else:
            return ''


    def __str__(self):
        return self.construction_type
    

    @classmethod
    def get_weekly_constructions(cls):
        today = datetime.date.today()
        weekday = today.weekday() 
        start_of_week = today - datetime.timedelta(days=weekday)  
        end_of_week = start_of_week + datetime.timedelta(days=6)  
        return cls.objects.filter(start_at__range=[start_of_week, end_of_week]).count()



    @classmethod
    def get_daily_constructions(cls):  #금일진행
        today = date.today()
        return cls.objects.filter(start_at=today).count()

    @classmethod
    def get_registered_constructions(cls):  #신규접수
        today = date.today()
        return cls.objects.filter(created_at=today).count()