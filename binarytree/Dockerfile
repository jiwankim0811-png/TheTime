# 파이썬 가벼운 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run에서 제공하는 PORT 환경 변수를 사용하여 Gunicorn 서버 실행
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
