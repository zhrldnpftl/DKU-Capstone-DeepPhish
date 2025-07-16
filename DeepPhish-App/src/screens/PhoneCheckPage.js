// src/screens/PhoneCheckPage.js

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import HeaderBar from '../components/HeaderBar';
import Toast from 'react-native-toast-message';

// ✅ 서버 주소 함수
const getServerUrl = () => {
  return 'http://192.168.219.104:5000'; // ✅ 현재 PC의 IP로 고정
};


export default function PhoneCheckPage({ route }) {
  const [inputNumber, setInputNumber] = useState(route?.params?.phoneNumber || '');
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    console.log("🟡 입력된 전화번호:", inputNumber);
    try {
      console.log("🔍 서버에 조회 요청 중...");

      const response = await fetch(`${getServerUrl()}/check-phone`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone_number: inputNumber }),
      });

      const data = await response.json();
      console.log("📦 받아온 데이터:", data);

      if (response.ok) {
        setResult({
          reportCount: data.reportCount,
          pattern: data.pattern,
          risk: data.risk,
        });

        Toast.show({
          type: 'success',
          text1: '✅ 조회 성공!',
          text2: `${data.reportCount}건의 신고 이력이 있어요.`,
        });
      } else {
        Toast.show({
          type: 'error',
          text1: '🚨 조회 실패',
          text2: data.error || '서버 오류가 발생했어요.',
        });
      }
    } catch (error) {
      console.error('❌ 서버 연결 오류:', error);
      Toast.show({
        type: 'error',
        text1: '❌ 서버 연결 실패',
        text2: '서버에 연결할 수 없습니다.',
      });
    }
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

// 💅 스타일 정의
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
