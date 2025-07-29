# voicephishing_KoBERT_predictor.py

import torch
from torch import nn
from transformers import BertTokenizer
from kobert_transformers import get_tokenizer, get_kobert_model

# 기준 threshold
DEFAULT_THRESHOLD = 0.80
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 모델 구조 정의
class KoBERTClassifier(nn.Module):
    def __init__(self, bert_model, hidden_size=768, num_classes=2, dr_rate=0.3):
        super(KoBERTClassifier, self).__init__()
        self.bert = bert_model
        self.dropout = nn.Dropout(p=dr_rate)
        self.classifier = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs = self.bert(input_ids=input_ids,
                            attention_mask=attention_mask,
                            token_type_ids=token_type_ids)
        cls_output = self.dropout(outputs.pooler_output)
        logits = self.classifier(cls_output)
        return self.softmax(logits)

# 토크나이저 및 모델 로딩
tokenizer = get_tokenizer()
kobert_model = get_kobert_model()
model = KoBERTClassifier(kobert_model).to(device)
model.load_state_dict(torch.load("voicephishing_model_threshold_080.pt", map_location=device))
model.eval()

# 예측 함수
def predict_phishing(texts, threshold=DEFAULT_THRESHOLD, max_len=128):
    if isinstance(texts, str):
        texts = [texts]  # 문자열 하나 입력된 경우도 처리
    pred_labels, confidences = [], []

    with torch.no_grad():
        for text in texts:
            encoded = tokenizer(
                text, padding='max_length', truncation=True,
                max_length=max_len, return_tensors='pt'
            )
            input_ids = encoded['input_ids'].to(device)
            attention_mask = encoded['attention_mask'].to(device)
            token_type_ids = encoded['token_type_ids'].to(device)

            output = model(input_ids, attention_mask, token_type_ids)
            phishing_score = output[0][1].item()
            label = 1 if phishing_score >= threshold else 0

            pred_labels.append(label)
            confidences.append(phishing_score)

    return pred_labels, confidences
