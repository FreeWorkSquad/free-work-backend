FROM python:3.9.16-slim

# Set environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV LOG_LEVEL=DEBUG

# 실행환경 설정
ENV APP_ENV=container

# 작업 디렉토리 설정
WORKDIR /app

# 파이썬 실행 위치
ENV PYTHONPATH=/app:${PYTHONPATH}

# 필요한 파일 복사
COPY config-prod.yaml ./config.yaml
COPY pyproject.toml ./
COPY ./app ./app/

# 패키지 설치
RUN pip install --no-cache-dir .[test,lint]

# Expose the port
EXPOSE 8000

# Run the app
CMD ["python", "app/main.py"]