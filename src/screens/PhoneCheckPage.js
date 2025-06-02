// src/screens/PhoneCheckPage.js

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import HeaderBar from '../components/HeaderBar';
import Toast from 'react-native-toast-message';

export default function PhoneCheckPage({ route }) {
  const [inputNumber, setInputNumber] = useState(route?.params?.phoneNumber || '');
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    console.log("🟡 입력된 전화번호:", inputNumber);
    try {
      console.log("try문 진입입");
                                    // http://localhost:5000/check-phone
                                    // 이 localhost 부분을 서버의 ip 주소로 넣고 실행해야 앱에서 실행됨
      const response = await fetch('http://192.168.219.104:5000/check-phone', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone_number: inputNumber }),
      });

      const data = await response.json();
      console.log("1. 받아온 데이터 data : ", data);
      console.log("2. response : ", response);
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
      console.error('조회 중 오류 발생:', error);
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
