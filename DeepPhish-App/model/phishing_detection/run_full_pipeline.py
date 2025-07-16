# run_full_pipeline.py

import os
from pathlib import Path
from First_audio_wav_converter import convert_to_wav
from Second_audio_preprocessor import preprocess_single_wav
from Third_stt_utils import transcribe_long_audio
from Fourth_voicephishing_KoBERT_predictor import predict_phishing_label

# 각 경로 설정
input_dir = r"D:/2025_work/2025_VoicePhshing_Detection_Model/dataset/phishing_dataset/FSS_voicephishing_data/mp4_2"
mp3_output_dir = r"D:/2025_work/2025_VoicePhshing_Detection_Model/dataset/phishing_dataset/FSS_voicephishing_data/mp4_mp3_2"
wav_output_dir = r"D:/2025_work/2025_VoicePhshing_Detection_Model/dataset/phishing_dataset/FSS_voicephishing_data/wav_2"

# ✅ 사용자 입력: 분석할 오디오 파일 경로
input_audio_path = Path("D:/2025_work/2025_VoicePhshing_Detection_Model/dataset/phishing_dataset/FSS_voicephishing_data/mp4_2/2번_3차례 신고된 여성 전화금융사기범 (음성_2).mp4")

# ✅ 1단계: 오디오 wav 변환
print("\n🔊 [1단계] 오디오 WAV 변환 시작")
convert_to_wav(input_dir, mp3_output_dir, wav_output_dir)  # 🛠️ 오타 수정: mp3_outpu8t_dir → mp3_output_dir

# ✅ 2단계: 오디오 전처리 (16kHz mono 변환)
print("\n🎧 [2단계] 오디오 전처리")
raw_wav_path = Path("D:/2025_work/2025_VoicePhshing_Detection_Model/dataset/phishing_dataset/FSS_voicephishing_data/wav_2/2번_3차례 신고된 여성 전화금융사기범 (음성_2).wav")
preprocessed_path = Path("D:/2025_work/2025_VoicePhshing_Detection_Model/dataset/phishing_dataset/FSS_voicephishing_data/processed_stt/processed.wav")
preprocessed_wav_path, _ = preprocess_single_wav(raw_wav_path, preprocessed_path)  # 🛠️ 단일 파일 전처리에 맞게 수정

# ✅ 2-1단계: GridFS 저장
from backend.db.gridfs_uploader import store_wav_to_gridfs
print("\n💾 [2-1단계] 전처리된 WAV 파일 GridFS 저장")
file_id = store_wav_to_gridfs(preprocessed_wav_path, original_filename=input_audio_path.name)

# ✅ 3단계: STT (음성 → 텍스트)
print("\n🗣️ [3단계] STT 변환 중...")
transcribed_text = transcribe_long_audio(str(preprocessed_wav_path))  # 🛠️ 전처리된 경로 사용

# ✅ 4단계: STT 기반 보이스 피싱 탐지
print("\n🧠 [4단계] 보이스피싱 탐지")
label, confidence = predict_phishing_label(transcribed_text)

# ✅ 최종 결과 출력
print("\n✅ [최종 결과]")
print(f"📄 텍스트: {transcribed_text}")
print("DEBUG:", label, confidence)
print(f"🎯 예측 결과: {'보이스피싱' if label[0] == 1 else '정상 통화'} (신뢰도: {confidence[0]:.2f})")
