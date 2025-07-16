import os
import json
from pathlib import Path

# 단계별 함수 import
from First_audio_wav_converter import convert_to_wav
from Second_audio_preprocessor import preprocess_single_wav
from Third_stt_utils import transcribe_long_audio
from Fourth_voicephishing_KoBERT_predictor import predict_phishing_label

# ✅ 전체 파이프라인 실행 함수
def run_full_pipeline(input_audio_path, log_callback=print):
    input_audio_path = Path(input_audio_path)
    log_callback("🚀 [시작] 보이스피싱 탐지 전체 파이프라인 실행")
    log_callback(f"🎧 입력 파일: {input_audio_path.name}")

    temp_dir = input_audio_path.parent
    filename_stem = input_audio_path.stem

    # 🔊 [1단계] mp3/mp4 → wav 변환
    log_callback("🔊 [1단계] mp3/mp4 → wav 변환 중...")
    wav_path = input_audio_path.with_suffix(".wav")  # temp 안에 같은 이름으로 .wav
    convert_to_wav(str(input_audio_path), str(wav_path))
    log_callback(f"✅ WAV 변환 완료 → {wav_path.name}")
    
    # 🛠️ [2단계] 전처리
    log_callback("🛠️ [2단계] wav 전처리 중 (mono, 16kHz)...")
    processed_wav_path = temp_dir / "processed.wav"
    preprocessed_wav_path, _ = preprocess_single_wav(wav_path, processed_wav_path)

    if preprocessed_wav_path is None or not os.path.exists(preprocessed_wav_path):
        log_callback("❌ 전처리 실패 → 파일 없음 또는 처리 실패")
        result = {
            "filename": input_audio_path.name,
            "transcribed_text": None,
            "label": "unknown",
            "probability": 0.0
        }
        log_callback("🏁 [중단] 전처리 실패로 인해 파이프라인 종료\n")
        return json.dumps(result, ensure_ascii=False)

    log_callback(f"✅ 전처리 완료 → {preprocessed_wav_path.name}")

    # 🗣️ [3단계] STT
    log_callback("🗣️ [3단계] 음성 텍스트 변환 (STT)...")
    transcribed_text = transcribe_long_audio(str(preprocessed_wav_path))

    if not transcribed_text or not isinstance(transcribed_text, str) or transcribed_text.strip() == "":
        log_callback("❌ STT 실패: 변환된 텍스트가 없음 → 문맥 분석 생략")
        result = {
            "filename": input_audio_path.name,
            "transcribed_text": None,
            "label": "unknown",
            "probability": 0.0
        }
        log_callback("🏁 [중단] STT 실패로 인해 파이프라인 종료\n")
        return json.dumps(result, ensure_ascii=False)

    log_callback("✅ 텍스트 변환 완료")

    # 🧠 [4단계] 보이스피싱 탐지
    log_callback("🧠 [4단계] KoBERT 기반 문맥 분석 중...")
    label, confidence = predict_phishing_label(transcribed_text)
    log_callback(f"✅ 탐지 완료 → 라벨: {'phishing' if label[0] == 1 else 'normal'}, 확률: {round(confidence[0], 4)}")

    # 🎯 [5단계] 결과 구성 및 반환
    result = {
        "file_name": input_audio_path.name,
        "transcribed_text": transcribed_text,
        "label": "phishing" if label[0] == 1 else "normal",
        "probability": round(confidence[0], 4)
    }


    # 🧹 임시파일 삭제
    for f in [input_audio_path, wav_path, processed_wav_path]:
        if f.exists():
            try:
                f.unlink()
                log_callback(f"🧹 임시 파일 삭제 완료: {f.name}")
            except Exception as e:
                log_callback(f"⚠️ 임시 파일 삭제 실패: {f.name} → {e}")

    log_callback("🎯 [완료] 파이프라인 결과 반환\n")
    return json.dumps(result, ensure_ascii=False)

