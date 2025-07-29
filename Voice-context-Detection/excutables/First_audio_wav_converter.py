# 🔧 audio_converter.py
import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def convert_to_wav(input_dir, mp3_output_dir, wav_output_dir):
    """
    입력 디렉토리에서 mp4/mp3 파일을 읽어 wav로 변환
    """
    os.makedirs(mp3_output_dir, exist_ok=True)
    os.makedirs(wav_output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        base_filename, ext = os.path.splitext(filename)

        try:
            if ext.lower() == ".mp4":
                mp3_path = os.path.join(mp3_output_dir, base_filename + ".mp3")
                wav_path = os.path.join(wav_output_dir, base_filename + ".wav")

                video = VideoFileClip(input_path)
                video.audio.write_audiofile(mp3_path)
                print(f"🎵 MP3 변환 완료: {base_filename}.mp3")

                audio = AudioSegment.from_mp3(mp3_path)
                audio = audio.set_frame_rate(16000).set_channels(1)
                audio.export(wav_path, format="wav")
                print(f"🎧 WAV 변환 완료: {base_filename}.wav")

            elif ext.lower() == ".mp3":
                wav_path = os.path.join(wav_output_dir, base_filename + ".wav")

                audio = AudioSegment.from_mp3(input_path)
                audio = audio.set_frame_rate(16000).set_channels(1)
                audio.export(wav_path, format="wav")
                print(f"🎧 WAV 변환 완료: {base_filename}.wav")

            else:
                print(f"⏭️ 지원되지 않는 형식: {filename} → 건너뜀")

        except Exception as e:
            print(f"❌ 변환 실패 ({filename}): {e}")