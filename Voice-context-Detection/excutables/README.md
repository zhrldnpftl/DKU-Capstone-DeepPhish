# 🎯 Voice Phishing Detection Pipeline - Python Scripts Overview

이 저장소는 **보이스 피싱 탐지**를 위한 전체 파이프라인을 단계별로 구현한 Python 스크립트 모음입니다.  
각 단계는 오디오 처리, STT, 문맥 분석, 전화번호 조회로 구성되어 있으며, 실시간 탐지 시스템의 구성요소입니다.

---

## 📁 실행 파일 설명

| 단계 | 파일명 | 목적 및 설명 |
|------|--------|--------------|
| 1단계 | `First_audio_wav_converter.py` | 🎵 **오디오 변환기**<br>FSS에서 수집한 `.mp4` 또는 `.mp3` 파일을 `.wav` 형식(16kHz, mono)으로 변환합니다.<br>→ `moviepy`로 mp4 → mp3 변환 후, `pydub`으로 wav로 재변환합니다. |
| 2단계 | `Second_audio_preprocessor.py` | 🛠 **오디오 전처리기**<br>피싱/일반 오디오를 16kHz, mono로 통일해 저장하며, 변환된 파일들의 경로·레이블·길이를 CSV로 기록합니다.<br>→ 패딩 없이 전처리만 수행합니다. |
| 3단계 | `Third_stt_utils.py` | 🗣 **STT 처리기**<br>Whisper 모델(`openai/whisper-small`)을 사용하여 긴 오디오 파일을 30초 단위로 나누고, 각 구간을 STT 처리합니다.<br>→ 결과 텍스트를 하나로 합쳐 반환합니다. |
| 4단계 | `Fourth_voicephishing_KoBERT_predictor.py` | 📚 **문맥 기반 피싱 판별기**<br>STT로 얻은 문장을 KoBERT 기반 분류기로 분석하여 보이스피싱 여부를 판단합니다.<br>→ Softmax 확률 기반으로 confidence(신뢰도)를 출력하며, threshold 조절 가능 (`0.8` 기본). |
| 5단계 | `Fifth_phone_checker.py` | 🔍 **전화번호 조회기**<br>경찰청 보이스피싱 신고 조회 사이트를 크롤링하여 전화번호 신고 이력을 확인합니다.<br>→ 총 신고 수, 음성 피싱 건수, 문자 피싱 건수를 반환합니다. |
| 보조 | `run_audio_wav_converter.py` | ▶️ **변환 스크립트 실행 파일**<br>`First_audio_wav_converter.py`를 호출하여 입력된 디렉토리의 mp4/mp3를 일괄적으로 wav로 변환하는 테스트 실행 예시입니다. |

---

## 💡 실행 순서

1. `run_audio_wav_converter.py` 또는 `First_audio_wav_converter.py`  
2. `Second_audio_preprocessor.py`  
3. `Third_stt_utils.py`  
4. `Fourth_voicephishing_KoBERT_predictor.py`  
5. (선택) `Fifth_phone_checker.py` – 전화번호가 존재할 경우

---

## 🛠 개발 환경 및 주요 패키지

- Python >= 3.8
- moviepy
- pydub
- librosa
- soundfile
- transformers (HuggingFace)
- selenium (ChromeDriver 필요)
- torch / kobert-transformers



