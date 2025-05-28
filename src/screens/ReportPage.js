// frontend/src/screens/ReportPage.js

import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import HeaderBar from '../components/HeaderBar';

export default function ReportPage({ route }) {
  const { phoneNumber = '010-****-1234', fileName = '피싱_의심_음성.mp3', result = '보이스 피싱 의심됨' } = route?.params || {};
  const [reportTime] = useState(new Date().toLocaleString());

  const handleReport = () => {
    // ✅ 추후 MongoDB에 신고 내역 저장도 가능
    Linking.openURL('https://www.counterscam112.go.kr/report/reportTerms.do;jsessionid=xlQMemiXsKGnXdIUUnJEexafqrHkqgq6VIUtWFQR.AP_homepage11?type=vop');
  };

  return (
    <View style={styles.container}>
      <HeaderBar />

      <Text style={styles.title}>🚨 보이스 피싱 신고</Text>

      <View style={styles.infoBox}>
        <Text style={styles.label}>📁 파일명:</Text>
        <Text style={styles.text}>{fileName}</Text>

        <Text style={styles.label}>⏰ 탐지 시간:</Text>
        <Text style={styles.text}>{reportTime}</Text>

        <Text style={styles.label}>🧠 탐지 결과:</Text>
        <Text style={styles.text}>{result}</Text>

        <Text style={styles.label}>📞 신고할 번호:</Text>
        <Text style={styles.text}>{phoneNumber}</Text>
      </View>

      <TouchableOpacity style={styles.button} onPress={handleReport}>
        <Text style={styles.buttonText}>📤 신고하기 (CounterScam112)</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingHorizontal: 24,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 24,
    textAlign: 'center',
  },
  infoBox: {
    backgroundColor: '#fdf6f6',
    padding: 20,
    borderRadius: 10,
    marginBottom: 30,
  },
  label: {
    fontWeight: '600',
    marginTop: 12,
    fontSize: 15,
  },
  text: {
    fontSize: 15,
    marginTop: 4,
    color: '#444',
  },
  button: {
    backgroundColor: '#d9534f',
    padding: 14,
    borderRadius: 10,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 15,
    fontWeight: 'bold',
  },
});
