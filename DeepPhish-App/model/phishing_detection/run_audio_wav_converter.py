# 🔨 main.py
from executables.audio_wav_converter import convert_to_wav

# 경로 설정 (r"" 사용 → 역슬래시 이스케이프 오류 방지)
input_dir = r"D:\2025_work\2025_VoicePhshing_Detection_Model\dataset\phishing_dataset\FSS_voicephishing_data\mp4_2"
mp3_output_dir = r"D:\2025_work\2025_VoicePhshing_Detection_Model\dataset\phishing_dataset\FSS_voicephishing_data\mp4_mp3"
wav_output_dir = r"D:\2025_work\2025_VoicePhshing_Detection_Model\dataset\phishing_dataset\FSS_voicephishing_data\wav_2"

# 함수 실행
convert_to_wav(input_dir, mp3_output_dir, wav_output_dir)
