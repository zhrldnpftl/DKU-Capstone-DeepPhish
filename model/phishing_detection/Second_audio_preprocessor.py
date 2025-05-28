# 📄 Second_audio_preprocessor.py

from pathlib import Path
import os
import librosa
import soundfile as sf
import csv

# ✅ 단일 wav 파일 전처리용 함수 추가

def preprocess_single_wav(wav_path, output_path, sample_rate=16000):
    """
    🎯 단일 WAV 파일을 16kHz, mono로 변환하여 저장하는 함수

    :param wav_path: 원본 WAV 파일 경로
    :param output_path: 전처리된 WAV 파일 저장 경로
    :param sample_rate: 목표 샘플링 주파수 (기본값: 16000Hz)
    :return: 저장된 파일 경로, duration (초)
    """
    try:
        # 1️⃣ 오디오 로딩 (librosa로 파일 불러오며, 16kHz로 리샘플링 + 모노 변환)
        y, _ = librosa.load(wav_path, sr=sample_rate, mono=True)

        # 2️⃣ 오디오 저장 (soundfile로 지정된 경로에 .wav로 저장)
        sf.write(output_path, y, sample_rate)

        # 3️⃣ 길이 계산 (샘플 개수 ÷ 샘플레이트로 재생 시간 계산)
        duration = round(len(y) / sample_rate, 2)

        # 4️⃣ 성공 메시지 출력 및 경로, 길이 반환
        print(f"✅ 전처리 완료: {output_path.name} ({duration} sec)")
        return output_path, duration

    except Exception as e:
        # ❌ 에러 발생 시 경고 메시지 출력 및 None 반환
        print(f"❌ 전처리 실패: {wav_path.name} - {e}")
        return None, None
