# 책 표지·책등·뒷표지·판권지 만들기 (cover.md)

『논술 마스터·매니아 시리즈』 25권 표지(2026-10-02)를 만든 방법을 그대로 적은 문서다. 같은 컴퓨터(z840)에서 이 문서의 명령을 차례로 실행하면 같은 결과를 다시 만들 수 있고, 다른 책 시리즈에도 그대로 쓸 수 있다.

- 도구 모음(키트): `~/mdfile/cover_kit/`
- 이번 작업 원본: `~/bookz840/book-nonsul25_2026-1002/cover/`
- 결과물 예: `~/bookz840/논술인강 단락책 25권/NN 제목/<줄기>-표지앞-v1.pdf` 등, 모아 보기는 `~/다운로드/논술인강단락책25권/표지/`
- 백업: `nonsul25-cover-v1-20261002.tar.gz` + `.sha256`이 z840 `~/backups/book-nonsul25_2026-1002/`, z440 같은 경로, NAS `/mnt/nas/book-nonsul25_2026-1002/`에 있다.

---

## 1. 무엇을 만드나

| 산출물 | 크기 | 내용 |
|---|---|---|
| 앞표지 `<줄기>-표지앞-vN.pdf/.png` | 210 × 297 mm(재단 크기) | 시리즈 배지·권 번호·제목·논제 질문·기출 정보·저자·시리즈 로고 + 일러스트 |
| 펼침 표지 `<줄기>-표지펼침-vN.pdf/.png` | (3 + 210 + 책등 + 210 + 3) × 303 mm | 뒷표지 │ 책등 │ 앞표지, 사방 도련 3 mm — 인쇄소에 넘기는 파일 |
| 판권지 `<줄기>-판권지-vN.pdf/.png` | A4 한 쪽 | 서지 정보 표(추후 기입 칸) + 저작권 문구 + 시리즈 전체 목록 |
| 모아 보기 `표지전체보기-vN.pdf` | — | 1쪽 앞표지 전부, 2쪽 책등을 나란히 꽂은 모습 |

사용자 요구(2026-10-02)와 그것을 디자인에 옮긴 방법:

1. **"비상·미래엔(high_sci_bio2.jpg) 고등학교 참고서처럼 보고 싶게"** → 납작한 벡터 그림체, 큰 제목, 참고서식 배지·로고 배치.
2. **"파스텔 톤으로 재미있게, 난해하지 않으면서 제목과 어울리는 과학 일러스트"** → 권마다 귀여운 마스코트 동물 + 그 단원을 상징하는 쉬운 사물(예: 기체 = 풍선 든 곰·열기구·유리병 속 공들), 파스텔 3~4색 + 진한 강조색 1색, 리소 인쇄 낟알.
3. **"책마다 디자인이 제각기 달라야"** → 배치 틀 5가지 × 제목 글꼴 13종 × 권마다 다른 그림·색을 돌려 쓴다.
4. **"1권만 보고도 나머지 24권을 알게 해야 세트로 산다"** → 뒷표지에 25권 전체 앞표지 썸네일(이 책은 테두리 강조)과 "함께 보면 좋은 권", 책등은 25권 모두 같은 글꼴·띠색·번호, 판권지에 25권 목록.
5. **시리즈 이름**: 화학 = 논술 매니아 시리즈(MANIA, 분홍 `#c0537a`), 생물 = 논술 마스터 시리즈(MASTER, 초록 `#3f8f5a`). 권 번호는 전체 일련번호 01–25.
6. **ISBN은 나중에** → 뒷표지 오른쪽 아래 52 × 30 mm 빈 바코드 상자, 정가·펴낸곳·출판 등록 등은 "(추후 기입)" 칸으로 남긴다.

---

## 2. 사용한 프로그램 (버전까지)

### 2-1. 컴퓨터

