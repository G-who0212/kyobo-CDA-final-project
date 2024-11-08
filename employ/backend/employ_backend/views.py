import requests
from django.shortcuts import render
from django.http import Http404

# Create your views here.
def login(request):
    return render(request,'login.html')

def employ(request):
    return render(request,'employ.html')

def employdetail(request, pk):
    url = f'http://127.0.0.1:8000/api/applicationsall/applications/{pk}/'
    # headers = {
    #     'Authorization': f'Bearer {request.session.get("accessToken")}',  # 세션이나 쿠키에 저장된 accessToken을 불러와 Authorization 헤더에 추가
    # }
    
    try:
        response = requests.get(url)
        print(f"response.json() {response.json()}")
        response.raise_for_status()  # 요청에 실패하면 HTTPError를 발생시킴
        applicant_data = response.json()  # JSON 데이터를 파이썬 딕셔너리로 변환
    except requests.exceptions.RequestException as e:
        print(f"Error fetching applicant data: {e}")
        raise Http404("지원자를 찾을 수 없습니다.")
    
    return render(request, 'employdetail.html', {'applicant': applicant_data})