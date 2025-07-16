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

  const handleFilePick = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({ type: '*/*' });
      if (result.canceled || result.type === 'cancel') return;

      const asset = result.assets?.[0] || result;
      const name = asset.name || '';
      const ext = name.split('.').pop().toLowerCase();

      if (!['mp3', 'mp4'].includes(ext)) {
        Toast.show({
          type: 'error',
          text1: '잘못된 파일 형식',
          text2: 'mp3 또는 mp4 파일만 선택할 수 있어요.',
        });
        setSelectedFile(null);
        return;
      }

      const fileData = {
        name,
        uri: asset.uri,
        mimeType: asset.mimeType || `audio/${ext}`,
        size: asset.size || null
        // file 속성 제거
      };

      setSelectedFile(fileData);
    } catch (error) {
      console.error('📛 파일 선택 중 오류:', error);
    }
  };
  const handleDetect = () => {
    if (!phoneNumber.trim() && !selectedFile) {
      Toast.show({
        type: 'error',
        text1: '입력 정보가 부족합니다',
        text2: '☎️ 전화번호와 🎧 음성 파일을 모두 입력해주세요.',
      });
      return;
    }

    if (!phoneNumber.trim()) {
      Toast.show({
        type: 'error',
        text1: '전화번호가 입력되지 않았어요',
        text2: '☎️ 전화번호를 먼저 입력해주세요.',
      });
      return;
    }

    if (!selectedFile) {
      Toast.show({
        type: 'error',
        text1: '파일이 선택되지 않았어요',
        text2: '🎧 음성 파일을 먼저 업로드해주세요.',
      });
      return;
    }

    navigation.navigate('DetectLoadingPage', {
      phoneNumber,
      selectedFile // ✅ 전체 객체 전달
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
        <Text style={styles.filename}>선택된 파일: {`${selectedFile.name}`}</Text>
      )}

      <View style={styles.detectButton}>
        <Button title="탐지 시작" onPress={handleDetect} color="#1E90FF" />
      </View>

      <Toast />
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