| 항목 | 값 |
|---|---|
| 컴퓨터 | z840 (HP Z840 워크스테이션) |
| 운영체제 | Rocky Linux 9.8 (Blue Onyx), 커널 5.14.0-687.45.1.el9_8.x86_64 |
| 그래픽 카드 | NVIDIA GeForce RTX 3060 12 GB × 2장, 드라이버 610.57.04 |

### 2-2. 그림 생성(일러스트) — ComfyUI + Z-Image-Turbo

| 항목 | 값 |
|---|---|
| 프로그램 | **ComfyUI** 0.35.0 (git 커밋 `f42b24ef`, 2026-09-13), 위치 `~/imggen/ComfyUI/` |
| 파이썬 | ComfyUI 전용 가상환경 `~/imggen/ComfyUI/.venv` — Python 3.12.14(uv로 설치), PyTorch 2.11.0+cu128(CUDA 12.8), Pillow 12.3.0 |
| 그림 모델 | **Z-Image-Turbo** bf16 — `z_image_turbo_bf16.safetensors` (12,309,866,400 바이트) |
| 글 해석 모델(텍스트 인코더) | `qwen_3_4b.safetensors` (8,044,982,048 바이트) |
| VAE | `ae.safetensors` → ComfyUI 안에서는 `z_image_ae.safetensors` 이름의 링크 (335,304,388 바이트) |
| 모델 받은 곳 | Hugging Face 저장소 `Comfy-Org/z_image_turbo`의 `split_files/…` (`~/imggen/download_models_v1.sh`, 끊기면 `~/imggen/pdownload_v1.py`로 이어받기) |
| 모델 실제 위치 | `~/imggen/hf/z_image_turbo/split_files/` → `ComfyUI/models/diffusion_models·text_encoders·vae/`에 심볼릭 링크 |
| 라이선스 | 세 파일 모두 **Apache 2.0** — 상업 출판(책 판매)에 써도 된다 |
| 서버 실행 | `~/mdfile/cover_kit/start_comfy_v1.sh`(= `~/imggen/start_comfy_v1.sh`): GPU0 → 포트 8188, GPU1 → 포트 8189. 한 GPU에 서버 하나 |
| 생성 설정 | 8스텝 · cfg 1.0 · 샘플러 `res_multistep` · 스케줄러 `simple` · `ModelSamplingAuraFlow` shift 3.0 · 네거티브 없음(`ConditioningZeroOut`) · 1024 × 1280 픽셀(세로 4:5) |
| 속도 | 1장 약 28~30초/GPU(첫 장은 모델 적재로 약 3분). 두 서버 병렬이라 100장 ≈ 25분 |
| 일괄 생성 스크립트 | `cover_kit/photo_gen_v1.py`(원래 요리 사진용 `cookphoto_kit`의 것과 같은 파일): 프롬프트 JSON을 읽어 두 서버에 나눠 보내고 PNG를 받는다. 이미 있는 후보는 건너뛰므로 끊겨도 같은 명령으로 이어진다 |

### 2-3. 조판·합성 — WeasyPrint(HTML/CSS → PDF)

| 항목 | 값 |
|---|---|
| 파이썬 | 시스템 Python 3.9.25 (`/usr/bin/python3`) |
| PDF 조판 | **WeasyPrint 66.0** (pydyf 0.11.0) — HTML/CSS로 표지를 짜서 PDF로 낸다 |
| 그림 처리 | **Pillow 11.3.0**(시스템 파이썬 쪽) — 일러스트 2배 확대, 낟알 입히기, 색 뽑기, 밀착 인화지·모아 보기 |
| PDF → PNG | **poppler-utils 21.01.0**의 `pdftoppm`(미리보기·썸네일·책등 잘라 보기), `pdfinfo`(쪽수 읽기) |
| 글꼴 관리 | fontconfig 2.14.0 (`fc-list`, `fc-cache`) |
| 내려받기 | curl 7.76.1 |

### 2-4. 글꼴 (모두 PDF에 내장됨)

