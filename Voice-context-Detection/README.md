# 🎧 Voice-context-Detection

사용자의 통화 음성 파일을 문맥 기반으로 분석하여 보이스 피싱 여부를 판단하고,  
입력한 전화번호가 보이스 피싱과 관련된 정보인지도 함께 판별하는 프로젝트입니다.  
이 폴더는 전체 보이스 피싱 탐지 파이프라인 중 **문맥 기반 탐지**와 **전화번호 탐지 기능**을 포함하고 있습니다.

---

## 📂 파일 구성 및 역할

| 단계 | 파일명 | 설명 |
|------|--------|------|
| 0단계 | `0_FSS_audio_extract.ipynb` | 금융감독원(FSS) 보이스 피싱 음성 파일 웹사이트에서 추출 |
| 1단계 | `1_voice_file_wav_conversion.ipynb` | 수집한 음성(mp4) → mp3 변환 → 최종 wav 변환 수행 |
| 2단계 | `2_data_processing.ipynb` | 음성 전처리 (16kHz 샘플링, mono 채널 변환, max length 계산 등) |
| 3단계 | `3_STT.ipynb` | 전처리된 음성 파일을 STT 변환하여 텍스트 추출 |
| 4단계 | `4_KoBERT_01.ipynb` ~ `4_KoBERT_04_Final.ipynb` | STT 텍스트에 대해 KoBERT를 활용한 문맥 분류 |
| 5단계 | `5_phone_checker.ipynb` | 경찰청 사이트 크롤링을 통해 전화번호 보이스 피싱 여부 확인 |

---

## 📘 KoBERT 모델 개선 단계 요약

STT된 통화 데이터를 문맥적으로 분석하기 위해 KoBERT 기반 모델을 여러 단계에 걸쳐 개선하였습니다.

| 단계 | 파일명 | 기준점 | 학습 데이터 | Epoch | 목적 |
|------|--------|--------|-------------|--------|------|
| 4-1단계 | `4_KoBERT_01.ipynb` | ❌ 없음 | KorCCVi | 3 | 초기 문맥 기반 피싱 분류 시도<br>→ 모든 문장이 보이스 피싱(1)로 분류되는 문제 발생 |
| 4-2단계 | `4_KoBERT_02.ipynb` | ❌ 없음 | KorCCVi + STT 변환 데이터(정상/피싱 각 100개) | 3 | 오분류 오류 분석<br>→ 금융 키워드 포함된 정상 문장도 보이스 피싱으로 분류 (FP 증가) |
| 4-3단계 | `4_KoBERT_03.ipynb` | ❌ 없음 | KorCCVi + STT 변환 데이터(정상/피싱 각 100개) | 5 | 금융 키워드 포함 정상 통화 데이터 추가 학습<br>→ 편향 완화 목적<br>→ 가중치 0.9 적용 |
| 4-4단계 (최종) | `4_KoBERT_04_Final.ipynb` | ✅ 있음<br>(0.7 / 0.8 / 0.9 / 0.95 테스트) | KorCCVi + STT 병합 데이터 | 5 | 최종 문맥 판단 모델<br>→ 다양한 기준점 실험 후 기준점 0.8 확정<br>→ FP 최소화, 실사용 모델로 채택 |

---

## 🔍 주요 기능 요약

- 🎙 **음성 수집 및 전처리**: FSS 사이트에서 음성 데이터를 수집하고, mp4 → mp3 → wav 변환 과정을 자동화  
- 🗣 **STT 변환**: Google STT API를 활용해 음성 파일을 텍스트로 변환  
- 🧠 **문맥 기반 보이스 피싱 탐지**: KoBERT 모델을 사용해 텍스트의 의미를 분석하고, 피싱 여부 판단  
- ☎ **전화번호 사기 여부 조회**: 경찰청 사이트 자동화 검색 기능으로, 사용자 입력 전화번호에 대한 피싱 여부 제공

---

## 🏁 실행 순서 (권장)

1. `0_FSS_audio_extract.ipynb`  
2. `1_voice_file_wav_conversion.ipynb`  
3. `2_data_processing.ipynb`  
4. `3_STT.ipynb`  
5. `4_KoBERT_04_Final.ipynb`  
6. `5_phone_checker.ipynb`

---

## 📦 `/executables` 폴더 안내

`Voice-context-Detection/executables` 폴더는 위의 모든 단계별 Jupyter Notebook을 `.py` 형태로 외부 실행 가능한 **스크립트 버전**으로 변환한 디렉토리입니다.

- 서버나 자동화 파이프라인에서 직접 실행 가능한 구조
- Jupyter 환경이 없는 경우에도 CLI 기반으로 전체 워크플로우 실행 가능
- 파일명과 로직은 `.ipynb` 버전과 동일한 기능 수행

> 📌 단, 실행 전 Python 환경 및 경로 설정이 정확히 되어 있어야 합니다.

---

## 💡 참고 사항

- 본 프로젝트는 **한국어 금융 대화문**에서 보이스 피싱을 탐지하기 위한 것으로,  
  문장의 길이나 키워드 분포에 따른 **False Positive** 문제가 주요 고려 대상이었습니다.
- 모델 개선 과정에서 여러 기준점과 학습 전략을 실험하였으며,  
  최종적으로 기준점 0.8에서 안정적인 성능을 보였습니다.

---

## 🔗 참고 링크

- 📞 **전화번호 검색 활용 (전기통신금융사기 신고 대응센터)**  
  https://www.counterscam112.go.kr/phishing/searchPhone.do

- 🧾 **KorCCVi 데이터셋 (Korean Voice Phishing Detection Dataset)**  
  https://github.com/selfcontrol7/Korean_Voice_Phishing_Detection

- 📂 **FSS (금융감독원) 실제 보이스 피싱 음성 데이터**  
  https://www.fss.or.kr/fss/bbs/B0000203/list.do?menuNo=200686&bbsId=&cl1Cd=&pageIndex=10&sdate=&edate=&searchCnd=1&searchWrd=

- 🎧 **정상 음성 데이터셋 (AI Hub - 일상 대화 음성)**  
  https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=470

- 🧠 **모델 실행 시 활용되는 기준점 파일 (구글 드라이브 - 다운로드)**
  https://drive.google.com/file/d/1U-vNzyiAM7a_svYLEx2shYbPGUq-qHKr/view?usp=drive_link
