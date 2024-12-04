# AI Malware File Detected
## 프로젝트 소개 ##
**프로젝트 명**  
AI 기반 공급망 보안: 악성파일 탐지 및 안전한 배포 서비스 제작

**팀원** | ★ : 팀장  
채진수 ( jinsu9758 ) ★   
고재민 ( Greenboy )  
양재원 ( R4ambb )  

- Malconv model 분석, Malconv model Predict code 작성.
- Malconv 모델 학습 및 파인 튜닝.
- 악성 샘플 수집 크롤링 코드 작성.
- 정상, 악성 샘플 전처리 코드 작성.

유성모 ( d0razi ) 

***프로젝트 배경***  
공급망 공격에 대한 빈도가 늘어나면서 심각성이 확대되고 있습니다.  
공급망 공격에 대한 보안 대응이 필요하며, 해당 방안으로 관리적 보안인 sbom이 화두로 떠오르고 있습니다.

하지만 이는 관리적 보안이며, 저희 팀은 공급망 공격을 기술적으로 방어하는데 기여하고자 도전적인 프로젝트를 진행하였습니다.

***프로젝트 개요***  
프로그램, 소프트웨어를 배포하기 전, 학습시킨 AI를 이용하여 배포 파일을 검사를 수행합니다. 검사 결과를 통해 배포 파일에 악성파일이 존재하는지 확인하여 배포 여부를 결정합니다.

- 하나라도 악성 파일인 경우 → 배포x
- 모든 파일이 정상 파일인 경우 → 배포o  

※ 파일 검사는 PE 파일을 대상으로 하고있습니다.

## 프로젝트 환경구축 ##
### 1. AWS 환경 구축, 구성도 설명###
***AWS Architecture***  
![aws 아키텍쳐 수정본 배경 흰색](https://github.com/user-attachments/assets/3c1bc4df-3a17-451e-a259-3fd4df511420)

① 프로그램을 배포하기 위해 웹(ec2)을 통해서 업로드  
② 첫번째 버킷에 해당 프로그램 저장  
③ ECR 이미지로 배포한 AI model을 실행시키는 Lambda 서비스  
④ AI 결과 웹(ec2)으로 전송  
⑤ 결과에 따라 배포한 파일 두번째 버킷으로 전송  
⑥ 클라이언트는 안전한 배포파일 다운로드 가능

※ AWS 환경 구성은 아래의 url 참고  
https://github.com/jinsu9758/lambda_docker_test


### 2.EC2 접속 ###
아래의 명령어를 수행합니다.
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python3-pip
$ sudo pip install django
$ sudo pip install django-bootstrap4
$ git clone https://github.com/jinsu9758/AIMalCodeDetect.git
```

***필요한 파일 추가***
※ 개인정보 보안상 github에는 넣지 않았습니다.
- media 폴더 생성 (project 폴더와 동일위치)
- settings.py 생성 및 설정 (설정 일부분만을 다루고 있습니다.)
```
ALLOWED_HOSTS = ["*"] # 설정

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'main',
    'users',
    'developer_page',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
AUTH_USER_MODEL = "users.User"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# AWS setting
AWS_ACCESS_KEY_ID = '[생성한 IAM 액세스 키]'
AWS_SECRET_ACCESS_KEY = '[생성한 IAM 시크릿 액세스 키]'
AWS_STORAGE_PRE_BUCKET_NAME = '[첫번째 버킷이름]'
AWS_STORAGE_FORE_BUCKET_NAME = '[두번째 버킷이름]'
AWS_S3_REGION_NAME = '[리전]'

```
***Django 실행***  
`python3 manage.py runserver 0.0.0.0:8000`


![스크린샷 2024-09-25 202713](https://github.com/user-attachments/assets/1584ae2f-81e3-44de-8add-ddf2eacc1156)
![KakaoTalk_20241017_135329988](https://github.com/user-attachments/assets/86dc1e7d-5893-4322-a9de-19b5e9ff7513)
