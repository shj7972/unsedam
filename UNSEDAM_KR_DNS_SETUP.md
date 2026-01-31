# unsedam.kr 도메인 DNS 설정 가이드

## ✅ Heroku 도메인 추가 완료

다음 도메인이 Heroku에 추가되었습니다:
- `unsedam.kr` (루트 도메인)
- `www.unsedam.kr` (서브도메인)

---

## 🔧 가비아 DNS 설정 방법

### 1단계: 가비아 도메인 관리 페이지 접속

1. https://www.gabia.com 접속
2. 로그인
3. **도메인 관리** → **내 도메인** 메뉴 클릭
4. `unsedam.kr` 도메인 선택
5. **DNS 관리** 또는 **네임서버 설정** 메뉴 클릭

---

### 2단계: DNS 레코드 추가

#### 📌 www.unsedam.kr 설정 (CNAME 레코드)

**가비아 DNS 관리 페이지에서:**

1. **레코드 추가** 또는 **CNAME 레코드 추가** 클릭
2. 다음 정보 입력:
   ```
   타입: CNAME
   호스트: www
   값/대상: stormy-gooseberry-ekwkhkqqiuibdp8c2ya8s7qh.herokudns.com
   TTL: 3600 (또는 기본값)
   ```
3. **저장** 또는 **확인** 클릭

---

#### 📌 unsedam.kr 설정 (루트 도메인)

**.kr 도메인은 루트 도메인에 CNAME을 사용할 수 없으므로 다음 중 하나를 사용:**

### 방법 A: ALIAS/ANAME 레코드 (권장)

가비아가 ALIAS 또는 ANAME 레코드를 지원하는 경우:

1. **레코드 추가** 클릭
2. 다음 정보 입력:
   ```
   타입: ALIAS (또는 ANAME)
   호스트: @ (또는 공백, 또는 unsedam.kr)
   값/대상: agile-beet-06nns5s9bw7wgju2ssav3jvw.herokudns.com
   TTL: 3600
   ```
3. **저장** 클릭

### 방법 B: A 레코드 (ALIAS 미지원 시)

가비아가 ALIAS를 지원하지 않는 경우, Heroku IP 주소를 사용해야 합니다.

**Heroku IP 주소 확인:**
```bash
# 터미널에서 실행
nslookup agile-beet-06nns5s9bw7wgju2ssav3jvw.herokudns.com
```

또는 다음 IP 주소를 사용 (Heroku 공용 IP):
- `75.101.163.44`
- `75.101.145.87`
- `54.243.75.98`
- `54.235.186.58`

**A 레코드 설정:**
```
타입: A
호스트: @ (또는 공백)
값/대상: 75.101.163.44
TTL: 3600
```

⚠️ **주의:** A 레코드는 Heroku IP가 변경될 수 있어 권장하지 않습니다. 가능하면 ALIAS 레코드를 사용하세요.

---

## 📋 설정 요약

| 도메인 | 레코드 타입 | 호스트 | 값/대상 |
|--------|------------|--------|---------|
| `www.unsedam.kr` | **CNAME** | `www` | `stormy-gooseberry-ekwkhkqqiuibdp8c2ya8s7qh.herokudns.com` |
| `unsedam.kr` | **ALIAS/ANAME** | `@` 또는 공백 | `agile-beet-06nns5s9bw7wgju2ssav3jvw.herokudns.com` |

---

## ⏱️ DNS 전파 대기

DNS 설정 후 전 세계 DNS 서버에 반영되는데 시간이 걸립니다:
- **일반적으로**: 5분 ~ 1시간
- **최대**: 24시간 (드물게)

**전파 확인 방법:**
```bash
# 터미널에서 실행
nslookup www.unsedam.kr
nslookup unsedam.kr
```

또는 온라인 도구 사용:
- https://www.whatsmydns.net/
- https://dnschecker.org/

---

## 🔒 SSL 인증서 자동 적용

Heroku는 자동으로 SSL 인증서를 발급합니다:
- DNS 전파 완료 후 자동 시작
- 약 5~10분 소요
- 완료 후 `https://unsedam.kr` 접속 가능

**SSL 인증서 상태 확인:**
```bash
heroku certs:info
```

---

## ✅ 설정 완료 확인

### 1. DNS 전파 확인
```bash
# 터미널에서 실행
nslookup www.unsedam.kr
nslookup unsedam.kr
```

### 2. 브라우저에서 접속 테스트
- `http://unsedam.kr` (HTTP)
- `https://unsedam.kr` (HTTPS - SSL 인증서 적용 후)
- `http://www.unsedam.kr`
- `https://www.unsedam.kr`

### 3. Heroku 도메인 상태 확인
```bash
heroku domains
heroku domains:wait unsedam.kr
heroku domains:wait www.unsedam.kr
```

---

## 🆘 문제 해결

### DNS 전파가 안 될 때
1. **TTL 값 확인**: 3600초(1시간) 권장
2. **레코드 타입 확인**: CNAME vs ALIAS vs A 레코드
3. **값/대상 확인**: 오타 없는지 확인
4. **시간 대기**: 최대 24시간까지 기다려보기

### SSL 인증서가 적용되지 않을 때
1. **DNS 전파 완료 확인**: `nslookup`으로 확인
2. **Heroku 상태 확인**: `heroku certs:info`
3. **시간 대기**: DNS 전파 후 5~10분 추가 대기

### 가비아에서 ALIAS 레코드를 찾을 수 없을 때
1. **고객 지원 문의**: 가비아 고객센터에 ALIAS/ANAME 지원 여부 문의
2. **A 레코드 사용**: 임시로 A 레코드 사용 (권장하지 않음)
3. **네임서버 변경**: Cloudflare 등 다른 DNS 서비스 사용 고려

---

## 📞 가비아 고객 지원

DNS 설정에 문제가 있으면:
- **전화**: 1588-5821 (평일 9:00~18:00)
- **이메일**: support@gabia.com
- **온라인 문의**: 가비아 웹사이트 고객센터

---

## 🎯 다음 단계

DNS 설정 완료 후:
1. ✅ DNS 전파 대기 (5분~1시간)
2. ✅ SSL 인증서 자동 적용 대기 (5~10분)
3. ✅ `https://unsedam.kr` 접속 테스트
4. ✅ SEO 설정 업데이트 (필요 시)

---

## 📝 참고 정보

**Heroku DNS Target:**
- `unsedam.kr`: `agile-beet-06nns5s9bw7wgju2ssav3jvw.herokudns.com`
- `www.unsedam.kr`: `stormy-gooseberry-ekwkhkqqiuibdp8c2ya8s7qh.herokudns.com`

**Heroku 앱 정보:**
- 앱 이름: `fortune-guide`
- 기본 도메인: `fortune-guide-d050303a06c6.herokuapp.com`

---

설정 완료 후 `https://unsedam.kr`로 접속하실 수 있습니다! 🎉

