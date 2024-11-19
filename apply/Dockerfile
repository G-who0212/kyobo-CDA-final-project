# 베이스 이미지로 Python 3.12 slim 버전 사용
FROM python:3.12-slim

# 필요한 패키지를 미리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    nginx

# 작업 디렉토리 설정
WORKDIR /apply

# 소스 코드 복사
COPY . /apply/

# 프로젝트 의존성 설치
RUN pip3 install --upgrade pip && pip3 install -r backend/requirements.txt

# 백엔드 서버 디렉토리로 이동
WORKDIR /apply/backend/

ENV DJANGO_ENV=production
ENV PYTHONUNBUFFERED=1

# # uWSGI 설치
# RUN pip3 install uwsgi

# # uWSGI 설정 파일 복사 (로컬에서 준비된 uwsgi.ini를 컨테이너로 복사)
# COPY uwsgi.ini /apply/backend/uwsgi.ini

# # Nginx 설정 파일 복사 (로컬에서 준비된 nginx.conf를 복사하여 Nginx 설정)
# COPY nginx.conf /etc/nginx/nginx.conf
# COPY default /etc/nginx/sites-enabled/default

# 8000 포트 오픈
EXPOSE 8000

RUN python manage.py collectstatic --noinput

# uWSGI와 Nginx 시작
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py makemigrations application_form && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]