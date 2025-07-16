// src/components/HeaderBar.js

import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';

export default function HeaderBar() {
  const navigation = useNavigation();

  return (
    <View style={styles.wrapper}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('HomePage')}>
          <Text style={styles.logo}>🛡️ DeepPhish</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.separatorSpacing} />
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    paddingTop: 40, // ⬅️ 상단 여백 추가
    paddingBottom: 24, // ⬅️ 하단 여백 증가
    paddingHorizontal: 24,
    backgroundColor: '#fff',
    borderBottomWidth: 2, // ⬅️ 구분선 추가
    borderBottomColor: '#eee',
    alignItems: 'center',
  },
  separatorSpacing: {
    height: 20, // ✅ 구분선 아래 여백 공간 분리
  },
  logo: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1E90FF',
  },
});