| 글꼴 | 출처·라이선스 | 쓰인 곳 |
|---|---|---|
| Noto Sans CJK KR (Thin~Black) | 시스템 기본(`google-noto-sans-cjk` 패키지), SIL OFL | 본문 글자 전부, 책등 제목(700), 일부 표지 제목(300) |
| Jua, Do Hyeon, Black Han Sans, Gowun Dodum, Gowun Batang Bold, Sunflower(Light·Bold), Gothic A1(Light·Bold·Black), NanumGothic(Regular·ExtraBold), Gaegu Bold, Hahmlet(가변 굵기), Stylish, IBM Plex Sans KR(Light·Bold), Song Myung | Google Fonts 저장소 `github.com/google/fonts/ofl/…`, **SIL Open Font License** — 상업 이용·PDF 내장 가능 | 표지 제목(권마다 다름), Black Han Sans는 큰 권 번호·책등 번호 |

설치: `bash ~/mdfile/cover_kit/install_fonts_v1.sh` → `~/.local/share/fonts/ofl-kr/`에 받고 `fc-cache -f`. 확인: `fc-list : family | grep -iE "jua|hahmlet|black han"`.

---

## 3. 키트 파일 (`~/mdfile/cover_kit/`)

| 파일 | 하는 일 |
|---|---|
| `start_comfy_v1.sh` | ComfyUI 서버 두 개(8188·8189) 켜기 |
| `photo_gen_v1.py` | 프롬프트 JSON → 후보 그림 일괄 생성 (ComfyUI 가상환경 파이썬으로 실행) |
| `style_cover_v4.txt` | 모든 그림 프롬프트 끝에 붙는 공통 그림체 문장(최종판) |
| `noboost.json` | 빈 보강 규칙 `[]` — photo_gen의 `--boost`에 넘긴다(없으면 오류) |
| `contact_v1.py` | 후보 밀착 인화지(한 줄에 한 권 4장, 다섯 권씩 한 장) |
| `meta_v1.py` | 권별 정보(제목·짧은 이름·문항 수·연도 범위·쪽수·차례·연결 단원)를 원고에서 다시 세어 `meta.json`으로 |
| `make_cover_v1.py` | 앞표지·펼침 표지·판권지 PDF/PNG를 만드는 본체 |
| `shelf_v1.py` | 책등 나란히 보기 + 앞표지 모아 보기 PDF |
| `install_fonts_v1.sh` | OFL 한글 글꼴 18개 내려받기 |
| `examples/prompts_nonsul25_v1.json` | 이번 25권 그림 프롬프트(권마다 마스코트·장면·색) |
| `examples/picks_nonsul25_v1.json` | 이번에 고른 후보 파일 이름 |
| `examples/meta_nonsul25.json` | 이번 `meta.json` |

`meta_v1.py`와 `make_cover_v1.py`는 논술 25권 프로젝트 구조(`books/NN-slug/book.json`, 엔진 `engine/build.py`의 `Book` 클래스)에 맞춰져 있다. 다른 책에 쓸 때는 `meta.json`만 같은 형식으로 손으로 만들어도 된다(필드: `no, title, short, subject, stem, question, summary, links, n_items, n_schools, years[2], n_official, chapters[], pages`).

---

## 4. 작업 순서 (명령 그대로)

작업 폴더를 `<책프로젝트>/cover/`로 하고 키트를 복사해 쓴다.

```bash
P=~/bookz840/<책프로젝트>; mkdir -p $P/cover/{prompts,cand,sel,out}
# make_cover·meta·contact·photo_gen·shelf 스크립트와 그림체 문장·빈 보강 파일을 작업 폴더로
cp ~/mdfile/cover_kit/*.py ~/mdfile/cover_kit/*.txt ~/mdfile/cover_kit/noboost.json $P/cover/
cd $P/cover
VPY=~/imggen/ComfyUI/.venv/bin/python     # 그림 생성·밀착 인화지는 이 파이썬
```

