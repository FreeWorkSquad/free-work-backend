# free-work-backend

![PythonVersion](https://img.shields.io/badge/python-3.9.13-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.103.1-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.7.1-orange)

## free-work-backend-service

> 근태 관리 앱 freework의 backend service 입니다.


###  1. Development Environment Setting
1. 로컬 개발 환경에 `git clone ...` 
2. Pycharm 을 열고 `open project ...`
3. Interpreter Setting
   - **Virtualenv**
     1. **Add New Interpreter** 선택
     2. **Add Local Interpreter** 선택
     3. **Virtualenv Environment** 선택 
     4. 로컬에 설치된 Python 3.10 경로를 Base Interpreter로 설정
     5. `pip install .` (`pyproject.toml`에 작성한 의존성 설치, 아래 **3. Extra Setting** 참고)

###  2. Extra Setting
- 도커 빌드 및 실행할 경우, `version.py` 실행 사전 작업 필요    
  👉 `version_info.py` 정보 생성 과정
  ```python
  version: str = 'v0.40e05b9'
  git_branch: str = 'docs/7-update-readme.md'
  git_revision: str = ''
  git_short_revision: str = ' 40e05b9'
  build_date: str = '2023-10-03 20:55:28'
  ```
- `pyproject.toml` 작성 (참고: [Declaring project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/))
   - project 메타데이터 작성 (_name_, _version_, ... etc)
   - 의존성 작성: _dependencies_
   - 개발 의존성 작성: _project.optional-dependencies_
- `config.yaml` 파일 작성
  - `PORT`: fastapi server port
  - `LOG`: [loguru](https://github.com/Delgan/loguru) 사용하여 로그 세팅
    - `SAVE`: 로그 파일 저장 여부 (1 = 저장, 0 = 저장하지 않음)
    - `ROTATION`: 매일 `mm:ss`시에 새로운 로그 파일 생성
    - `RETENTION`: 설정한 시간 이후에 제거 (ex. "1 month 2 weeks", "10h")
    - `COMPRESSION`: 압축 형식 ("gz", "bz2", "xz", "lzma", "tar", "tar.gz", "tar.bz2", "tar.xz", "zip" 등의 형식 지원)
    - `ROTATION`, `RETENTION`, `COMPRESSION` 모두 loguru에 있는 파라미터로 자세한 파라미터 정보는 [공식 문서](https://loguru.readthedocs.io/en/stable/api/logger.html#file:~:text=See%20datetime.datetime-,The%20time%20formatting,-To%20use%20your) 확인
    - `PATH`: 디렉토리명까지 설정, (default = `YYYY/MM/*.log` 디렉토리 생성)
- **Project Major Version**은 `pyproject.toml`의 [project.version]에서 설정한다.
  - 해당 설정은 project version, FastAPI version 설정에 영향을 미친다.


### 3. How To Run
- local run
  - `$HOME/main.py`
    - `FileNotFoundError` or `ImportError` 발생시 _Working Directory_ (Working Directory = `$HOME`) 확인하기
  - _http :8000/openapi.json_ or _http://localhost:3000/docs_ 로 API 명세 확인 및 테스트
- docker run    
  `docker build ...` && `docker run -d -p ...` 로 컨테이너 빌드 & 구동
  ```shell
  # 도커 이미지 빌드
  docker build -t python-fastapi-template:0.1.5-dev -f Dockerfile .
  # 컨테이너 구동
  docker run -d --name python-fastapi-template -p 8000:8000 -e DEFAULT_X_TOKEN=fake-super-secret-token -e DEFAULT_TOKEN=default-token python-fastapi-template:0.1.5-dev
  ```

### 📚 참고 사항 📚   
- 해당 템플릿은 크게 **msa**와 **monlith** 두 가지로 나뉜다. (@TODO: monolith)
- Default는 **msa**(`$HOME/app`)로 해당 템플릿을 그대로 사용하면 된다.
- 📌 **monolith**를 사용할 경우, msa (`$HOME/app`, `$HOME/tests`)는 삭제하고 최상위 디렉터리인 monolith를 삭제 후 사용한다.
- 📌 DB를 사용하지 않을 경우, 관련된 코드는 모두 삭제한다. (`crud.py`, `database.py`, `schemas.py` 등)


### MSA
> @tiangolo(FastAPI 개발자)가 제공하는 유형(ex. api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조
- 출처: https://fastapi.tiangolo.com/tutorial/bigger-applications/
```
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # 
│   ├── main.py          # 
│   ├── dependencies.py  # 
│   ├── exceptions.py  # custom exception
│   ├── models.py  # 
│   ├── schemas.py  # 데이터베이스를 사용할 경우
│   ├── database.py  # 데이터베이스를 사용할 경우
│   ├── crud.py  # 데이터베이스를 사용할 경우
│   └── routers          # (API Endpoints) "routers" is a "Python subpackage" 
│   │   ├── __init__.py  # 
│   │   ├── items.py     # 
│   │   └── users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── admin.py     # 
│   └── src         # (Main Functions) "src" is a "Python subpackage"
│       ├── __init__.py  # 
├── tests                  # app directory architecture 에 맞게 unit test 구성
│   ├── __init__.py      # 
│   └── routers          # 
│   │   ├── __init__.py  # 
│   │   ├── test_items.py     # 
│   │   └── test_users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── test_admin.py     # 
│   └── src         # 
│       ├── __init__.py  #
```

- **routers**: API Endpoint. 작성한 API들은 `$HOME/app/main.py`에 router를 추가한다. (ex. `app.include_router(users.router)`)
- **src**: 모듈 메인 기능
- unit test
  - 👉 유닛 테스트는 기본적으로 `$HOME/app`의 디렉토리 구조에 맞게 구성한다.
  - 유닛 테스트 종류로는 기능 테스트, API 엔드포인트 테스트, Pydantic 모델 유효성 테스트, 보안 테스트가 있다.
- **Dockerfile**
  - `Dockerfile`(=Dockerfile.dev 역할): 개발을 위해 필요한 도구 및 라이브러리와 같은 추가적인 종속성을 설치하기 위한 라이브러리들이 설치된 환경
  - `product.Dockerfile`: 최종 제품을 배포하기 위해 필요한 것들만 포함한 환경