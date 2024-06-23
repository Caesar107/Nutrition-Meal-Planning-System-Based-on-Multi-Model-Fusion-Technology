"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from mysite import settings
from app.views import *
# from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls'), name='user'), # 用户
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')), # 引入ckeditor
    path('captcha/', include('captcha.urls')), # 验证码
    # path('', TemplateView.as_view(template_name='app/index.html')),
    path('', index, name='index'),
    path('recom/', item_pred, name='recom'),
    path('accept/<int:data_id>', accept, name='accept'),
    path('reject/<int:data_id>', dislike, name='reject'),
    # path("api/", api.urls), # 引入restful
    path("__debug__/", include("debug_toolbar.urls")), # 调试信息
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL) # 配置静态资源的路径
