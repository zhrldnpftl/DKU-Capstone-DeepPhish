# phishing_detection/RunPipelin.py

# run_full_pipeline.py

import os
import json
from pathlib import Path

# 단계별 함수 import
from First_audio_wav_converter import convert_to_wav
from Second_audio_preprocessor import preprocess_single_wav
from Third_stt_utils import transcribe_long_audio
from Fourth_voicephishing_KoBERT_predictor import predict_phishing_label
from backend.db.gridfs_uploader import store_wav_to_gridfs

# ✅ 전체 파이프라인 실행 함수
def run_full_pipeline(input_audio_path):
    input_audio_path = Path(input_audio_path)

    # 경로 설정
    input_dir = input_audio_path.parent
    filename_stem = input_audio_path.stem
    filename_wav = f"{filename_stem}.wav"

    # 중간 경로 (mp3, wav, processed wav)
    mp3_output_dir = input_dir.parent / "mp4_mp3_2"
    wav_output_dir = input_dir.parent / "wav_2"
    processed_wav_path = input_dir.parent / "processed_stt" / "processed.wav"

    # ✅ 1단계: WAV 변환
    convert_to_wav(str(input_dir), str(mp3_output_dir), str(wav_output_dir))

    # ✅ 2단계: 전처리 (mono 16kHz 변환)
    raw_wav_path = wav_output_dir / filename_wav
    preprocessed_wav_path, _ = preprocess_single_wav(raw_wav_path, processed_wav_path)

    # ✅ 2-1단계: GridFS에 저장
    file_id = store_wav_to_gridfs(preprocessed_wav_path, original_filename=input_audio_path.name)

    # ✅ 3단계: STT
    transcribed_text = transcribe_long_audio(str(preprocessed_wav_path))

    # ✅ 4단계: 보이스피싱 탐지
    label, confidence = predict_phishing_label(transcribed_text)

    # ✅ 결과 JSON 반환
    result = {
        "filename": input_audio_path.name,
        "transcribed_text": transcribed_text,
        "label": "phishing" if label[0] == 1 else "normal",
        "probability": round(confidence[0], 4),
        "file_id": str(file_id)
    }

    return json.dumps(result, ensure_ascii=False)
