# 식물성 케톤식 영양강좌 수요조사 - Vercel 배포 버전

## Vercel 배포 방법

### 1. Vercel CLI 설치 (선택사항)
```bash
npm i -g vercel
```

### 2. Vercel에 배포
```bash
vercel
```

또는

### 3. GitHub 연동
1. https://vercel.com 접속
2. GitHub 계정으로 로그인
3. "New Project" 클릭
4. 이 저장소 선택
5. 자동 배포

## ⚠️ 주의사항

### Vercel의 PHP 제한사항
1. **파일 쓰기**: Vercel은 서버리스 환경이므로 파일 시스템에 직접 쓰기가 제한됩니다.
   - `result/` 폴더에 파일 저장이 작동하지 않을 수 있습니다.
   - 대안: 데이터베이스나 클라우드 스토리지 사용 권장

2. **세션**: 세션 저장도 제한적일 수 있습니다.

3. **환경 변수**: 민감한 정보는 Vercel 환경 변수로 설정하세요.

## 🔧 해결 방법

### 파일 저장 문제 해결
- Vercel KV (Key-Value 저장소) 사용
- 또는 Supabase, MongoDB 등 외부 데이터베이스 사용
- 또는 Vercel Blob Storage 사용

## 📝 파일 구조

```
ask2/
├── index.php          # 설문지 메인 페이지
├── submit.php         # 설문 제출 처리
├── admin.php          # 관리자 로그인
├── admin_login.php    # 로그인 처리
├── admin_logout.php   # 로그아웃
├── statistics.php     # 통계 페이지
├── survey.json        # 설문지 데이터
└── vercel.json        # Vercel 설정
```

## 🚀 배포 후

배포가 완료되면 Vercel이 제공하는 URL로 접속할 수 있습니다.
예: `https://your-project.vercel.app`

