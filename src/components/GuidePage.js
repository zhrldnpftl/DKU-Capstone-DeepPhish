import React from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  StyleSheet, 
  Modal, 
  ScrollView,
  Dimensions 
} from 'react-native';

const { width, height } = Dimensions.get('window');

export default function GuidePage({ visible, onClose }) {
  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <View style={styles.modalContainer}>
          {/* 헤더 */}
          <View style={styles.header}>
            <Text style={styles.title}>📋 사용 가이드</Text>
            <TouchableOpacity style={styles.closeButton} onPress={onClose}>
              <Text style={styles.closeButtonText}>✕</Text>
            </TouchableOpacity>
          </View>

          {/* 내용 */}
          <ScrollView 
            style={styles.content}
            showsVerticalScrollIndicator={true}
          >
            <View style={styles.guideItem}>
              <Text style={styles.guideTitle}>🎙️ 의심스러운 전화 녹음</Text>
              <Text style={styles.guideDescription}>
                의심스러운 전화를 받으면 즉시 녹음을 시작하세요. 
                앱의 '보이스 피싱 탐지 시작하기' 버튼을 눌러 녹음을 시작할 수 있습니다.
              </Text>
            </View>

            <View style={styles.guideItem}>
              <Text style={styles.guideTitle}>🤖 AI 실시간 분석</Text>
              <Text style={styles.guideDescription}>
                AI가 실시간으로 보이스 피싱 패턴을 분석합니다. 
                통화 중에 의심스러운 패턴이 감지되면 즉시 알림을 받을 수 있습니다.
              </Text>
            </View>

            <View style={styles.guideItem}>
              <Text style={styles.guideTitle}>📞 전화번호 사전 조회</Text>
              <Text style={styles.guideDescription}>
                전화번호 조회 기능을 사용하여 사전에 위험한 번호인지 확인하세요. 
                데이터베이스에 등록된 피싱 번호라면 경고 메시지를 표시합니다.
              </Text>
            </View>

            <View style={styles.guideItem}>
              <Text style={styles.guideTitle}>📊 통계 및 동향 파악</Text>
              <Text style={styles.guideDescription}>
                정기적으로 최신 보이스 피싱 통계를 확인하여 동향을 파악하세요. 
                홈 화면 하단의 통계 카드에서 최신 정보를 확인할 수 있습니다.
              </Text>
            </View>

            <View style={styles.tipContainer}>
              <Text style={styles.tipTitle}>💡 추가 팁</Text>
              <Text style={styles.tipText}>
                • 녹음 시 조용한 환경에서 진행하세요{'\n'}
                • 통화 내용을 정확히 전달하기 위해 명확하게 말하세요{'\n'}
                • 의심스러운 통화는 즉시 끊고 관련 기관에 신고하세요
              </Text>
            </View>
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    width: width * 0.9,
    maxHeight: height * 0.8,
    backgroundColor: '#fff',
    borderRadius: 15,
    overflow: 'hidden',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#F0F8FF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  closeButton: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#E0E0E0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 16,
    color: '#666',
    fontWeight: 'bold',
  },
  content: {
    padding: 20,
  },
  guideItem: {
    marginBottom: 20,
    paddingBottom: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  guideTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  guideDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  tipContainer: {
    backgroundColor: '#F8F9FA',
    padding: 15,
    borderRadius: 10,
    marginTop: 10,
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  tipText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
});