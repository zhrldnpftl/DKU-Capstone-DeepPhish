import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Platform } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import HeaderBar from '../components/HeaderBar';
import PhishingStatsCard from '../components/PhishingStatsCard';
import GuidePage from '../components/GuidePage';
import SafetyPage from '../components/SafetyPage';
import Toast from 'react-native-toast-message';

export default function HomePage() {
  const navigation = useNavigation();
  const [showGuideModal, setShowGuideModal] = useState(false);
  const [showSafetyModal, setShowSafetyModal] = useState(false);

  return (
    <View style={styles.container}>
      <ScrollView 
        style={styles.scrollContainer}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={true}
        bounces={true}
        alwaysBounceVertical={Platform.OS === 'ios'}
      >
        {/* HeaderBar */}
        <View style={styles.headerWrapper}>
          <HeaderBar />
        </View>

        <View style={styles.contentWrapper}>
          <Text style={styles.subTitle}>AI 기반 딥보이스 · 보이스 피싱 탐지 시스템</Text>

          {/* 가로 배치된 작은 가이드 섹션 - 크기 축소 */}
          <View style={styles.horizontalGuideContainer}>
            {/* 사용 가이드 (좌측) */}
            <TouchableOpacity 
              style={styles.leftGuideSection} 
              onPress={() => setShowGuideModal(true)}
            >
              <Text style={styles.extraText}>📋 사용 가이드</Text>
              <Text style={styles.previewText}>탭하여 보기</Text>
            </TouchableOpacity>

            {/* 예방 수칙 (우측) */}
            <TouchableOpacity 
              style={styles.rightGuideSection} 
              onPress={() => setShowSafetyModal(true)}
            >
              <Text style={styles.extraText}>🛡️ 예방 수칙</Text>
              <Text style={styles.previewText}>탭하여 보기</Text>
            </TouchableOpacity>
          </View>

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

          <PhishingStatsCard />

          {/* 하단 여백 */}
          <View style={styles.bottomSpacer} />
        </View>
      </ScrollView>

      {/* 모달들 */}
      <GuidePage 
        visible={showGuideModal} 
        onClose={() => setShowGuideModal(false)} 
      />
      <SafetyPage 
        visible={showSafetyModal} 
        onClose={() => setShowSafetyModal(false)} 
      />
    </View>
  );
}

const styles = StyleSheet.create({
  // 최상위 컨테이너
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },

  // 스크롤 컨테이너 - flex 제거
  scrollContainer: {
    backgroundColor: '#fff',
  },
  
  // 스크롤 내용 - flexGrow 제거하고 paddingBottom만 유지
  scrollContent: {
    paddingBottom: 100,
  },
  
  // 콘텐츠 래퍼 - flex 제거하고 자연스러운 높이로
  contentWrapper: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  
  headerWrapper: {
    width: '100%',
    marginBottom: 10,
  },
  
  subTitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 24,
  },
  
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 10,
    marginBottom: 15,
    width: '100%',
    alignItems: 'center',
    // 플랫폼별 그림자 처리
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: {
          width: 0,
          height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 3.84,
      },
      android: {
        elevation: 5,
      },
      web: {
        boxShadow: '0px 2px 3.84px rgba(0, 0, 0, 0.1)',
      },
    }),
  },
  
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },

  // 가로 배치된 작은 가이드 섹션 - 크기 대폭 축소
  horizontalGuideContainer: {
    flexDirection: 'row',
    width: '100%',
    marginBottom: 20,
    gap: 8,
  },

  leftGuideSection: {
    flex: 1,
    padding: 6,
    backgroundColor: '#F0F8FF',
    borderRadius: 6,
    borderLeftWidth: 2,
    borderLeftColor: '#007AFF',
    minHeight: 35,
    justifyContent: 'center',
    alignItems: 'center',
  },

  rightGuideSection: {
    flex: 1,
    padding: 6,
    backgroundColor: '#FFF8E1',
    borderRadius: 6,
    borderLeftWidth: 2,
    borderLeftColor: '#FFA726',
    minHeight: 35,
    justifyContent: 'center',
    alignItems: 'center',
  },

  extraText: {
    fontSize: 10,
    fontWeight: 'bold',
    marginBottom: 2,
    color: '#333',
    textAlign: 'center',
  },

  previewText: {
    fontSize: 8,
    color: '#888',
    textAlign: 'center',
  },

  // 하단 여백
  bottomSpacer: {
    height: 50,
  },
});