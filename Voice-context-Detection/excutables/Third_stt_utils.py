# stt_utils.py
import os
from pydub import AudioSegment     # pydub : 오디오 파일을 일정 길이로 나누기 위해 사용
from transformers import pipeline  # transformers.pipeline : HuggingFace에서 Whisper 모델을 불러오기 위해 사

# 🤖 Whisper STT 파이프라인 생성 (모듈 로딩 시 1회만)
# Whisper-small 모델을 사용하여 음성 → 텍스트 변환 수행
asr_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

def transcribe_long_audio(audio_path, chunk_duration=30):
    """
    긴 오디오 파일을 Whisper로 STT 처리하는 함수
    :param audio_path: 오디오 파일 경로 (예: "sample.wav")
    :param chunk_duration: 분할 단위 (초)
    :return: 전체 변환된 텍스트 (str)
    """
    print(f"🎧 오디오 파일 로딩 중: {audio_path}")

    """
    - wav 형식 오디오 파일을 로딩
    - 전체 오디오 길이를 30초 단위로 나눔
    """
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    total_chunks = len(audio) // (chunk_duration * 1000) + 1
    
    print(f"🔄 총 분할 개수: {total_chunks}개 (약 {chunk_duration}초씩)")

    # 각 청크 반복 처리 : 오디오를 30초 단위로 잘라 임시 .wav 파일로 저장
    for idx, i in enumerate(range(0, len(audio), chunk_duration * 1000), start=1):
        chunk = audio[i:i + chunk_duration * 1000]
        chunk_path = f"temp_chunk_{i}.wav"

        print(f"\n⏳ [{idx}/{total_chunks}] Chunk 변환 중... ({chunk_duration}초)")
        chunk.export(chunk_path, format="wav")

        # Whisper 모델로 STT 수행
        try:
            result = asr_pipe(chunk_path)
            text = result.get("text", "")
            chunks.append(text.strip())
            print(f"✅ 변환 완료: \"{text.strip()}\"")
        except Exception as e:
            print(f"❌ 변환 실패: {e}")
            chunks.append("")

        # 임시 파일 제거 및 결과 누적
        os.remove(chunk_path)

    # 최종 첵스트 반환 : 분할된 텍스트들을 공백으로 연결한 전체 텍스트 반
    full_text = " ".join(chunks)
    print("\n📝 전체 추출 텍스트 완료!")
    print("-" * 60)
    print(full_text)
    print("-" * 60)
    return full_text