### 4-1. 글꼴 설치 (처음 한 번)
```bash
bash ~/mdfile/cover_kit/install_fonts_v1.sh
```

### 4-2. 권별 정보 뽑기
```bash
python3 meta_v1.py          # → cover/meta.json, 화면에 권·문항·쪽수 표
```
- 문항 수·대학 수·연도 범위는 원고(front matter)에서 **다시 센다**. book.json의 표지 문구(`cover.core`)는 원고를 고친 뒤 낡아 있을 수 있어서 쓰지 않는다.
- 쪽수는 흑백판 PDF(`out/<줄기>-v1-bw.pdf`)를 `pdfinfo`로 읽는다(책등 폭 계산용).

### 4-3. 그림 서버 켜기
```bash
bash ~/mdfile/cover_kit/start_comfy_v1.sh
until curl -s -m 2 localhost:8188/system_stats >/dev/null && curl -s -m 2 localhost:8189/system_stats >/dev/null; do sleep 3; done
nvidia-smi        # 두 GPU에 ComfyUI가 올라갔는지
```

### 4-4. 그림 프롬프트 쓰기 — `prompts/covers_v1.json`
형식(photo_gen 공통):
```json
{"no":"C","name":"covers","shots":[
 {"id":"c01","label":"01","prompt":"<장면 설명>. Colors: <파스텔 3색>, with <진한 강조색> accents.","w":1024,"h":1280},
 ...]}
```
권마다 한 문장 장면을 쓰는 규칙:
- **마스코트 동물 하나 + 그 단원을 상징하는 쉬운 사물 3~5개**. 개념을 그대로 그리지 말고 생활 사물로 비유한다(유전 암호 = 요리사 로봇과 구슬 이중 나선, 세포막 = 작은 문이 많은 비눗방울 집, 면역 = 방패 든 강아지 기사와 귀여운 가시 세균, 화학 전지 = 레몬 전지와 전구, 화학양론 = 저울로 밀가루 다는 사슴 제빵사).
- **마스코트는 25권이 모두 달라야 한다**(곰·로봇·고양이·토끼·판다·펭귄·여우·수달·강아지·거북·다람쥐·코알라·고슴도치·너구리·오리·부엉이·개구리·햄스터·달팽이·나무늘보·물범·양·병아리·사슴 …).
- **색은 권마다 다른 조합**: 파스텔 3색 + 진한 강조색 1색(예: "lavender purple, butter yellow, soft coral, with deep navy accents").
- 글자를 부르는 낱말(letters, recipe, reading, sign, label, book, title 등)은 장면에 쓰지 않는다. 그림 속 종이는 "with only pictures"처럼 적는다.

이번 25권 실제 문장: `cover_kit/examples/prompts_nonsul25_v1.json`.

### 4-5. 공통 그림체 문장 — `style_cover_v4.txt` (최종판, 그대로 쓸 것)
```
Style: contemporary flat vector illustration, risograph screen-print look with stippled grain shading, only three or four flat pastel ink colors plus one dark accent, bold simple rounded shapes, cute mascot character, rich playful scene densely filling the whole frame from edge to edge with objects, plants, flowers and sparkles everywhere, no empty areas, graphic and modern editorial picture. The picture contains no writing of any kind: no title, no caption, no letters, no characters, no logo.
```

### 4-6. 후보 생성 (권마다 4장)
```bash
$VPY photo_gen_v1.py prompts/covers_v1.json --seeds 4 --out cand --style style_cover_v4.txt --boost noboost.json > gen_v1.log 2>&1
tail -1 gen_v1.log          # "done 100, fail 0"
```
- 결과는 `cand/c01/c<NN>_s<k>_<seed>.png`(폴더 이름은 첫 샷 id에서 `_` 앞부분을 딴다 — `c01`).
- 시험할 때는 `--only c01,c24`로 몇 권만, `--dry`로 최종 프롬프트만 확인.
- 중간에 멈추려면 **PID로** kill할 것: `ps aux | grep photo_gen_v1 | grep -v grep` → `kill <PID>`. `pkill -f "photo_gen…"`은 그 문자열이 든 셸까지 죽인다(exit 144). 멈춘 뒤 두 서버의 대기열 비우기:
  `for p in 8188 8189; do curl -s -X POST localhost:$p/queue -d '{"clear":true}' -H 'Content-Type: application/json'; curl -s -X POST localhost:$p/interrupt; done`

