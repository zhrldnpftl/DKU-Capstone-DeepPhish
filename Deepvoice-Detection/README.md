# Deepvoice-Detection

사용자의 통화 음성 파일을 Mel-spectrogram과(CNN) 시간에 따른 음성의 특성을 기반(LSTM)으로 분석하여 딥보이스 여부를 판단하는 프로젝트이다.  
본 폴더는 전체 딥보이스 탐지 파이프라인을 담고 있으며, 모델의 학습부터 시스템 적용까지의 기능을 포함하고 있다. 

---

## 파일 구성 및 역할 (학습단계 1-3 / 활용단계 4-7)

| 단계 | 파일명 | 역할 |
|------|--------|------|
| 1단계 | `preprocessing.py` | 학습 데이터 전처리 수행 (데이터 추출 ~ Mel-spectrogram 변환) |
| 2단계 | `MakeBatch.py` | 전처리된 데이터를 배치 단위 `.npy` 파일로 저장 (선택 사항) |
| 3단계 | `CNNLSTM.py`, `Model_Threshold.py` | CNN+LSTM 딥보이스 탐지 모델 학습 |
| 4단계 | `mp3TOwav.py` | mp3/mp4 파일을 16kHz mono `.wav` 파일로 변환 |
| 5단계 | `make_melspectrogram.py` | `.wav` → log-Mel Spectrogram 변환 및 정규화 |
| 6단계 | `ModelLoader.py` | 모델 구조 정의 및 학습된 `.pt` 모델 로딩 |
| 7단계 | `RunPipeline.py` | 전체 파이프라인 실행 (mp3 → Mel → 추론 → 결과 반환)

---

## 딥보이스 탐지 모델(CNNLSTM) 개선 단계 요약

전처리된 통화 데이터를 음성의 특징에 따라 분석하기 위해 CNNLSTM 기반 하이브리드 모델을 여러 단계에 걸쳐 개선하였습니다.
최종 학습 (3-6)을 제외한 모든 단계는 정상 데이터와 비정상 데이터를 각 5000개씩 묶은 배치 폴더 15개에서 랜덤으로 3000개를 뽑아 학습을 진행하였다. 검증 데이터로 학습에 사용되지 않은 정상 데이터와 비정상 데이터 중 1000개를 뽑아 사용하였다. 검증 데이터는 모델마다 학습 진행 시 랜덤으로 고정하여 사용하였으므로 모두 상이하다.
3-2단계부터 3-5단계까지는 기준점에 따른 모델 성능 평가를 위하여 동일한 모델에 기준점 환경만 변경하여 사용하였다.

| 단계 | 파일명 | 기준점 | 학습 데이터 | Epoch | 목적 |
|------|--------|--------|-------------|--------|------|
| 3-1단계 | CNNLSTM | 없음 | People’s Speech + Fake or Real | 3 | 기준점 없이 분류 진행. 데이터가 매 epoch마다 랜덤 배정되어 Loss 변동성 존재 |
| 3-2단계 | Model_Threshold | 0.7 | 동일 | 3 | 검증 데이터 고정. 위양성 18 / 위음성 1 / 정확도 98% |
| 3-3단계 | Model_Threshold | 0.8 | 동일 | 3 | 기준점 0.8에서 위양성 33 / 위음성 6 |
| 3-4단계 | Model_Threshold | 0.9 | 동일 | 3 | 기준점 0.9에서 위양성 80 / 위음성 3 |
| 3-5단계 | Model_Threshold | 0.95 | 동일 | 3 | 기준점 0.9와 큰 차이 없음 |
| 3-6단계 | Model_Threshold | 0.8 | 20개 배치 | 10 | 기준점 0.8, 데이터 확장으로 학습 진행 → 최종 모델 `modelWithThreshold.pt` 생성 (정확도 99%)

---

## 주요 기능 요약

- **음성 파일 변환**: mp3 또는 mp4 파일을 16kHz, mono 채널의 `.wav`로 변환
- **Mel-spectrogram 생성**: log-Mel Spectrogram으로 변환 후 정규화 및 길이 고정
- **딥보이스 탐지**: CNN + LSTM 모델을 통해 음성이 Deepfake인지 판별
- **추론 결과 출력**: 확률과 함께 `real` / `fake` 판별 결과를 JSON으로 출력

---

## 실행 순서

1. `preprocessing.py`  
2. `MakeBatch.py`  
3. `Model_Threshold.py` (학습된 모델 저장)  
4. `mp3TOwav.py`  
5. `make_melspectrogram.py`  
6. `ModelLoader.py`  
7. `RunPipeline.py`

---

## 참고 링크

### 데이터셋

- Fake or Real (FoR Dataset):  
  https://www.kaggle.com/datasets/mohammedabdeldayem/the-fake-or-real-dataset/code

- People’s Speech:  
  https://huggingface.co/datasets/MLCommons/peoples_speech_v1.0

### Colab 코드 링크

- preprocessing.py  
  https://colab.research.google.com/drive/1mLSS_4ckM9oleYUi1N4bDqCfkvbBdoi0?usp=sharing

- MakeBatch.py  
  https://colab.research.google.com/drive/19ly-8lahEysif-GX7EK8gezxxJvjb-Xe?usp=sharing

- CNNLSTM.py  
  https://colab.research.google.com/drive/1yFcwrr__mzLSpxEp1p9dK8shKneAlqrY?usp=sharing

- Model_Threshold.py  
  https://colab.research.google.com/drive/1gh2Uc1t1TeYRYb7XNGkoyex0GbOANwO0?usp=sharing

- mp3TOwav.py  
  https://colab.research.google.com/drive/1NKmwJGE1Uz37QmgJ-OfjbiFJG3r_bRJT?usp=sharing

- make_melspectrogram.py  
  https://colab.research.google.com/drive/1QLtUlMrZ4Hgg3vfOvakIcFyiEXpTY48a?usp=sharing

- ModelLoader.py  
  https://colab.research.google.com/drive/1Hbe_KkVYTxGgjtB73BZE5Yth3OWwS3Dk?usp=sharing

- RunPipeline.py  
  https://colab.research.google.com/drive/1mewU0k4bVzf70PrpX6gb86D1Yl_cusMl?usp=sharing

