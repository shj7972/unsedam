# 사이트맵 접근 방법

## 문제
`https://unsedam.kr/static/sitemap.xml` 경로로 접근 시 내용이 표시되지 않습니다.
이는 Streamlit이 Heroku 환경에서 static 폴더의 파일을 직접 서빙하지 못하기 때문입니다.

## 해결 방법

### 방법 1: 페이지 경로 사용 (권장)
```
https://unsedam.kr/?page=sitemap
```

이 경로는 Streamlit 앱 내에서 사이트맵을 동적으로 생성하여 표시합니다.

### 방법 2: 정적 파일 직접 접근 (제한적)
Streamlit은 기본적으로 `static/` 폴더의 파일을 `/static/` 경로로 서빙하지만,
Heroku 배포 환경에서는 제한적일 수 있습니다.

## Google Search Console 제출

Google Search Console에 다음 URL을 제출하세요:
```
https://unsedam.kr/?page=sitemap
```

또는 robots.txt에 명시된 경로를 사용하세요:
```
https://unsedam.kr/?page=robots
```

## 참고사항

- Streamlit은 동적 웹 애플리케이션 프레임워크이므로 완전한 정적 파일 서빙에는 제한이 있습니다.
- `/?page=sitemap` 경로는 XML 형식의 사이트맵을 제공합니다.
- Google Search Console은 이 형식의 사이트맵을 인식할 수 있습니다.