### 4-7. 고르기
```bash
python3 contact_v1.py cand/c01      # contact_01-05.jpg … contact_21-25.jpg
```
밀착 인화지를 **눈으로 직접 보고** 권마다 한 장을 고른다. 기준:
1. 그림 속에 글자·가짜 한자·영문이 **전혀 없을 것**(있으면 탈락).
2. 단원 상징이 한눈에 보일 것(마스코트만 있고 과학 사물이 약하면 다른 후보).
3. 파스텔일 것(검은 남색 바탕처럼 어두운 후보는 탈락 — 23권 4번).
4. 주인공이 그림 가운데~아래에 있을 것(배치 틀이 위쪽을 제목 자리로 잘라 쓰므로).

고른 것을 `sel/NN.png`로 복사하고 기록을 남긴다(이번 기록: `examples/picks_nonsul25_v1.json`):
```python
pick={1:2,2:3,3:4,...}   # 권: 후보 번호
for no,k in pick.items(): shutil.copy(glob.glob(f'cand/c01/c{no:02d}_s{k}_*.png')[0], f'sel/{no:02d}.png')
```

### 4-8. 표지 만들기
```bash
python3 make_cover_v1.py front            # 앞표지 전부 먼저 (썸네일 thumb/NN.png도 이때 생김)
python3 make_cover_v1.py all              # 앞표지 + 펼침 표지 + 판권지
python3 make_cover_v1.py all --only 3,24 --ver v2   # 일부만, 새 판번호로
```
**반드시 앞표지를 먼저 다 만든다** — 뒷표지의 25권 썸네일과 판권지의 표지 그림이 `thumb/NN.png`(앞표지 PDF를 40 dpi로 바꾼 것)를 쓰기 때문이다. 결과는 `out/NN/`.

### 4-9. 검사
1. 앞표지 모아 보기와 책등 나란히 보기를 만들어 **눈으로 확인**한다(겹침, 글자 잘림, 대비).
   - `python3 shelf_v1.py --ver v1` → `표지전체보기-앞-v1.png`, `표지전체보기-책등-v1.png`, `표지전체보기-v1.pdf`. 책등 띠는 펼침 PDF에서 x = (3 + 210) mm, 폭 = 책등 폭을 `pdftoppm -r 80 -x -y -W -H`로 잘라 2 px 간격으로 이어 붙인 것이다.
2. 몇 권은 펼침 표지 전체를 45~120 dpi로 뽑아 뒷표지·책등을 확대해 본다.
3. 확인할 것: 제목이 그림과 겹치지 않는가, 배지 글자가 잘리지 않는가, 책등 제목·시리즈 이름이 잘리지 않는가, 썸네일 줄이 정가·ISBN 칸을 덮지 않는가, 글자가 바탕에서 잘 읽히는가.

### 4-10. 배포·백업
- 권 폴더 `~/bookz840/<시리즈 폴더>/NN 제목/`에 본문 PDF와 함께, `~/다운로드/<시리즈>/표지/`에는 `NN-` 접두어를 붙여 복사. **같은 이름이 있으면 덮어쓰지 않는다**(판번호 vN 규칙).
- `cover/` 폴더를 tar.gz로 묶고 sha256을 만들어 z840 `~/backups/<프로젝트>/`, z440 같은 경로(scp), NAS `/mnt/nas/<프로젝트>/`에 넣고 세 곳 모두 `sha256sum -c`.

