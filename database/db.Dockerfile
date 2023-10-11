FROM mongo:4.0.6

# 환경변수 생성
ENV MONGO_INITDB_ROOT_USERNAME root
ENV MONGO_INITDB_ROOT_PASSWORD 1234
ENV MONGO_INITDB_DATABASE freework
ENV TZ Asia/Seoul

# 컨테이너 내부에서 사용할 작업 디렉터리 생성
WORKDIR /app

# MongoDB 설정 파일 복사
COPY ./database/mongod.conf /etc/mongod.conf
COPY ./database/init.sh /docker-entrypoint-initdb.d/

# 컨테이너가 시작될 때 MongoDB 실행
CMD ["mongod", "-f", "/etc/mongod.conf"]
