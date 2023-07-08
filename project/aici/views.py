from io import BytesIO
import time
from django.shortcuts import render
from django.http import HttpResponse
from Gongsa.models import Post
from aici.models import VOC
from datetime import datetime
from datetime import date, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import requests
import json
from django.http import JsonResponse
import base64
import hashlib
import hmac
import pandas as pd
from openpyxl import Workbook
import pickle

import pandas as pd
import numpy as np
import os
from django.conf import settings
from konlpy.tag import Mecab
#123
def classify_emotion(text):
    with open('/mnt/c/Users/User/Desktop/AICI1/AI_8_31/wv_model.pt', 'rb') as fr:
        wv_model = pickle.load(fr)
    with open('/mnt/c/Users/User/Desktop/AICI1/AI_8_31/ML_model.pt', 'rb') as fr:
        ml_model = pickle.load(fr)

    mecab = Mecab()
    
    my_word=mecab.morphs(text)
    feature_vec = np.zeros((200), dtype="float32")
    n_words = 0
    for word in my_word:
        if word in wv_model.wv.key_to_index:
            n_words += 1
            # 임베딩 벡터에 해당 단어의 벡터를 더함
            feature_vec = np.add(feature_vec, wv_model.wv[word])
    # 단어 개수가 0보다 큰 경우 벡터를 단어 개수로 나눠줌 (평균 임베딩 벡터 계산)
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    tmp=[]
    tmp.append(feature_vec)
    # 입력된 내용을 감정 분류 모델로 분석하여 결과를 반환
    result = ml_model.predict(tmp)
    return 'positive' if result == 0 else 'negative'

def chatbot(request, phone):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        voc = VOC.objects.get(phone=phone)
        voc.comment = comment

        # 감정 분류 모델을 사용하여 입력된 내용을 분석하여 결과에 따라 voc_status 변경
        emotion = classify_emotion(comment)
        if emotion == 'positive':
            voc.voc_status = '최종완료'
            voc.delete()  # 데이터 삭제
            voc.save()  # 변경사항 저장   
        else:
            voc.voc_status = '추가조치필요'

        voc.save()  # 변경사항 저장

        if emotion == 'positive':
            return redirect('aici:positive')
        else:
            return redirect('aici:negative')
    else:
        voc = VOC.objects.get(phone=phone)
        return render(request, 'aici/chatbot.html', {'voc': voc})
    

def chat(request):
    if request.method == 'POST':
        response_text = request.POST['comment']
        if response_text == '네':
            return redirect('aici:positive')
        elif response_text == '아니오':
            return redirect('aici:negative')
    return render(request, 'aici/chat.html')

# @login_required
# def chatbot(request, phone):
#     if request.method == 'POST':
#         comment = request.POST.get('comment')
#         voc = VOC.objects.get(phone=phone)
#         voc.comment = comment

#         if comment.lower() == '네':
#             voc.voc_status = '확인완료'
#             voc.delete()  # 데이터 삭제
#             voc.save()  # 변경사항 저장            
#             return redirect('aici:positive')
#         elif comment.lower() == '아니오':
#             voc.voc_status = '추가조치필요'
#             voc.save()  # 변경사항 저장
#             return redirect('aici:negative')
#         else:
#             voc.save()  # 변경사항 저장

#             return redirect('aici:chat', phone=phone)
#     else:
#         voc = VOC.objects.get(phone=phone)
#         return render(request, 'aici/chatbot.html', {'voc': voc})


def positive(request):
    # positive 뷰의 내용을 작성하세요
    return render(request, 'aici/positive.html')

def negative(request):
    # negative 뷰의 내용을 작성하세요
    return render(request, 'aici/negative.html')

