import React, { useEffect, useState, useRef } from 'react';
import { View, Text, ActivityIndicator, StyleSheet, ScrollView } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

// 📡 서버 URL
const getServerUrl = () => {
  return 'http://192.168.219.104:5000';  // Wi-Fi IP에 맞게 조정
};
const SERVER_URL = getServerUrl();

export default function DetectLoadingPage() {
  const navigation = useNavigation();
  const route = useRoute();

  const { phoneNumber, selectedFile } = route.params || {};
  const [logMessages, setLogMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(true);
  const isProcessingRef = useRef(false);

  const addLog = (msg) => {
    setLogMessages((prev) => [...prev, msg]);
    console.log(msg);
  };

  useEffect(() => {
    if (isProcessingRef.current) return;
    isProcessingRef.current = true;

    const detectStream = async () => {
      try {
        if (!selectedFile || !phoneNumber) {
          addLog('❌ 필수 정보 누락');
          return;
        }

        addLog('📤 파일 업로드 중...');

        const uriParts = selectedFile.uri.split('.');
        const fileType = uriParts[uriParts.length - 1];
        const mimeType = fileType === 'mp3' ? 'audio/mpeg' : `audio/${fileType}`;
        const fileName = selectedFile.name || `audio.${fileType}`;

        const formData = new FormData();
        formData.append('phone_number', phoneNumber);
        formData.append('audio', {
          uri: selectedFile.uri,
          name: fileName,
          type: mimeType
        });

        const uploadRes = await fetch(`${SERVER_URL}/upload-audio`, {
          method: 'POST',
          body: formData,
        });

        const uploadData = await uploadRes.json();
        const fileId = uploadData.file_id;
        addLog(`✅ 업로드 완료: ${fileId}`);

        pollForResult(fileId);
      } catch (err) {
        addLog(`❌ 업로드 실패: ${err.message}`);
        setIsProcessing(false);
      }
    };
    detectStream();
  }, []);

  const pollForResult = async (fileId) => {
    let attempts = 0;
    const maxAttempts = 150;
    let displayedLogs = new Set();

    const poll = async () => {
      try {
        attempts++;
        const res = await fetch(`${SERVER_URL}/detect-stream/${fileId}?phone_number=${phoneNumber}`);
        
        if (!res.ok) {
          const errorData = await res.json();
          addLog(`❌ 서버 오류: ${errorData.error || '알 수 없는 오류'}`);
          setIsProcessing(false);
          return;
        }

        const data = await res.json();

        if (data.done) {
          addLog('✅ 분석 완료! 결과 페이지로 이동');
          setIsProcessing(false);
          navigation.replace('DetectResultPage', {
            result: data,
            phoneNumber,
            fileName: selectedFile?.name || '업로드_음성파일.mp3',  // ✅ 이 줄을 추가!
          });
          return;
        }

        if (data.error) {
          addLog(`❌ 탐지 오류: ${data.error}`);
          setIsProcessing(false);
          return;
        }

        if (data.all_logs && Array.isArray(data.all_logs)) {
          data.all_logs.forEach(logMsg => {
            if (!displayedLogs.has(logMsg)) {
              displayedLogs.add(logMsg);
              addLog(logMsg);
            }
          });
        }

        if (attempts < maxAttempts) {
          setTimeout(poll, 2000);
        } else {
          addLog('❌ 최대 재시도 횟수 초과');
          setIsProcessing(false);
        }

      } catch (err) {
        addLog(`❌ 폴링 오류: ${err.message}`);
        if (attempts < maxAttempts) {
          setTimeout(poll, 3000);
        } else {
          setIsProcessing(false);
        }
      }
    };

    poll();
  };

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#1E90FF" />
      <Text style={styles.text}>
        {isProcessing ? 'AI가 음성을 분석 중입니다...' : '처리 완료'}
      </Text>

      <ScrollView style={styles.logContainer} showsVerticalScrollIndicator={false}>
        {logMessages.map((log, i) => (
          <Text key={i} style={styles.logText}>
            {log}
          </Text>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    justifyContent: 'center', 
    alignItems: 'center', 
    padding: 20,
    backgroundColor: '#f8f9fa'
  },
  text: { 
    marginVertical: 20, 
    fontSize: 16, 
    color: '#333',
    fontWeight: '600'
  },
  logContainer: { 
    width: '100%', 
    maxHeight: 400, 
    paddingHorizontal: 10,
    backgroundColor: '#fff',
    borderRadius: 8,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  logText: { 
    fontSize: 13, 
    color: '#444', 
    marginBottom: 8, 
    fontFamily: 'monospace',
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#1E90FF',
    backgroundColor: '#f8f9fa',
    marginHorizontal: 5,
    borderRadius: 4
  },
});
