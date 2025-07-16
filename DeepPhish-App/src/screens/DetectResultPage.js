import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import HeaderBar from '../components/HeaderBar';

export default function DetectResultPage() {
  const navigation = useNavigation();
  const route = useRoute();

  // ✅ 전달받은 파라미터
  const { result, phoneNumber = '010-****-1234', fileName = '업로드_음성파일.mp3' } = route.params || {};


  // ✅ 수정된 구조에 맞게 변수 추출
  const deep = result?.deepvoice_result || {};
  const phish = result?.phishing_result || {};
  const report = result?.phone_check?.report || { voice: 0, sms: 0 };
  const final = result?.final_result || {};

  // ✅ 확률 계산 안전하게 처리
  const deepProb = typeof deep.probability === 'number' ? Math.round(deep.probability * 100) : '??';
  const phishProb = typeof phish.probability === 'number' ? Math.round(phish.probability * 100) : '??';

  // ✅ 사용자에게 보여줄 문장 구성
  const deepvoiceResult = `🎤 딥보이스 탐지: ${deep.label === 'fake' ? '합성 음성' : '일반 음성'} (${deepProb}%)`;
  const phishingResult = `🧠 문맥 분석: ${phish.label === 'phishing' ? '피싱 의심' : '정상 통화'} (${phishProb}%)`;
  const reportResult = `📞 해당 번호 신고 내역\nㆍ음성 신고: ${report.voice}건\nㆍ문자 신고: ${report.sms}건`;

  const finalJudgement = final.is_phishing
    ? `⚠️ [주의] 보이스 피싱으로 의심됩니다\n📝 사유: ${final.reason}`
    : `✅ [정상] 안전한 통화로 판단됩니다\n📝 사유: ${final.reason}`;

  return (
    <View style={styles.container}>
      <HeaderBar />
      <Text style={styles.title}>🔍 탐지 결과</Text>

      {/* 🔹 분석 결과 요약 */}
      <View style={styles.resultBox}>
        <Text style={styles.resultItem}>{deepvoiceResult}</Text>
        <Text style={styles.resultItem}>{phishingResult}</Text>
        <Text style={styles.resultItem}>{reportResult}</Text>
        <Text style={[styles.resultItem, styles.finalResult]}>{finalJudgement}</Text>
      </View>

      {/* 🔹 후속 동작 버튼 */}
      <View style={styles.buttonGroup}>
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate('PhoneCheckPage', { phoneNumber })}
        >
          <Text style={styles.buttonText}>📞 이 번호 다시 조회하기</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.button}
          onPress={() =>
            navigation.navigate('ReportPage', {
              phoneNumber,
              fileName,
              result: final.is_phishing ? '보이스 피싱 의심됨' : '정상 통화',
            })
          }
        >
          <Text style={styles.buttonText}>🚨 신고 페이지로 이동</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// 💅 스타일 정의
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingTop: 40,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#1E90FF',
  },
  resultBox: {
    backgroundColor: '#f0f8ff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 30,
    elevation: 2,
  },
  resultItem: {
    fontSize: 15,
    marginBottom: 10,
    color: '#333',
  },
  finalResult: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#d9534f',
    marginTop: 10,
  },
  buttonGroup: {
    gap: 15,
  },
  button: {
    backgroundColor: '#1E90FF',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 15,
  },
});
