# Heroku 배포 가이드

## 📋 사전 준비사항

1. **Heroku 계정 생성**
   - https://www.heroku.com 에서 계정 생성

2. **Heroku CLI 설치**
   - Windows: https://devcenter.heroku.com/articles/heroku-cli
   - 또는 `winget install Heroku.HerokuCLI` (Windows 11)

3. **Git 저장소 확인**
   - 현재 프로젝트가 Git 저장소인지 확인
   - `git status` 명령어로 확인

## 🚀 배포 단계

### 1. Heroku CLI 로그인
```bash
heroku login
```

### 2. Heroku 앱 생성
```bash
heroku create your-app-name
# 예: heroku create fortune-guide-app
```

### 3. 환경 변수 설정 (필요한 경우)
```bash
# OpenAI API Key 설정 (선택사항 - secrets.toml 대신 사용 가능)
heroku config:set OPENAI_API_KEY=your-api-key-here

# Google Generative AI API Key 설정 (선택사항)
heroku config:set GOOGLE_API_KEY=your-api-key-here
```

### 4. Git에 파일 추가 및 커밋
```bash
git add Procfile .slugignore runtime.txt setup.sh
git commit -m "Add Heroku deployment files"
```

### 5. Heroku에 배포
```bash
git push heroku main
# 또는
git push heroku master
```

### 6. 앱 확인
```bash
heroku open
```

## 📝 주요 파일 설명

### Procfile
- Heroku가 앱을 실행하는 방법을 정의
- Streamlit 앱을 웹 서버로 실행

### .slugignore
- Heroku 빌드에서 제외할 파일/폴더 지정
- venv, __pycache__ 등 불필요한 파일 제외로 빌드 속도 향상

### runtime.txt
- Python 버전 지정
- 현재: Python 3.11.9

### setup.sh
- Streamlit 설정 파일 자동 생성
- Heroku 환경에 맞게 설정

### requirements.txt
- Python 패키지 의존성 목록
- Heroku가 자동으로 설치

## 🔧 문제 해결

### 배포 실패 시
```bash
# 로그 확인
heroku logs --tail

# 빌드 로그 확인
heroku logs --tail --source app
```

### 포트 에러
- Procfile에 `--server.port=$PORT` 설정 확인
- `--server.address=0.0.0.0` 설정 확인

### 패키지 설치 실패
- requirements.txt에 버전 명시 고려
- 예: `streamlit>=1.28.0`

### 메모리 부족
```bash
# Heroku 플랜 확인
heroku ps

# 필요시 플랜 업그레이드
heroku ps:scale web=1:standard-1x
```

## 🔐 보안 설정

### API Key 관리
1. **Streamlit Secrets (권장)**
   - Heroku Dashboard → Settings → Config Vars
   - `STREAMLIT_SECRETS` 키로 secrets.toml 내용 추가

2. **환경 변수**
   ```bash
   heroku config:set OPENAI_API_KEY=your-key
   ```

### secrets.toml 형식
```toml
[api_keys]
openai_api_key = "your-openai-key"
google_api_key = "your-google-key"
```

## 📊 모니터링

### 앱 상태 확인
```bash
heroku ps
```

### 로그 실시간 확인
```bash
heroku logs --tail
```

### 앱 재시작
```bash
heroku restart
```

## 🔄 업데이트 배포

코드 변경 후:
```bash
git add .
git commit -m "Update app"
git push heroku main
```

## 💰 비용 정보

- **Hobby 플랜**: 무료 (월 550시간, 30분 비활성 시 슬리프 모드)
- **Eco 플랜**: $5/월 (월 1000시간, 슬리프 없음)
- **Basic 플랜**: $7/월 (24/7 운영)

## 📚 참고 자료

- [Heroku 공식 문서](https://devcenter.heroku.com/)
- [Streamlit 배포 가이드](https://docs.streamlit.io/deploy/heroku)
- [Heroku Python 지원](https://devcenter.heroku.com/articles/python-support)

