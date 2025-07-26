# ✅ 필요한 라이브러리 임포트
import os  # 파일 경로 및 디렉토리 작업을 위한 모듈
import time  # 시간 측정을 위한 모듈
import sys  # tqdm 출력 조절을 위한 시스템 모듈
import torch  # PyTorch 기본 모듈
import torch.nn as nn  # 신경망 레이어 모듈
import torch.optim as optim  # 옵티마이저 모듈
import numpy as np  # 수치 계산 모듈
from torch.utils.data import Dataset, DataLoader, ConcatDataset  # 데이터셋 및 로더 관련
from tqdm import tqdm  # 학습 진행 시각화
import torch.nn.functional as F  # softmax 등 함수 제공

# ✅ 배치 폴더에서 최대 max_files개의 .npy 파일 경로 수집
# - 파일이 존재하는 경우 npy 파일만 추출하여 무작위로 섞고 max_files개 반환

def get_npy_paths_from_batch(batch_path, max_files=3000):
    if not os.path.exists(batch_path):  # 폴더가 없으면 빈 리스트 반환
        return []
    files = [os.path.join(batch_path, f) for f in os.listdir(batch_path) if f.endswith('.npy')]  # npy 파일 목록
    np.random.shuffle(files)  # 무작위 셔플
    return files[:max_files]  # 상위 max_files개만 반환

# ✅ npy 파일을 불러와 텐서로 변환하는 Dataset 클래스
# - 에러 발생 시 다음 인덱스로 우회 로딩

class SubsetNpyDataset(Dataset):
    def __init__(self, file_paths, label):  # 파일 경로 리스트와 라벨
        self.file_paths = file_paths
        self.label = label

    def __len__(self):  # 전체 샘플 개수 반환
        return len(self.file_paths)

    def __getitem__(self, idx):  # 인덱스에 해당하는 텐서 반환
        try:
            npy_array = np.load(self.file_paths[idx])  # (80, 300)
            npy_array = npy_array.T  # (300, 80)
            npy_array = np.clip(npy_array, -80, 30)  # 클리핑
            npy_array = (npy_array + 80) / 110  # 정규화 (0~1)
            tensor = torch.tensor(npy_array, dtype=torch.float32)  # Tensor 변환
            return tensor, self.label  # 텐서와 라벨 반환
        except Exception as e:
            print(f"⚠️ {self.file_paths[idx]} 불러오기 실패 - {e}")  # 에러 출력
            return self.__getitem__((idx + 1) % len(self))  # 다음 샘플로 우회

# ✅ CNN + LSTM 하이브리드 모델 정의
# - CNN으로 특징 추출 후 LSTM으로 시계열 학습 → FC로 분류

class CNNLSTM(nn.Module):
    def __init__(self, input_channels):
        super(CNNLSTM, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv1d(input_channels, 128, kernel_size=5, padding=2),  # 1D Convolution
            nn.BatchNorm1d(128),  # 배치 정규화
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )
        self.lstm = nn.LSTM(256, 128, num_layers=1, batch_first=True, bidirectional=True)  # 양방향 LSTM
        self.classifier = nn.Sequential(
            nn.Linear(128 * 2, 64),  # LSTM 양방향 출력
            nn.ReLU(),
            nn.Linear(64, 2)  # 이진 분류 출력층
        )

    def forward(self, x):
        x = x.permute(0, 2, 1)  # (B, T, F) → (B, F, T)
        x = self.cnn(x)  # CNN 처리
        x = x.permute(0, 2, 1)  # (B, F, T) → (B, T, F)
        lstm_out, _ = self.lstm(x)  # LSTM 처리
        pooled = torch.mean(lstm_out, dim=1)  # 시간축 평균 풀링
        return self.classifier(pooled)  # 최종 분류 결과

# ✅ Threshold 기반 평가 함수 (정확도, FP/FN 포함)
# - softmax 확률 기반 이진 분류 + 혼동행렬 통계

def evaluate(loader, threshold=0.8):
    model.eval()  # 평가 모드
    total_loss, correct, total = 0, 0, 0
    false_positive, false_negative = 0, 0

    with torch.no_grad():  # 그래디언트 계산 비활성화
        for mel, label in loader:
            mel, label = mel.to(device), label.to(device)
            outputs = model(mel)  # 모델 예측
            probs = F.softmax(outputs, dim=1)  # softmax 확률
            pred_probs = probs[:, 1]  # 클래스 1 확률 추출
            preds = (pred_probs >= threshold).long()  # threshold 기준 이진화
            loss = criterion(outputs, label)  # 손실 계산
            total_loss += loss.item()

            for i in range(label.size(0)):
                true = label[i].item()
                pred = preds[i].item()
                if true == 1 and pred == 0:
                    false_positive += 1  # 딥보이스 놓침
                elif true == 0 and pred == 1:
                    false_negative += 1  # 정상 오탐

            correct += (preds == label).sum().item()  # 정확도 누적
            total += label.size(0)

    acc = 100 * correct / total  # 정확도 (%)
    print(f"\n📊 Threshold 평가 결과 (기준 확률 ≥ {threshold}):")
    print(f"✅ 정확도: {acc:.2f}%")
    print(f"🔺 False Positive (딥보이스를 정상으로 판단): {false_positive}개")
    print(f"🔻 False Negative (정상을 딥보이스로 판단): {false_negative}개")
    return total_loss, acc

