from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import JsonResponse
from loguru import logger
from mysite.settings import SITE_NAME
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import datetime

# Create your views here.
@logger.catch
def index(request):
    return render(request, 'app/index.html')
    return HttpResponse(SITE_NAME)

import requests

def get_recom(user_id):
    try:
        #sentence = '7家涉房股东被执行额逾14亿元 朝阳银行陷业绩股权双困'

        r = requests.post('http://127.0.0.1:5000/predict', data={'user_id': user_id}).json()
        logger.success(r)
        return r.get('items_idx')
    except Exception as e:
        return []

@login_required
def item_pred(request):
    """
    推荐
    """
    user_id = request.user.id
    try:
        items_idx = get_recom(user_id)
        logger.warning(items_idx)
        items = Data.objects.filter(id__in=items_idx)
        if items.count() == 0:
            items = Data.objects.all().order_by('?')[:10]
    except Exception as e:
        logger.error("推荐引擎出错: " + str(e))
        items = Data.objects.all().order_by('?')[:10]

    return render(request, 'app/recom.html', {'items': items})

@login_required
def accept(request, data_id):
    UserVisit.objects.create(user_id=request.user.id, data_id=data_id, visit_time=datetime.datetime.now(), rating=5).save()
    messages.success(request, '已接受')
    return redirect('index')

@login_required
def dislike(request, data_id):
    data = get_object_or_404(Data, id=data_id)
    # todo 
    messages.success(request, '已拒绝')
    return redirect('index')