---

## 5. `make_cover_v1.py` 안에서 하는 일 (원리)

### 5-1. 그림 다듬기 `prep_image()`
1. 1024 × 1280 PNG를 **LANCZOS로 2배(2048 × 2560)** 확대 → 216 mm 폭에 약 240 dpi.
2. **리소 낟알**: `Image.effect_noise(크기, 38)` 회색 잡음 → 0.6 px 흐림 → 자동 대비 → 세기 10 %로 낮춰 곱하기(`ImageChops.multiply`). JPEG 품질 92로 `work/NN.jpg` 저장.
3. **색 뽑기**
   - 바탕색 `bg` = 그림 맨 위 6 % 띠의 중앙값 색.
   - 진한색 `dark` = 128 × 160으로 줄여 12색으로 양자화한 뒤 가장 어두운 색.
   - 강조색 `accent` = 그중 채도(최대–최소)가 가장 큰 중간색(아치형 큰 번호).
   - 연한색 `tint` = 바탕색을 흰색 쪽으로 55 % (액자형 바탕·뒷표지 바탕).
4. **글자 대비 보정**: WCAG 상대 휘도로 `dark`와 `bg`의 대비를 계산해 **6 : 1 이상이 될 때까지 dark를 0.88배씩 어둡게** 한다. (이것이 없으면 회색·올리브 글자가 연두 바탕에서 안 읽혔다 — 3·9·14·24권.)

### 5-2. 앞표지 배치 틀 5가지 (`LAYOUTS = "ABCDEBDAECADBEC…"`로 권마다 돌림)
| 틀 | 이름 | 구성 |
|---|---|---|
| A | 참고서형 | 위 90 mm는 바탕색, 그 아래 211 mm 전면 그림(아래 기준으로 잘라 씀), 경계는 바탕색→투명 그라데이션 26 mm, 왼쪽 아래 반투명 흰 상자에 논제 질문·기출 정보·저자 |
| B | 액자형 | 연한 바탕, 제목 아래 두꺼운 테두리(2.2 mm)의 둥근 사각 창(모서리 16 mm)에 그림 |
| C | 아치형 | 오른쪽 위 큰 권 번호(Black Han Sans 92 pt, 강조색), 아치 창(위가 반원) 그림 |
| D | 세로 띠형 | 왼쪽 33 mm 진한색 띠에 권 번호·MANIA/MASTER, 오른쪽에 그림 |
| E | 아래 패널형 | 위 206 mm 그림, 아래 미색 패널에 큰 제목 + "1부 기본개념·2부 기출 개념·3부 답안 패턴·4부 실전 풀이" 칩 4개 |

- 제목 글꼴은 `FONTS` 16개 목록에서 `(권번호 × 7) mod 16`으로 골라 이웃 권이 겹치지 않게 했다.
- **제목 줄나눔** `title_lines()`: 7자 이하는 한 줄, 길면 가운뎃점(·) 단위로 2~3줄 중 가장 긴 줄이 가장 짧아지는 조합을 고른다(예: "유전 암호· / 전사·번역").
- **제목 크기** `fit()`: 한글 한 자 폭 ≈ 글자 크기(pt) × 0.353 mm로 보고, 폭(틀마다 140~182 mm)과 높이(44~56 mm)에 둘 다 들어가는 가장 큰 크기. 줄 간격 1.12~1.15.
- 공통 요소: 왼쪽 위 시리즈 배지(`MASTER | 논술 마스터 시리즈 | 생물 03`, `white-space: nowrap` 필수), 오른쪽 아래 시리즈 로고 상자, 논제 질문("○○ 논제는 무엇을 묻고, 어떻게 답하는가?"), "대학 기출 n문항 · 연도–연도학년도", "이광조 지음".

