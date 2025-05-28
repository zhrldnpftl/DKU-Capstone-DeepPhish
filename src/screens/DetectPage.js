// src/screens/DetectPage.js
// ✅ 모듈 설치 필요 : npx expo install expo-document-picker
// ✅ 모듈 설치 필요 : npm install react-native-toast-message

import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { useNavigation } from '@react-navigation/native';
import Toast from 'react-native-toast-message';
import HeaderBar from '../components/HeaderBar';

export default function DetectPage() {
  const navigation = useNavigation();
  const [phoneNumber, setPhoneNumber] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  // 📂 파일 선택
  const handleFilePick = async () => {
    try {
      console.log("📂 handleFilePick 시작");

      const result = await DocumentPicker.getDocumentAsync({
        type: '*/*',
      });

      console.log("📂 result:", result);

      if (result.canceled || result.type === 'cancel') return;

      // Web에서는 result.assets[0], Native에선 result.name
      const asset = result.assets?.[0] || result;
      const name = asset.name || '';
      const ext = name.split('.').pop().toLowerCase();

      console.log("📁 선택한 파일명:", name);
      console.log("📄 확장자:", ext);

      if (!['mp3', 'mp4'].includes(ext)) {
        Toast.show({
          type: 'error',
          text1: '잘못된 파일 형식',
          text2: 'mp3 또는 mp4 파일만 선택할 수 있어요.',
        });
        setSelectedFile(null);
        return;
      }

      setSelectedFile({ ...asset, name }); // name을 보장해서 저장

    } catch (error) {
      console.error('📛 파일 선택 중 오류:', error);
    }
  };


  // 🔍 탐지 시작
  const handleDetect = () => {
    const noPhone = !phoneNumber.trim();
    const noFile = !selectedFile;

    if (noPhone && noFile) {
      Toast.show({
        type: 'error',
        text1: '입력 정보가 부족합니다',
        text2: '☎️ 전화번호와 🎧 음성 파일을 모두 입력해주세요.',
      });
      return;
    }

    if (noPhone) {
      Toast.show({
        type: 'error',
        text1: '전화번호가 입력되지 않았어요',
        text2: '☎️ 전화번호를 먼저 입력해주세요.',
      });
      return;
    }

    if (noFile) {
      Toast.show({
        type: 'error',
        text1: '파일이 선택되지 않았어요',
        text2: '🎧 음성 파일을 먼저 업로드해주세요.',
      });
      return;
    }

    // 둘 다 입력된 경우 → 탐지 진행
    navigation.navigate('DetectLoadingPage', {
      phoneNumber,
      file: selectedFile,
    });
  };


  return (
      <View style={styles.container}>
        <HeaderBar />
        <Text style={styles.title}>📞 보이스 피싱 탐지</Text>

        <TextInput
          placeholder="발신번호 입력"
          value={phoneNumber}
          onChangeText={setPhoneNumber}
          keyboardType="phone-pad"
          style={styles.input}
        />

        <Button title="음성 파일 선택" onPress={handleFilePick} />

        {!!selectedFile?.name && (
          <Text style={styles.filename}>
            선택된 파일: {`${selectedFile.name}`}
          </Text>
        )}

        <View style={styles.detectButton}>
          <Button title="탐지 시작" onPress={handleDetect} color="#1E90FF" />
        </View>

        <Toast /> {/* 알림 컴포넌트 등록 */}
      </View>
    );
  }

const styles = StyleSheet.create({
  container: {
    padding: 24,
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'flex-start',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    marginBottom: 20,
  },
  filename: {
    marginTop: 10,
    fontStyle: 'italic',
    color: '#444',
  },
  detectButton: {
    marginTop: 30,
  },
});