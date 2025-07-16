# make_melspectrogram.py (수정 버전)
import torch
import torchaudio
import torchaudio.transforms as T
import numpy as np

# 전처리 파라미터
SAMPLE_RATE = 16000
N_MELS = 80
N_FFT = 400
HOP_LENGTH = 160
MAX_DURATION = 3
MAX_FRAMES = int((SAMPLE_RATE / HOP_LENGTH) * MAX_DURATION)

# 전처리 함수
def wav_to_melspectrogram(wav_path):
    waveform, sample_rate = torchaudio.load(wav_path)
    waveform = waveform.to(torch.float32)

    # 리샘플링
    if sample_rate != SAMPLE_RATE:
        resampler = T.Resample(orig_freq=sample_rate, new_freq=SAMPLE_RATE)
        waveform = resampler(waveform)

    # 스테레오 → 모노
    if waveform.shape[0] == 2:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Mel 변환 및 로그 스케일
    mel_transform = T.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS
    )
    amplitude_to_db = T.AmplitudeToDB()
    mel_spec = mel_transform(waveform)
    log_mel = amplitude_to_db(mel_spec).squeeze(0)

    # 길이 고정
    if log_mel.shape[1] < MAX_FRAMES:
        log_mel = torch.nn.functional.pad(log_mel, (0, MAX_FRAMES - log_mel.shape[1]))
    else:
        log_mel = log_mel[:, :MAX_FRAMES]
        
    log_mel = torch.clamp(log_mel, -80, 30)
    log_mel = (log_mel + 80) / 110
 

    return log_mel.numpy().astype(np.float32)
