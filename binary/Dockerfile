# Python 3.10 슬림 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 복사
COPY . .

# Cloud Run에서 제공하는 PORT 환경변수(기본 8080)를 사용하여 Uvicorn 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
