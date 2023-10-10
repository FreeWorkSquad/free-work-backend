from pymongo import MongoClient

from app.src.database.database import Database

HOSTNAME = 'localhost'
PORT = '27017'
USERNAME = 'root'
PASSWORD = '1234'
DBNAME = 'admin'


def create_db_enpoint(username: str, password: str, hostname: str, port: str) -> str:
    return f'mongodb://{username}:{password}@{hostname}:{port}/'


def get_db_endpoint():
    return create_db_enpoint(USERNAME, PASSWORD, HOSTNAME, PORT)


def connect_db(db_name: str):
    # MongoDB 연결 설정
    client = MongoClient(get_db_endpoint())
    return client[db_name]


db = Database(connect_db(DBNAME))