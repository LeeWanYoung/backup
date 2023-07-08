from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User

class VOC(models.Model):
    REPAIR_STATUS_CHOICES = [
        ('수리중', '수리중'),
        ('수리완료', '수리완료'),
        ('수리전', '수리전'),
    ]

    VOC_STATUS_CHOICES = [
        ('확인중', '확인중'),
        ('확인완료', '확인완료'),
        ('추가조치필요', '추가조치필요'),
        ('발송전', '발송전'),
    ]


    phone = models.CharField(max_length=20) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    tt = models.CharField(max_length=30) 
    updated_at = models.DateField(auto_now=True)
    repair_status = models.CharField(max_length=100, choices=REPAIR_STATUS_CHOICES)
    voc_status = models.CharField(max_length=100, choices=VOC_STATUS_CHOICES, null=True)
    comment = models.TextField(max_length=100, blank=True, null=True) #사용자의견
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.phone
    

    @classmethod
    def get_preparing_vocs(cls):
        return cls.objects.filter(voc_status='발송전').count()

    @classmethod
    def get_processing_vocs(cls):
        return cls.objects.filter(voc_status='확인중').count()

    @classmethod
    def get_reprocessing_vocs(cls):
        return cls.objects.filter(voc_status='추가조치필요').count()

    @classmethod
    def get_completed_vocs(cls):
        return cls.objects.filter(voc_status='확인완료').count()