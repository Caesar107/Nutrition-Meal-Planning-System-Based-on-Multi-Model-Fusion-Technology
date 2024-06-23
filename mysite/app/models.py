from django.db import models
from user.models import User
from django.utils.html import format_html

# Create your models here.
class Data(models.Model):
    title = models.CharField(max_length=200, verbose_name='名称')
    rating = models.FloatField(null=True, blank=True, verbose_name='评分')
    calories = models.IntegerField(null=True, blank=True, verbose_name='卡路里')
    protein = models.FloatField(null=True, blank=True, verbose_name='蛋白质')
    fat = models.FloatField(null=True, blank=True, verbose_name='脂肪')
    sodium = models.FloatField(null=True, blank=True, verbose_name='钠含量')
    categories = models.CharField(max_length=200, null=True, blank=True, verbose_name='菜品配料与描述')

    @property
    def show_info(self):
        return format_html(
            f'''
              <div class="card mt-3 card-primary">
                <div class="card-header">
                  {self.title}
                 </div>
                <div class="card-body">
                  <p>评分：{self.rating}</p>
                  <p>卡路里：{self.calories}</p>
                  <p>蛋白质：{self.protein}</p>
                  <p>脂肪：{self.fat}</p>
                  <p>钠含量：{self.sodium}</p>
                  <p>菜品配料与描述：{self.categories}</p>
                </div>
                <div class="card-footer">
                  <a href="/accept/{self.id}" class="btn btn-primary btn-sm">接受</a> 
                  <a href="/reject/{self.id}" class="btn btn-danger btn-sm">拒绝</a> 
                </div>
              </div>
            '''
        )
        
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '菜肴'
        verbose_name_plural = verbose_name

class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    data = models.ForeignKey(Data, on_delete=models.CASCADE, verbose_name='菜品')
    visit_time = models.DateTimeField(verbose_name='时间')
    rating = models.FloatField(verbose_name='评分')

    class Meta:
        verbose_name = '用户推荐记录'
        verbose_name_plural = verbose_name
    
        
    def __str__(self):
        return self.user.username + '-' + self.data.name