### 5-3. 뒷표지 `back_html()` — 세트 판매 장치
- 위: 논제 질문(15 pt) · 한 줄 요약 · 4부 구성 카드 4장(2 × 2) · "이 책의 차례 — 1부 기본개념편" 14장 2단 목록.
- 가운데(위에서 120 mm): **시리즈 전 25권 상자** — "논술 마스터 시리즈 · 생물 12권 (01–12)" 한 줄, "논술 매니아 시리즈 · 화학 13권 (13–25)" 한 줄. 썸네일 폭 = (175 − (권수 − 1) × 1.2) ÷ 권수 mm, 높이 = 폭 × 1.414, 아래에 번호와 짧은 이름. **이 책은 시리즈색 0.8 mm 외곽선**. 그 아래 "함께 보면 좋은 권: …"(book.json `cover.links`).
- 아래: 마스코트 원형 자르기(52 mm) + 말풍선("개념 → 기출 → 답안 → 실전, 한 단원을 끝까지."), 왼쪽 아래 정가(추후 기입)와 "실린 기출 문항의 저작권은 각 대학에 있습니다", 오른쪽 아래 ISBN·바코드 빈 상자 52 × 30 mm(점선).

### 5-4. 책등 `spine_html()` — 25권이 한 세트로 보이게
- **책등 폭 = 흑백판 쪽수 × 0.055 mm + 0.5 mm** (백모조 100 g의 한 장 두께 ≈ 0.11 mm, 한 쪽 = 반 장으로 어림). 상수 `PAPER_MM_PER_PAGE` — **인쇄소에서 실제 종이 두께를 받으면 이 값만 고치고 다시 만든다**. 이번 25권은 16.0~24.0 mm.
- 위 36 mm 시리즈색 띠 + 흰 권 번호(Black Han Sans) + MASTER/MANIA.
- 가운데: 제목을 **위→아래로 읽게 90° 돌린** 한 줄(Noto Sans CJK KR 700, 최대 14 pt) + 같은 줄 끝에 "시리즈 이름 · 이광조 지음". 돌린 상자 길이 236 mm, 세로 중심 164 mm(띠와 아래 띠 사이).
- 아래 11 mm 진한색 띠.
- 제목 글꼴은 **앞표지와 달리 25권 모두 같게** 한다(꽂아 두었을 때 통일감).

### 5-5. 펼침 표지 조립 `make_spread()`
- 전체 폭 W = 3 + 210 + 책등 + 210 + 3 mm, 높이 303 mm. HTML 상자 세 개를 절대 위치로 놓는다: 뒷표지 상자(216 mm 폭) x = 0, 앞표지 상자 x = 3 + 210 + 책등 − 3, 책등 상자 x = 3 + 210을 **마지막에** 놓아 앞·뒤표지 도련이 책등 밑으로 들어가게 한다.
- `@page { size: W mm 303 mm; margin: 0 }`로 WeasyPrint가 한 쪽 PDF를 만든다. 미리보기 PNG는 `pdftoppm -r 50`.

### 5-6. 판권지 `make_colophon()`
- 앞표지 썸네일 + 시리즈 표기 + 제목 + 4부 구성 설명.
- 표: 1판 1쇄 발행(20○○년 ○월 ○일), 지은이 이광조, 펴낸이·펴낸곳·출판 등록·주소·전화·ISBN·세트 ISBN·정가 = "(추후 기입)".
- 문구: 무단 전재·복제 금지, 기출 문항 저작권은 각 대학, 표지 그림은 Apache 2.0 오픈 모델, 글꼴은 SIL OFL, 파본 교환.
- 시리즈 25권 목록 두 단(마스터 · 생물 / 매니아 · 화학), 이 책은 굵게·시리즈색.

---

## 6. 겪은 함정과 해결 (다시 하면 처음부터 피할 것)

