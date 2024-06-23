from .models import *
from app.models import Data, UserVisit
from loguru import logger
from django.db.transaction import atomic
import datetime
import random

def get_gender():
    genders = ['F', 'M']
    return random.choice(genders)

def get_age():
    return random.randint(40, 70)

@atomic
def gen_user_dataset():
    k = 100
    password = 'user123456'
    for i in range(1, k+1):
        username = f'user.fake.{i}'
        User.objects.filter(username=username).delete()
        # 生成用户
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = 1
        user.is_active = 1
        user.save()
        # 加入普通用组
        user.groups.add(1)
        # 生成用户信息
        gender = get_gender()
        age = get_age()
        profile = Profile.objects.create(user=user, gender=gender, age=age)
        profile.save()
        logger.info(f'{username} 创建成功')

@atomic
def change_password():
    k = 100
    password = 'user123456'
    for i in range(1, k+1):
        username = f'user.fake.{i}'
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        logger.success(f'{username} 密码已修改')

@atomic
def gen_visit_dataset():
    UserVisit.objects.all().delete()
    logger.success('用户推荐记录已删除')
    # 创建用户浏览记录
    for user in User.objects.filter(username__contains='user.fake'):
        # 为每一个用户随机创建K个浏览记录
        k = random.randint(1, 1000)
        for i in range(1, k+1):
            # 随机选择一个物品
            data = Data.objects.order_by('?').first()
            # 随机选择1个分数
            score = random.randint(1, 5)
            # 随机选择一个时间
            create_at = datetime.datetime.now()
            # 创建浏览记录
            UserVisit.objects.create(user=user, data=data, rating=score, visit_time=create_at)
        logger.info(f'{user.username} 创建成功')

@atomic
def gen_user_health_dataset():
    HealthIndex.objects.all().delete()
    logger.success('用户健康记录已删除')
    # 创建用户浏览记录
    for user in User.objects.filter(username__contains='user.fake'):
        # 为每一个用户创建10个浏览记录
        # 创建10个日期
        dates = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(10)]
        for date in dates:
            logger.info(date)
            # 生成随机小数
            weight = round(random.uniform(50, 52), 2)
            # 生成血糖数据
            blood_sugar = round(random.uniform(3.9, 4.9), 2)
            # 生成血压
            blood_pressure = round(random.uniform(120, 130), 2)
            # 生成心率
            heart_rate = round(random.uniform(60, 100), 2)
            HealthIndex(user=user, date=date, weight=weight, blood_sugar=blood_sugar, blood_pressure=blood_pressure, heart_rate=heart_rate).save()
        logger.info(f'{user.username} 创建成功')