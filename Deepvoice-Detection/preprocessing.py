# google colab 기반 전처리 진행 코드 (전처리된 파일이 구글 드라이브에 저장되는 형태)

# 1. 라이브러리 설치
# Google Colab 환경에서 필요한 패키지 설치
!pip install datasets torchaudio kagglehub
# Hugging Face datasets, 오디오 처리용 torchaudio, kagglehub

# 라이브러리 import
import os                                    # 경로 조작용
import kagglehub                             # KaggleHub를 통해 kagglehub dataset 다운로드
from datasets import load_dataset, Audio     # HuggingFace datasets API 및 오디오 타입
import torch                                 # PyTorch - 텐서 처리
import torchaudio                            # 오디오 처리용 torchaudio
import torchaudio.transforms as T            # torchaudio에서 제공하는 오디오 변환 함수들
import numpy as np                           # 넘파이 배열 연산
import matplotlib.pyplot as plt              # 시각화 도구
import glob                                  # 파일 탐색용
from google.colab import drive               # Google Drive 연동
from itertools import islice
from tqdm import tqdm

# 2. 구글 드라이브 저장 및 저장 경로 설정
# Google Drive를 마운트 (연결)
drive.mount('/content/drive')  # 브라우저에 인증 링크 제공

# 전처리 결과 저장 경로 설정
save_dir = "/content/drive/MyDrive/Capstone"  # Google Drive 내 Capstone 폴더 경로
os.makedirs(save_dir, exist_ok=True)          # 폴더가 없으면 생성

# label_0, label_1 하위 폴더 경로 정의
label0_dir = os.path.join(save_dir, "label_0")
label1_dir = os.path.join(save_dir, "label_1")

# 폴더가 없다면 생성
os.makedirs(label0_dir, exist_ok=True)
os.makedirs(label1_dir, exist_ok=True)

# 3. 전처리 설정 및 함수 정의
# 전처리용 파라미터 정의
SAMPLE_RATE = 16000           # 모든 오디오를 16kHz로 맞춤
N_MELS = 80                   # Mel-spectrogram에서 사용할 Mel 밴드 수
MAX_DURATION = 3              # 최대 허용 오디오 길이 (초)
HOP_LENGTH = 160              # Mel-spectrogram 프레임 간 간격
MAX_FRAMES = int((SAMPLE_RATE / HOP_LENGTH) * MAX_DURATION)  # 3초 기준 최대 프레임 수
# Mel-spectrogram 변환기 정의
mel_transform = T.MelSpectrogram(
    sample_rate=SAMPLE_RATE,  # 목표 샘플레이트
    n_fft=400,                # FFT 크기
    hop_length=HOP_LENGTH,    # 프레임 간 이동 간격
    n_mels=N_MELS             # Mel 밴드 수
)

# Amplitude를 로그 스케일로 변환 (dB)
amplitude_to_db = T.AmplitudeToDB()
# 오디오 전처리 함수 정의
def preprocess_audio(waveform, sample_rate):

    waveform = waveform.to(torch.float32)  # float64 → float32 변환
    # 샘플레이트가 16kHz가 아니면 리샘플링
    if sample_rate != SAMPLE_RATE:
        resampler = T.Resample(orig_freq=sample_rate, new_freq=SAMPLE_RATE)
        waveform = resampler(waveform)

    # stereo인 경우 → mono로 평균 처리
    if waveform.shape[0] == 2:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Mel-spectrogram 생성
    mel_spec = mel_transform(waveform)

    # 로그 스케일로 변환
    log_mel = amplitude_to_db(mel_spec).squeeze(0)

    # 시간 축 길이 고정 (패딩 or 잘라내기)
    if log_mel.shape[1] < MAX_FRAMES:
        log_mel = torch.nn.functional.pad(log_mel, (0, MAX_FRAMES - log_mel.shape[1]))
    else:
        log_mel = log_mel[:, :MAX_FRAMES]

    # numpy 배열로 반환
    return log_mel.numpy().astype(np.float32)

# 4. people's speech 전처리 진행 (정상 데이터)
# HuggingFace에서 스트리밍 방식으로 clean dataset 로드
print(" People's Speech 데이터 전처리 중...")
people_ds = load_dataset("MLCommons/peoples_speech", "clean", split="train", streaming=True)

# 오디오 컬럼을 16kHz로 디코딩하도록 지정
people_ds = people_ds.cast_column("audio", Audio(sampling_rate=SAMPLE_RATE, decode=True))
# 스트리밍 데이터셋에서 하나씩 불러와 전처리 수행
for idx, sample in enumerate(people_ds):
    try:
        waveform = torch.tensor(sample["audio"]["array"]).unsqueeze(0)  # numpy → torch tensor
        features = preprocess_audio(waveform, SAMPLE_RATE)              # 전처리 수행

        # 저장
        np.save(os.path.join(label0_dir, f"sample_{idx:05d}.npy"), features) # 라벨 0에 저장
        # 상태 출력
        if idx % 500 == 0:
            print(f" 정상 샘플 처리됨: {idx}개")

       # if idx == 1000: break
    except Exception as e:
        print(f"오류 발생 (index {idx}): {e}")

    # 테스트 목적: 일부 샘플만 처리할 경우 사용
    # if idx == 1000: break

# 5. Fake or Real 전처리 진행 (비정상 데이터)
# Fake or Real 데이터셋 다운로드 및 파일 목록 생성
print("Fake or Real 데이터 전처리 중...")
fake_path = kagglehub.dataset_download("mohammedabdeldayem/the-fake-or-real-dataset")
audio_files = glob.glob(os.path.join(fake_path, "**/*.wav"), recursive=True)  # 모든 .wav 파일 탐색

# 각 오디오 파일에 대해 전처리 수행
for idx, path in enumerate(audio_files):
    try:
        waveform, sample_rate = torchaudio.load(path)            # 오디오 로드
        features = preprocess_audio(waveform, SAMPLE_RATE)       # 전처리 수행

        # 저장
        np.save(os.path.join(label1_dir, f"sample_{idx:05d}.npy"), features) # 라벨 1에 저장

        if idx % 200 == 0:
            print(f"딥보이스 샘플 처리됨: {idx}개")
       # if idx == 1000: break
    except Exception as e:
        print(f"오류 발생 (file: {path}): {e}")

    # if idx == 1000: break  # 일부만 처리할 경우 사용
