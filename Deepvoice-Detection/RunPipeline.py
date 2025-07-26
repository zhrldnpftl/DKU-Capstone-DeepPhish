import torch
import json
import os

# 변환/추론 관련 함수들 import
from .mp3TOwav import convert_file_to_wav
from .make_melspectrogram import wav_to_melspectrogram
from .ModelLoader import load_model

# 판별 기준이 되는 threshold
THRESHOLD = 0.8

# 전체 파이프라인을 실행하는 함수 (mp3 → label + 확률 반환)
# log_callback: 로그를 실시간으로 보내기 위한 콜백 함수 (기본은 print)
def run_inference(mp3_path, log_callback=print):
    log_callback("🚀 [시작] 딥보이스 탐지 파이프라인 실행")
    log_callback(f"🎧 입력 파일: {os.path.basename(mp3_path)}")

    # 🔊 [1단계] mp3 → wav 변환
    wav_path = mp3_path.replace(".mp3", ".wav").replace(".mp4", ".wav")
    log_callback("🔊 [1단계] 파일 → wav 변환 중...")
    convert_file_to_wav(mp3_path, wav_path)
    log_callback(f"✅ WAV 저장 완료 → {os.path.basename(wav_path)}")

    # 📊 [2단계] Mel-spectrogram 변환
    log_callback("📊 [2단계] Mel-spectrogram 변환 중...")
    mel_np = wav_to_melspectrogram(wav_path)  # (T, 80) or (300, 80)
    mel_np = mel_np.T  # (80, T) 형태로 전치
    mel_spec = torch.tensor(mel_np, dtype=torch.float32).unsqueeze(0)  # (1, 80, T)
    log_callback("✅ Mel-spectrogram 생성 완료")

    # 📦 [3단계] 모델 로드
    log_callback("📦 [3단계] 딥보이스 탐지 모델 로드 중...")
    model_path = os.path.join(os.path.dirname(__file__), "modelWithThreshold.pt")
    model = load_model(model_path)
    log_callback("✅ 모델 로드 완료")

    # 🧠 [4단계] 추론 실행
    log_callback("🧠 [4단계] 추론 실행 중...")
    with torch.no_grad():
        output = model(mel_spec)  # (1, 2)
        prob = torch.softmax(output, dim=1)[0, 1].item()  # 1번 클래스 확률
    log_callback(f"✅ 추론 완료 → 확률: {round(prob, 4)}")


    # 🎯 [5단계] 결과 처리
    result = {
        "label": "fake" if prob >= THRESHOLD else "real",
        "probability": round(prob, 4)
    }

    log_callback(f"🎯 [결과] 라벨: {result['label']} / 확률: {result['probability']}")
    log_callback("🏁 [완료] 딥보이스 탐지 종료\n")

    return json.dumps(result)
