from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import redirect
from application.SRT.srt import STATION_CODE, SRT
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import RequestContext
from application.SRT.errors import *


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
        now = datetime.now()
        if datetime.strptime(date+tm, '%Y%m%d%H%M%S') < datetime.now():
            tm = now.strftime('%H%M%S')
        srt = SRT(request.session['user'], request.session['password'])
        srtTrains = srt.search_train(dep, arr, date, tm, available_only=False)
        datetime_date = datetime.strptime(srtTrains[0].arr_date, '%Y%m%d')
        dt = datetime_date.strftime('%Y년 %m월 %d일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        dateDict = {0: '(월)', 1: '(화)', 2: '(수)', 3: '(목)', 4: '(금)', 5: '(토)', 6: '(일)'}
        searchDate=dt+dateDict[datetime_date.weekday()]
        return render(request, 'srtJoin.html', {'srtTrains': srtTrains, 'searchDate':searchDate,'dep':dep,'arr':arr,'dptTm':tm})
    except:
        return render(request, 'srtJoin.html')



async def srt_macro(request):
    arr_time = request.GET.get('arr_time')
    dep_time = request.GET.get('dep_time')
    dep = request.GET.get('dep')
    arr = request.GET.get('arr')
    date = request.GET.get('date')

    try:
        srt = SRT(request.session['user'], request.session['password'])
        trains = srt.search_train_one(STATION_CODE[dep], STATION_CODE[arr], date, dep_time,dep_time)

        for train in trains:
            if train.dep_time in dep_time:
                reservation = srt.reserve(train)
                return JsonResponse({'msg':'예약 성공!'})
    except Exception as e:
        return JsonResponse({'msg':e.__str__})
    return JsonResponse({'msg':'false'}) #render(request, 'check.html', {'check':"false"})