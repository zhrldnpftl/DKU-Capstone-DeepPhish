# 🔧 audio_converter.py
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os

def convert_to_wav(input_path, wav_output_path):
    """
    단일 mp3 또는 mp4 파일을 받아서 wav로 변환 (16000Hz, mono)
    """
    _, ext = os.path.splitext(input_path)
    ext = ext.lower()

    try:
        if ext == ".mp4":
            # mp4 → mp3 → wav
            temp_mp3_path = input_path.replace(".mp4", ".temp.mp3")
            video = VideoFileClip(input_path)
            video.audio.write_audiofile(temp_mp3_path)
            print(f"🎵 임시 MP3 추출 완료: {os.path.basename(temp_mp3_path)}")

            audio = AudioSegment.from_mp3(temp_mp3_path)
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_output_path, format="wav")
            print(f"🎧 WAV 변환 완료: {os.path.basename(wav_output_path)}")

            os.remove(temp_mp3_path)  # 임시 mp3 삭제

        elif ext == ".mp3":
            audio = AudioSegment.from_mp3(input_path)
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_output_path, format="wav")
            print(f"🎧 WAV 변환 완료: {os.path.basename(wav_output_path)}")

        else:
            raise ValueError(f"지원되지 않는 형식: {ext}")

    except Exception as e:
        raise RuntimeError(f"❌ 변환 실패 ({os.path.basename(input_path)}): {e}")
