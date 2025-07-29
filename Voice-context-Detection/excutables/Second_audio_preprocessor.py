# audio_preprocessor.py

from pathlib import Path
import os
import librosa
import soundfile as sf
import csv

def preprocess_wav_files_without_padding(phishing_wav_dir: Path, normal_wav_dir: Path,
                                          output_dir: Path, output_csv_path: Path,
                                          sample_rate: int = 16000):
    """
    📦 피싱/일반 오디오 데이터를 16kHz mono로 변환하고, 메타데이터를 CSV로 저장하는 전처리 함수
    - padding 없이 변환만 수행
    """

    # 📁 출력 디렉토리 생성
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # 🔍 입력 디렉토리 정보 출력
    print(f"📂 phishing 디렉토리: {phishing_wav_dir}")
    print(f"📂 normal 디렉토리: {normal_wav_dir}")

    # 🔍 .wav 파일만 추출
    phishing_files = [phishing_wav_dir / f for f in os.listdir(phishing_wav_dir) if f.endswith(".wav")]
    normal_files = [normal_wav_dir / f for f in os.listdir(normal_wav_dir) if f.endswith(".wav")]

    print(f"🔎 phishing 파일 수: {len(phishing_files)}개")
    print(f"🔎 normal 파일 수: {len(normal_files)}개")

    # 🔁 메타데이터 CSV 파일 열기
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label", "path", "duration_sec"])

        def process_and_save(file_path, label, new_filename):
            try:
                # 1️⃣ 오디오 로딩 및 16kHz/mono 변환
                y, _ = librosa.load(file_path, sr=sample_rate, mono=True)

                # 2️⃣ 저장할 경로
                output_path = output_dir / new_filename

                # 3️⃣ wav 저장
                sf.write(output_path, y, sample_rate)

                # 4️⃣ 길이(초) 계산
                duration = round(len(y) / sample_rate, 2)

                return output_path, duration

            except Exception as e:
                print(f"⚠️ 변환 실패: {file_path.name} - {e}")
                return None, None

        # 🟠 피싱 오디오 처리
        print("\n📤 피싱 오디오 처리 시작...")
        for path in phishing_files:
            name = f"phishing_{path.name}"
            out_path, dur = process_and_save(path, 1, name)
            if out_path:
                writer.writerow([name, 1, str(out_path), dur])
                print(f"✅ 저장 완료 (phishing): {name} ({dur} sec)")

        # 🔵 일반 오디오 처리
        print("\n📤 일반 오디오 처리 시작...")
        for path in normal_files:
            name = f"normal_{path.name}"
            out_path, dur = process_and_save(path, 0, name)
            if out_path:
                writer.writerow([name, 0, str(out_path), dur])
                print(f"✅ 저장 완료 (normal): {name} ({dur} sec)")

    print(f"\n📄 메타데이터 저장 완료: {output_csv_path}")

# ✨ 사용 예시
if __name__ == "__main__":
    phishing_dir = Path("D:/.../phishing")  # 입력 경로 수정
    normal_dir = Path("D:/.../normal")
    output_dir = Path("D:/.../processed")
    csv_path = Path("D:/.../processed_metadata.csv")

    preprocess_wav_files_without_padding(
        phishing_wav_dir=phishing_dir,
        normal_wav_dir=normal_dir,
        output_dir=output_dir,
        output_csv_path=csv_path,
        sample_rate=16000
    )
