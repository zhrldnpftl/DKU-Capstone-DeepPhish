// frontend/src/screens/DetectResultPage.js

import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import HeaderBar from '../components/HeaderBar';

export default function DetectResultPage() {
  const navigation = useNavigation();
  const route = useRoute();
  const { phoneNumber = '010-****-1234' } = route.params || {}; // 샘플 데이터

  // 예시 결과값 (향후 실제 탐지 결과 연결 예정)
  const deepvoiceResult = '딥보이스 음성입니다 (확률 88%)';
  const phishingContext = '사칭형 보이스 피싱 의심';
  const reportHistory = '해당 번호: 3건 신고';
  const finalJudgement = '⚠️ 보이스 피싱으로 의심됩니다';

  return (
    <View style={styles.container}>
      <HeaderBar />

      <Text style={styles.title}>🔍 탐지 결과</Text>

      <View style={styles.resultBox}>
        <Text style={styles.resultItem}>🎤 {deepvoiceResult}</Text>
        <Text style={styles.resultItem}>🧠 {phishingContext}</Text>
        <Text style={styles.resultItem}>📞 {reportHistory}</Text>
        <Text style={[styles.resultItem, styles.final]}>{finalJudgement}</Text>
      </View>

      <View style={styles.buttonGroup}>
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate('PhoneCheckPage', { phoneNumber })}
        >
          <Text style={styles.buttonText}>📞 이 번호 다시 조회하기</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate('ReportPage', { phoneNumber })}
        >
          <Text style={styles.buttonText}>🚨 신고 페이지로 이동</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 24,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 20,
    textAlign: 'center',
  },
  resultBox: {
    backgroundColor: '#f0f8ff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 30,
  },
  resultItem: {
    fontSize: 16,
    marginBottom: 10,
  },
  final: {
    fontWeight: 'bold',
    color: '#d9534f',
    fontSize: 17,
  },
  buttonGroup: {
    gap: 16,
  },
  button: {
    backgroundColor: '#1E90FF',
    padding: 14,
    borderRadius: 10,
    marginBottom: 12,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 15,
    fontWeight: '600',
  },
});