class AiciLoginView(LoginView):
    template_name = 'aici/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name='aici').exists():
                # gongsa 그룹에 있는 사용자인 경우 로그인 처리
                login(self.request, user)
                return redirect('aici:main')  # 로그인 후 리디렉션할 페이지
            elif user.groups.filter(name='gongsa').exists():
                # aici 그룹에 있는 사용자인 경우 로그인 거부
                error_message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
                return render(self.request, 'aici/login.html', {'error_message': error_message})
        else:
            # 인증 실패
            error_message = 'Invalid credentials.'
            return render(self.request, 'aici/login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('aici:login')

@login_required
def main(request):
    
    xData_gongsa, yData_gongsa = gongsa_graph(request)
    xData_voc, yData_voc = voc_graph(request)

    registered_constructions = Post.get_registered_constructions()
    daily_constructions = Post.get_daily_constructions()
    weekly_constructions = Post.get_weekly_constructions()

    preparing_vocs = VOC.get_preparing_vocs()
    processing_vocs = VOC.get_processing_vocs()
    reprocessing_vocs = VOC.get_reprocessing_vocs()
    completed_voc = VOC.get_completed_vocs()


    context = {
        'registered_constructions': registered_constructions,
        'daily_constructions': daily_constructions,
        'weekly_constructions': weekly_constructions,
        'preparing_vocs': preparing_vocs,
        'processing_vocs': processing_vocs,
        'reprocessing_vocs': reprocessing_vocs,
        'completed_voc': completed_voc,
        'xData_gongsa': xData_gongsa,
        'yData_gongsa': yData_gongsa,
        'xData_voc': xData_voc,
        'yData_voc': yData_voc,
    }
    return render(request, 'aici/main.html', context)



@login_required
def voc(request):
    voc_data = VOC.objects.filter(author=request.user).order_by('-created_at', '-id')
    context = {
        'voc_data': voc_data
    }
    return render(request, 'aici/voc.html', context)

from django.db.models import Q

@login_required
def work(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_at')
        end_date = request.GET.get('end_at')
        posts = Post.objects.all()
        error_message = ""

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            posts = posts.filter(Q(start_at__range=[start_date, end_date]) | Q(end_at__range=[start_date, end_date]))
        elif start_date:
            error_message = "종료일을 선택해주세요."
        elif end_date:
            error_message = "시작일을 선택해주세요."

        context = {'posts': posts, 'start_date': start_date, 'end_date': end_date, 'error_message': error_message}
    else:
        context = {}

    return render(request, 'aici/work.html', context)

@login_required
def edit_voc(request):
    voc = VOC.objects.first()  # 가져올 VOC 인스턴스를 선택하는 방법에 따라 적절한 쿼리를 사용합니다.
    comment = voc.comment if voc else None

    context = {
        'comment': comment,
    }


    return render(request, 'aici/edit_voc.html', context)


@login_required
def gongsa_graph(request):
    today = date.today()
    end_date = today + timedelta(days=6)

    xData = [str(today + timedelta(days=i)) for i in range((end_date - today).days + 1)]

    yData = [Post.objects.filter(start_at=date_val).count() for date_val in xData]

    # Check if today's date is in xData
    if str(today) not in xData:
        xData.append(str(today))
        yData.append(0)

    return xData, yData

@login_required
def voc_graph(request):
    current_datetime = timezone.now()
    start_datetime = current_datetime.replace(minute=0, second=0, microsecond=0) - timezone.timedelta(hours=23)
    end_datetime = current_datetime.replace(minute=0, second=0, microsecond=0) + timezone.timedelta(hours=1)

    xData = []
    yData = []

    for i in range(24):
        hour_start = start_datetime + timezone.timedelta(hours=i)
        hour_end = start_datetime + timezone.timedelta(hours=i+1)

        count = VOC.objects.filter(
            voc_status__in=['발송전', '추가조치필요'],
            created_at__gte=hour_start,
            created_at__lt=hour_end
        ).count()
        xData.append(hour_start.strftime("%H"))
        yData.append(count)

    # # 현재 시간
    # xData.append(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    # yData.append(VOC.objects.filter(voc_status__in=['발송전', '확인중', '추가조치필요'], created_at__range=(end_datetime, current_datetime)).count())

    return xData, yData



def send_mms_proxy(request):
    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/" + "ncp:sms:kr:310425331464:mms_chat" + "/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = "43Q01oRn0O7n6hgLV0xi"
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign)
    
    voc_status = '확인중'
    data = json.loads(request.body)
    selected_phone_numbers = data.get('phone_numbers', [])
    for phone_number in selected_phone_numbers:
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': access_key,
            'x-ncp-apigw-signature-v2': signature
        }

    
        body = {
            "type": "LMS",
            "countryCode": "82",
            "from": "01044339761",
            "subject": "MMS 제목",
            "contentType": "COMM",
            "content": "MMS 내용",
            "messages": [
                {
                    "subject": "테스트",
                    "content": "[KT안내] KATI 안내\n고객님,안녕하세요. KT입니다.\nKATI가 도착하였습니다.KATI에게 의견을 남겨주세요\n☞KATI\nhttps://e6f6-2001-2d8-6363-6ab6-d13d-6ceb-678c-fbf3.ngrok-free.app/aici/chatbot/01056706136\n감사합니다.\n[마음을 담다,DIGICO KT]",
                    "to": phone_number,
                }
            ]
        }
        try:
            vocs = VOC.objects.filter(phone=phone_number)
            for voc in vocs:
                voc.voc_status = voc_status
                voc.save()
        except VOC.DoesNotExist:
            return JsonResponse({"status": "error", "message": "VOC 객체를 찾을 수 없습니다."})
    
        body = json.dumps(body)
        response = requests.post(api_url, headers=headers, data=body)

        # if response.status_code == 200:
        #     print(f"MMS sent successfully to {phone_number}")
        # else:
        #     print(f"Failed to send MMS to {phone_number}. Error: {response.text}")

    message = f"메시지가 전송되었습니다."
    return JsonResponse({"status": "error", 'message': message}, status=200)

