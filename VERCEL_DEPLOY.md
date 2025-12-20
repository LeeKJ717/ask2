# Vercel 배포 가이드

## 🚀 빠른 배포

### 방법 1: Vercel 웹사이트에서 배포 (가장 쉬움)

1. **Vercel 계정 생성**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인

2. **프로젝트 배포**
   - "Add New..." → "Project" 클릭
   - GitHub 저장소 선택 또는 직접 업로드
   - 이 폴더(`ask2`)를 업로드
   - 자동으로 PHP 감지됨

3. **배포 완료**
   - Vercel이 자동으로 URL 제공
   - 예: `https://your-project.vercel.app`

### 방법 2: Vercel CLI 사용

```bash
# Vercel CLI 설치
npm i -g vercel

# 프로젝트 폴더로 이동
cd ask2

# 배포
vercel
```

## ⚠️ 중요 제한사항

### 1. 파일 저장 문제
Vercel은 **서버리스 환경**이므로 파일 시스템에 직접 쓰기가 **제한**됩니다.

**현재 코드의 문제:**
- `submit.php`에서 `result/` 폴더에 파일 저장 시도
- Vercel에서는 작동하지 않을 수 있음

**해결 방법:**
1. **Vercel KV 사용** (Key-Value 저장소)
2. **Supabase/MongoDB** 등 외부 데이터베이스 사용
3. **Vercel Blob Storage** 사용
4. **임시 저장**: `/tmp` 디렉토리 사용 (영구 저장 안됨)

### 2. 세션 저장
세션도 제한적일 수 있으므로, 필요시 외부 세션 저장소 사용

## 🔧 수정이 필요한 부분

### submit.php 수정 예시 (Vercel KV 사용)

```php
// Vercel KV 사용 예시
$kv = getenv('KV_REST_API_URL');
// 또는 외부 데이터베이스 사용
```

### statistics.php 수정
- `result/` 폴더에서 파일 읽기 부분도 수정 필요
- 외부 저장소에서 데이터 읽도록 변경

## 📝 현재 상태

- ✅ 기본 PHP 파일들 복사 완료
- ✅ `vercel.json` 설정 완료
- ⚠️ 파일 저장 기능은 Vercel에서 작동하지 않을 수 있음
- ⚠️ 데이터베이스 또는 외부 저장소 연동 필요

## 🎯 권장 사항

Vercel 대신 **Railway** 또는 **Render** 사용을 권장합니다:
- PHP 완전 지원
- 파일 저장 가능
- 더 쉬운 설정

## 📚 참고 자료

- Vercel PHP 문서: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/php
- Vercel KV: https://vercel.com/docs/storage/vercel-kv