| 증상 | 원인 | 해결 |
|---|---|---|
| 그림 위쪽에 가짜 한자·영문 제목(“语文”, “TOU THU”)이 그려짐 | 프롬프트에 "textbook **cover**", "**top fifth plain** background", "reading a ribbon of **letters**/recipe" 같은 말 | 이 낱말을 모두 빼고 style v4처럼 "화면 가득 + 글자 없음" 문장을 끝에 붙인다. 제목 자리는 그림을 잘라 만든다 |
| 장면이 휑하고 아동 그림책 같음 | "generous clean background" | "rich playful scene densely filling the whole frame … no empty areas" |
| `photo_gen_v1.py`가 JSON 오류로 시작 안 함 | `--boost /dev/null` | 빈 배열 파일 `noboost.json`(`[]`)을 넘긴다 |
| 생성 중단 시 내 셸이 죽음(exit 144) | `pgrep/pkill -f "photo_gen…"`이 명령 문자열이 든 셸 자신과도 일치 | `ps aux | grep … | grep -v grep`으로 PID를 보고 `kill PID` |
| 바탕색 채움이 안 됨(흰색) | WeasyPrint가 CSS `inset: 0`을 무시 | `left:0; top:0; width:100%; height:100%` |
| 시리즈 배지 마지막 글자 잘림, 두 줄로 꺾임 | `display:inline-flex` 폭 계산 문제 | `display:inline-block` + `white-space:nowrap` |
| 제목이 그림 위로 겹침 | 그림이 270 mm 전면이고 제목 자리를 안 비움 | 틀마다 제목 높이를 계산(`th(fs)`)해 그림 시작 위치를 그 아래로 |
| 화학 권 번호가 12로 나옴(24권) | 시리즈 안 번호(권−12)를 씀 | 전체 일련번호 01–25로 통일 |
| 뒷표지 썸네일이 정가·ISBN 칸을 덮음 | 한 줄 7권씩 4줄 | 시리즈별 한 줄(12권·13권)로 폭을 계산 |
| 책등 시리즈 이름이 아래 띠에 잘림, 얇은 제목이 안 읽힘 | 돌린 상자 245 mm가 너무 길고 제목에 권별 얇은 글꼴 | 236 mm·중심 164 mm, 책등 제목은 Noto Sans CJK KR 700으로 통일 |
| 일부 권 글자가 바탕에 묻힘 | 양자화 "가장 어두운 색"이 회색·올리브 | 대비 6 : 1 자동 보정(5-1의 4) |
| Hahmlet 글꼴 경고 `instantiateVariableFont` | 가변 글꼴을 WeasyPrint가 굵기별로 잘라 씀 | 경고일 뿐 결과는 정상 |

---

## 7. 다른 책·시리즈에 쓸 때 바꿀 곳

1. `meta.json` — 권 목록(직접 만들거나 `meta_v1.py`를 그 프로젝트에 맞게 고침).
2. `make_cover_v1.py`
   - `series()` — 시리즈 이름·영문 로고·색·분류 기준(지금은 `subject`가 생물이면 MASTER).
   - 앞표지 문구 `kicker`, 논제 질문 `question`, 저자 "이광조 지음"(→ `author_txt()`와 각 틀의 `author`), 뒷표지 4부 구성 카드 `feat`, 말풍선 문구, 판권지 문구.
   - 썸네일 줄 구성(`back_html()`의 `(('… 생물 12권 …', range(1, 13)), ('… 화학 13권 …', range(13, 26)))`) — 권 수가 다르면 줄을 나누는 범위를 바꾼다(한 줄 최대 14권 정도까지 읽을 만하다).
   - 판형이 다르면 `TRIM_W, TRIM_H`와 각 틀의 mm 좌표, 종이가 다르면 `PAPER_MM_PER_PAGE`.
3. 프롬프트 JSON — 책마다 마스코트·장면·색.
4. 출력 판번호는 `--ver vN`으로 올리고 이전 판은 지우지 않는다.

관련 문서: `~/mdfile/cookphoto_v1.md`(같은 ComfyUI 환경으로 요리 사진 만들기), 메모리 `imggen-comfyui-setup`, `nonsul-25-books-project`.