def make_signature(string):
    secret_key = bytes("aWwoibbxIHwnzuYD30PqvYGeOYbLX6Rto3y9TaUx", 'UTF-8')
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64

@login_required
def gongsa_excel(request):
    # 데이터베이스에서 모든 항목 가져오기
    posts = Post.objects.all()

    # 데이터를 DataFrame으로 변환
    data = {
        '#': [i + 1 for i, post in enumerate(posts)],
        '접수기관': [post.author.profile.agency for post in posts],
        '담당자': [str(post.author) for post in posts],
        '연락처': [post.author.profile.phone for post in posts],
        '공사종류': [post.construction_type for post in posts],
        '공사기간': [f"{post.start_at} ~ {post.end_at}" for post in posts],
        '공사완료여부': [post.get_construction_status for post in posts]
    }
    df = pd.DataFrame(data)

    # 엑셀 파일 생성
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Gongsa Data', header=True)  # 수정된 부분

    # 파일 저장
    writer.save()

    # 파일 응답 생성
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=gongsalist_data.xlsx'
    response.write(output.getvalue())

    return response

@login_required
def voc_excel(request):
    # 데이터베이스에서 모든 VOC 데이터 가져오기
    voc_data = VOC.objects.all()

    # 데이터를 DataFrame으로 변환
    data = {
        'TT 번호': [voc.tt for voc in voc_data],
        '전화번호': [voc.phone for voc in voc_data],
        '수리현황': [voc.repair_status for voc in voc_data],
        'voc현황': [voc.voc_status for voc in voc_data],
        '사용자의견': [voc.comment for voc in voc_data],
    }
    df = pd.DataFrame(data)

    # 엑셀 파일 생성
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='VOC Data', header=True)

    # 파일 저장
    writer.save()

    # 파일 응답 생성
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=voc_data.xlsx'
    response.write(output.getvalue())

    return response

