# 1. 베이스 이미지 설정
FROM python:3.10-slim

# 2. 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 및 데이터 파일 복사
COPY . .

# 5. FastAPI 실행 명령 (컨테이너 내부에서는 8000 포트로 실행)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]