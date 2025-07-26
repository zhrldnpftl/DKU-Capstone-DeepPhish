import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader, ConcatDataset, random_split
#from google.colab import drive

# ✅ Google Drive 마운트
#drive.mount('/content/drive')

# ✅ .npy 파일 경로 수집 함수 (최대 개수 제한)
def get_npy_paths_from_batch(batch_path, max_files=5000):
    if not os.path.exists(batch_path):
        return []
    files = [os.path.join(batch_path, f) for f in os.listdir(batch_path) if f.endswith('.npy')]
    return files[:max_files]

# ✅ 정규화 포함 Dataset 클래스
class SubsetNpyDataset(Dataset):
    def __init__(self, file_paths, label):
        self.file_paths = file_paths
        self.label = label  # 0: 정상, 1: 딥보이스

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        try:
            npy_array = np.load(self.file_paths[idx])  # (80, 300)
            npy_array = npy_array.T                    # (300, 80)
            npy_array = np.clip(npy_array, -80, 30)
            npy_array = (npy_array + 80) / 110         # → [0, 1] 정규화
            tensor = torch.tensor(npy_array, dtype=torch.float32)
            return tensor, self.label
        except Exception as e:
            print(f"⚠️ {self.file_paths[idx]} 불러오기 실패 - {e}")
            return self.__getitem__((idx + 1) % len(self))  # 오류 시 다음 샘플로 우회

# ✅ 모델 정의
class CNNLSTM(nn.Module):
    def __init__(self, input_channels):
        super(CNNLSTM, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv1d(input_channels, 128, kernel_size=5, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )
        self.lstm = nn.LSTM(256, 128, num_layers=1, batch_first=True, bidirectional=True)
        self.classifier = nn.Sequential(
            nn.Linear(128 * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.cnn(x)
        x = x.permute(0, 2, 1)
        lstm_out, _ = self.lstm(x)
        pooled = torch.mean(lstm_out, dim=1)
        return self.classifier(pooled)

# ✅ 설정값
batch_indices = list(range(6))  # batch_000 ~ batch_005 사용
label_0_root = 'G:\내 드라이브\Capstone\label_0'
label_1_root = 'G:\내 드라이브\Capstone\label_1'

EPOCHS = 3  # 전체 배치 반복 횟수
BATCH_SIZE = 16
MAX_FILES_PER_CLASS = 2000
VAL_SPLIT = 0.2  # 검증용 비율

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ✅ 전체 배치 데이터 수집
all_paths = []
for idx in batch_indices:
    normal_batch = os.path.join(label_0_root, f'batch_{idx:03d}')
    abnormal_batch = os.path.join(label_1_root, f'batch_{idx:03d}')

    normal_paths = get_npy_paths_from_batch(normal_batch, max_files=MAX_FILES_PER_CLASS)
    abnormal_paths = get_npy_paths_from_batch(abnormal_batch, max_files=MAX_FILES_PER_CLASS)

    all_paths.extend([(p, 0) for p in normal_paths])
    all_paths.extend([(p, 1) for p in abnormal_paths])

# ✅ 데이터셋 생성 및 분할
full_dataset = ConcatDataset([
    SubsetNpyDataset([p], label) for p, label in all_paths
])
val_size = int(len(full_dataset) * VAL_SPLIT)
train_size = len(full_dataset) - val_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# ✅ EPOCHS 횟수만큼 전체 배치 반복 학습
model = CNNLSTM(input_channels=80).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)

for epoch in range(EPOCHS):
    model.train()
    train_loss, train_correct, total = 0, 0, 0

    for mel, label in train_loader:
        mel, label = mel.to(device), label.to(device)
        outputs = model(mel)
        loss = criterion(outputs, label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        _, pred = torch.max(outputs, 1)
        train_correct += (pred == label).sum().item()
        total += label.size(0)

    train_acc = 100 * train_correct / total

    # ✅ 검증 평가
    model.eval()
    val_loss, val_correct, val_total = 0, 0, 0
    with torch.no_grad():
        for mel, label in val_loader:
            mel, label = mel.to(device), label.to(device)
            outputs = model(mel)
            loss = criterion(outputs, label)
            val_loss += loss.item()
            _, pred = torch.max(outputs, 1)
            val_correct += (pred == label).sum().item()
            val_total += label.size(0)

    val_acc = 100 * val_correct / val_total

    print(f"[Epoch {epoch+1}/{EPOCHS}] \n"
          f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%\n"
          f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")

# ✅ 모델 저장
save_path = 'G:/내 드라이브/Capstone/model_combined_with_val.pt'
torch.save(model.state_dict(), save_path)
print(f"✅ 모델 저장 완료: {save_path}")
