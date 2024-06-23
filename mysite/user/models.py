from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女')
    ]
    gender = models.CharField(max_length=10, verbose_name='性别', choices=GENDER_CHOICES)
    age = models.IntegerField(verbose_name='年龄')

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

# 用户健康指标
class HealthIndex(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    weight = models.FloatField(verbose_name='体重', null=True, blank=True)
    # 血糖
    blood_sugar = models.FloatField(verbose_name='血糖', null=True, blank=True)
    # 血压
    blood_pressure = models.FloatField(verbose_name='血压', null=True, blank=True)
    # 心率
    heart_rate = models.FloatField(verbose_name='心率', null=True, blank=True)

    class Meta:
        verbose_name = '用户健康指标'
        verbose_name_plural = '用户健康指标'
    