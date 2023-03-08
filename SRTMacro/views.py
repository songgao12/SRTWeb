from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.forms import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect
from SRT.constants import STATION_CODE
# Create your views here.
from django.contrib.auth import get_user_model, login
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import RequestContext
from SRT import SRT
from SRT.errors import *
import asyncio
def print_page(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'Login.html')
def login_auth(request):
    if request.method == 'POST':
        try:
            srt = SRT(request.POST['username'].strip(), request.POST['password'])
            request.session['user'] = request.POST['username'].strip()
            request.session['password'] = request.POST['password']
            user = User.objects.get(username='test')
            login(request, user=user)
            return render(request, 'index.html')
        except SRTLoginError as e:
            messages.warning(request, e.__str__())
    return redirect('/login')

def login_page(request):
    return render(request, 'Login.html')

def page_not_found_view(request,exception):
    return render(request, 'error_page.html', RequestContext(request))

def server_error(request):
    return render(request, 'error_page.html')
def csrf_error(request,reason=""):
    return render(request, 'error_page.html')
def srt_list_join(request):

    try:
        dep = request.GET['dptRsStnCd']
        arr = request.GET['arvRsStnCd']
        date = request.GET['datePicker']
        tm = request.GET['dptTm']
        srt = SRT(request.session['user'], request.session['password'])
        srtTrains = srt.search_train(dep, arr, date, tm, available_only=False)
        datetime_date = datetime.strptime(srtTrains[0].arr_date, '%Y%m%d')
        dt = datetime_date.strftime('%Y년 %m월 %d일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        dateDict = {0: '(월)', 1: '(화)', 2: '(수)', 3: '(목)', 4: '(금)', 5: '(토)', 6: '(일)'}
        searchDate=dt+dateDict[datetime_date.weekday()]
        return render(request, 'srtJoin.html', {'srtTrains': srtTrains, 'searchDate':searchDate,'dep':dep,'arr':arr,'dptTm':tm})
    except:
        return render(request, 'srtJoin.html')



def srt_macro(request):
    arr_time = request.GET.get('arr_time')
    dep_time = request.GET.get('dep_time')
    dep = request.GET.get('dep')
    arr = request.GET.get('arr')
    date = request.GET.get('date')
    try:
        srt = SRT(request.session['user'], request.session['password'])
        trains = srt.search_train(STATION_CODE[dep], STATION_CODE[arr], date, "050000",dep_time)
        for train in trains:
            if train.dep_time in dep_time:
                reservation = srt.reserve(train)
                return render(request, 'check.html', {'check':"예약 성공!"})
    except Exception as e:
        return render(request, 'check.html', {'check':e})
    #
     #   break
    return render(request, 'check.html', {'check':"false"})