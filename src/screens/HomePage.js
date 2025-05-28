// frontend/src/screens/HomePage.js

import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import HeaderBar from '../components/HeaderBar';


export default function HomePage() {
  const navigation = useNavigation();

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <HeaderBar />
      
      <Text style={styles.subTitle}>AI 기반 딥보이스 · 보이스 피싱 탐지 시스템</Text>

      {/* 🔘 주요 기능 진입 버튼 */}
      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate('DetectPage')}
      >
        <Text style={styles.buttonText}>🔍 보이스 피싱 탐지 시작하기</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate('PhoneCheckPage')}
      >
        <Text style={styles.buttonText}>📞 전화번호 조회</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate('ReportPage')}
      >
        <Text style={styles.buttonText}>🚨 보이스 피싱 신고하기</Text>
      </TouchableOpacity>

      {/* 📊 최근 보이스피싱 사례 카드 */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>📊 최근 보이스 피싱 사례</Text>
        <Text style={styles.cardItem}>• 💳 금융기관 사칭 증가 (23%)</Text>
        <Text style={styles.cardItem}>• 📱 최근 가장 많이 신고된 번호: 010-****-1234</Text>
        <Text style={styles.cardItem}>• 🧠 딥보이스 탐지율 향상: 91%</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#fff',
    flexGrow: 1,
    justifyContent: 'flex-start',
    alignItems: 'center'
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1E90FF',
    marginBottom: 8,
    textAlign: 'center',
  },
  subTitle: {
    fontSize: 14,
    color: '#555',
    marginBottom: 30,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#1E90FF',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
    width: '100%',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center'
  },
  card: {
    marginTop: 30,
    padding: 20,
    backgroundColor: '#F8F8F8',
    borderRadius: 10,
    width: '100%',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10
  },
  cardItem: {
    fontSize: 14,
    marginVertical: 2
  }
});
