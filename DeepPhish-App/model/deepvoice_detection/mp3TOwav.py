import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def convert_file_to_wav(input_path: str, output_wav_path: str, target_rate=16000):
    """
    mp3 또는 mp4 파일을 입력 받아 wav 파일로 변환 (16kHz, mono)
    """
    base_filename, ext = os.path.splitext(os.path.basename(input_path))

    try:
        if ext.lower() == ".mp4":
            # mp4 → mp3 임시 변환
            temp_mp3_path = os.path.join(os.path.dirname(output_wav_path), base_filename + "_temp.mp3")
            video = VideoFileClip(input_path)
            video.audio.write_audiofile(temp_mp3_path)
            print(f"🎵 MP4 → MP3 변환 완료: {temp_mp3_path}")

            # mp3 → wav 변환
            audio = AudioSegment.from_mp3(temp_mp3_path)
            audio = audio.set_frame_rate(target_rate).set_channels(1)
            audio.export(output_wav_path, format="wav")
            print(f"🎧 WAV 변환 완료: {output_wav_path}")

            # 임시 mp3 삭제
            os.remove(temp_mp3_path)

        elif ext.lower() == ".mp3":
            audio = AudioSegment.from_mp3(input_path)
            audio = audio.set_frame_rate(target_rate).set_channels(1)
            audio.export(output_wav_path, format="wav")
            print(f"🎧 WAV 변환 완료: {output_wav_path}")

        else:
            raise ValueError(f"지원되지 않는 파일 형식: {ext}")

    except Exception as e:
        print(f"❌ 변환 실패 ({input_path}): {e}")
        raise