# ✅ 경로 및 설정값 정의
train_batch_indices = list(range(15))  # 학습용 배치 인덱스 (0~24)
val_batch_indices = list(range(25, 27))  # 검증용 배치 인덱스 (25~28)
label_0_root = "G:\\내 드라이브\\Capstone\\label_0"  # 정상 데이터 경로
label_1_root = "G:\\내 드라이브\\Capstone\\label_1"  # 딥보이스 데이터 경로
EPOCHS = 3  # 에폭 수
BATCH_SIZE = 16  # 배치 크기
MAX_FILES_PER_CLASS = 2000  # 학습용 최대 파일 수
VAL_MAX_FILES_PER_CLASS = 500  # 검증용 최대 파일 수
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 디바이스 설정

# ✅ 검증 데이터셋 고정 구성 (매 epoch 재사용)
val_paths = []
for idx in val_batch_indices:
    normal_batch = os.path.join(label_0_root, f'batch_{idx:03d}')  # 정상 배치 경로
    abnormal_batch = os.path.join(label_1_root, f'batch_{idx:03d}')  # 비정상 배치 경로
    normal_paths = get_npy_paths_from_batch(normal_batch, max_files=VAL_MAX_FILES_PER_CLASS)
    abnormal_paths = get_npy_paths_from_batch(abnormal_batch, max_files=VAL_MAX_FILES_PER_CLASS)
    val_paths.extend([(p, 0) for p in normal_paths])  # 정상 라벨
    val_paths.extend([(p, 1) for p in abnormal_paths])  # 딥보이스 라벨
val_dataset_fixed = ConcatDataset([SubsetNpyDataset([p], label) for p, label in val_paths])  # 검증 데이터셋 구성
val_loader = DataLoader(val_dataset_fixed, batch_size=BATCH_SIZE, shuffle=False)  # 검증 로더

# ✅ 모델 초기화 및 옵티마이저 설정
model = CNNLSTM(input_channels=80).to(device)
criterion = nn.CrossEntropyLoss()  # 손실 함수: 다중 클래스 분류
optimizer = optim.Adam(model.parameters(), lr=0.0005)  # Adam 옵티마이저

# ✅ 학습 루프 시작
for epoch in range(EPOCHS):
    print(f"\n📘 Epoch {epoch+1}/{EPOCHS}")
    start_time = time.time()  # 시간 측정 시작

    # 🔁 학습용 데이터 로딩 (매 epoch마다 새로 샘플링)
    all_paths = []
    for idx in train_batch_indices:
        normal_batch = os.path.join(label_0_root, f'batch_{idx:03d}')
        abnormal_batch = os.path.join(label_1_root, f'batch_{idx:03d}')
        normal_paths = get_npy_paths_from_batch(normal_batch, max_files=MAX_FILES_PER_CLASS)
        abnormal_paths = get_npy_paths_from_batch(abnormal_batch, max_files=MAX_FILES_PER_CLASS)
        all_paths.extend([(p, 0) for p in normal_paths])  # 정상
        all_paths.extend([(p, 1) for p in abnormal_paths])  # 비정상

    full_dataset = ConcatDataset([SubsetNpyDataset([p], label) for p, label in all_paths])  # 학습 데이터셋 구성
    train_loader = DataLoader(full_dataset, batch_size=BATCH_SIZE, shuffle=True)  # 학습용 데이터 로더

    # 🧠 모델 학습
    model.train()
    train_loss, train_correct, total = 0, 0, 0
    for mel, label in tqdm(train_loader, desc=f"Epoch {epoch+1} 진행중", ncols=100, leave=True, dynamic_ncols=True, file=sys.stdout, ascii=True):
        mel, label = mel.to(device), label.to(device)  # GPU 전송
        outputs = model(mel)  # 예측
        loss = criterion(outputs, label)  # 손실 계산
        optimizer.zero_grad()  # 기울기 초기화
        loss.backward()  # 역전파
        optimizer.step()  # 가중치 업데이트
        train_loss += loss.item()  # 손실 누적
        _, pred = torch.max(outputs, 1)  # 예측 결과
        train_correct += (pred == label).sum().item()  # 정확도 누적
        total += label.size(0)  # 전체 수

    # 📈 평가 및 결과 출력
    elapsed = time.time() - start_time  # 시간 측정 종료
    train_acc = 100 * train_correct / total  # 훈련 정확도
    val_loss, val_acc = evaluate(val_loader)  # 검증 수행
    print(f"📊 결과 - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
    print(f"⏱️ Epoch {epoch+1} 학습 시간: {elapsed:.2f}초")

# ✅ 모델 저장
save_path = "G:\\내 드라이브\\Capstone\\modelWithThreshold.pt"
torch.save(model.state_dict(), save_path)  # 모델 파라미터 저장
print(f"✅ 모델 저장 완료: {save_path}")
