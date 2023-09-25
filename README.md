# free-work-backend

![PythonVersion](https://img.shields.io/badge/python-3.9.13-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.103.1-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.7.1-orange)

## free-work-backend-service

> 근태 관리 앱 freework의 backend service 입니다.



###  Development Environment Setting
1. 로컬 개발 환경에 `git clone ...` 
2. Pycharm 을 열고 `open project ...`
3. Interpreter Setting
   - **Virtualenv**
     1. **Add New Interpreter** 선택
     2. **Add Local Interpreter** 선택
     3. **Virtualenv Environment** 선택 
     4. 로컬에 설치된 Python 3.10 경로를 Base Interpreter로 설정
     5. `pip install .` (`pyproject.toml`에 작성한 의존성 설치, 아래 **3. Extra Setting** 참고)