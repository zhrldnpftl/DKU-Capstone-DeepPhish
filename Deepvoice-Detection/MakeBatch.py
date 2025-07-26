import os
import shutil

# 경로 설정
src_dir = r"G:\내 드라이브\Capstone\label_0"  # label_0이 있는 폴더 경로
dst_root = r"G:\내 드라이브\Capstone\0"       # 이동 대상 폴더
batch_size = 5000

# .npy 파일 목록 정렬
all_files = sorted([f for f in os.listdir(src_dir) if f.endswith('.npy')])

print(f"총 파일 수: {len(all_files)}")

# 5000개씩 나눠서 이동
for i in range(0, len(all_files), batch_size):
    batch_files = all_files[i:i+batch_size]
    batch_folder = os.path.join(dst_root, f"batch_{i//batch_size:03d}")
    os.makedirs(batch_folder, exist_ok=True)

    for f in batch_files:
        src_path = os.path.join(src_dir, f)
        dst_path = os.path.join(batch_folder, f)
        try:
            shutil.move(src_path, dst_path)
        except Exception as e:
            print(f"❌ {f} 이동 실패: {e}")
    
    print(f"✅ {batch_folder} 완료 ({len(batch_files)}개 이동됨)")
