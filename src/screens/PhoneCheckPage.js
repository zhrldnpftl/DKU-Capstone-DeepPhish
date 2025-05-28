// src/screens/PhoneCheckPage.js

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import HeaderBar from '../components/HeaderBar';

export default function PhoneCheckPage({ route }) {
  const [inputNumber, setInputNumber] = useState(route?.params?.phoneNumber || '');
  const [result, setResult] = useState(null);

  const handleSearch = () => {
    // ✅ 실제로는 백엔드 API 또는 크롤링 결과 연동
    // 임시 결과 시뮬레이션
    setResult({
      reportCount: 3,
      pattern: '사칭형 피싱',
      risk: '⚠️ 위험 등급: 높음',
    });
  };

  return (
    <View style={styles.container}>
      <HeaderBar />

      <Text style={styles.title}>📞 전화번호 조회</Text>

      <TextInput
        placeholder="조회할 전화번호 입력"
        keyboardType="phone-pad"
        value={inputNumber}
        onChangeText={setInputNumber}
        style={styles.input}
      />

      <TouchableOpacity style={styles.button} onPress={handleSearch}>
        <Text style={styles.buttonText}>🔍 조회하기</Text>
      </TouchableOpacity>

      {result && (
        <View style={styles.resultBox}>
          <Text style={styles.resultItem}>🚨 신고 건수: {result.reportCount}건</Text>
          <Text style={styles.resultItem}>📌 신고 유형: {result.pattern}</Text>
          <Text style={styles.resultRisk}>{result.risk}</Text>
        </View>
      )}
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
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 24,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  button: {
    backgroundColor: '#1E90FF',
    padding: 14,
    borderRadius: 10,
    marginBottom: 20,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: '600',
  },
  resultBox: {
    backgroundColor: '#f9f9f9',
    padding: 20,
    borderRadius: 10,
  },
  resultItem: {
    fontSize: 16,
    marginBottom: 10,
  },
  resultRisk: {
    fontSize: 17,
    fontWeight: 'bold',
    color: '#d9534f',
  },
});
