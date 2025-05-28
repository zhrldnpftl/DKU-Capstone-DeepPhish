// src/screens/DetectLoadingPage.js

import React, { useEffect } from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';

export default function DetectLoadingPage() {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#1E90FF" />
      <Text style={styles.text}>AI가 음성을 분석 중입니다...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 20,
  },
  text: {
    marginTop: 20,
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
});
