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

export default function SafetyPage({ visible, onClose }) {
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
            <Text style={styles.title}>🛡️ 보이스 피싱 예방 수칙</Text>
            <TouchableOpacity style={styles.closeButton} onPress={onClose}>
              <Text style={styles.closeButtonText}>✕</Text>
            </TouchableOpacity>
          </View>

          {/* 내용 */}
          <ScrollView 
            style={styles.content}
            showsVerticalScrollIndicator={true}
          >
            <View style={styles.ruleItem}>
              <Text style={styles.ruleNumber}>1</Text>
              <View style={styles.ruleContent}>
                <Text style={styles.ruleTitle}>🔒 개인정보 보호</Text>
                <Text style={styles.ruleDescription}>
                  개인정보를 절대 전화로 말하지 마세요. 
                  주민등록번호, 계좌번호, 비밀번호 등은 전화로 요구하지 않습니다.
                </Text>
              </View>
            </View>

            <View style={styles.ruleItem}>
              <Text style={styles.ruleNumber}>2</Text>
              <View style={styles.ruleContent}>
                <Text style={styles.ruleTitle}>🏦 금융기관 원칙</Text>
                <Text style={styles.ruleDescription}>
                  금융기관에서 먼저 전화하지 않습니다. 
                  은행, 카드사, 보험사 등에서 개인정보를 요구하는 전화는 의심하세요.
                </Text>
              </View>
            </View>

            <View style={styles.ruleItem}>
              <Text style={styles.ruleNumber}>3</Text>
              <View style={styles.ruleContent}>
                <Text style={styles.ruleTitle}>⏰ 급박함 의심</Text>
                <Text style={styles.ruleDescription}>
                  급하다고 재촉하면 의심하세요. 
                  "지금 당장", "빨리" 등의 표현으로 압박하는 것은 피싱의 특징입니다.
                </Text>
              </View>
            </View>

            <View style={styles.ruleItem}>
              <Text style={styles.ruleNumber}>4</Text>
              <View style={styles.ruleContent}>
                <Text style={styles.ruleTitle}>✅ 직접 확인</Text>
                <Text style={styles.ruleDescription}>
                  의심스러우면 직접 기관에 확인하세요. 
                  전화를 끊고 해당 기관의 공식 번호로 직접 연락하여 확인하세요.
                </Text>
              </View>
            </View>

            <View style={styles.ruleItem}>
              <Text style={styles.ruleNumber}>5</Text>
              <View style={styles.ruleContent}>
                <Text style={styles.ruleTitle}>👨‍👩‍👧‍👦 가족 암호</Text>
                <Text style={styles.ruleDescription}>
                  가족과 미리 암호를 정해두세요. 
                  가족을 사칭하는 전화에 대비하여 미리 약속된 암호를 사용하세요.
                </Text>
              </View>
            </View>

            <View style={styles.warningContainer}>
              <Text style={styles.warningTitle}>⚠️ 즉시 신고하세요</Text>
              <Text style={styles.warningText}>
                의심스러운 전화를 받았다면:{'\n'}
                • 경찰서: 112{'\n'}
                • 금융감독원: 1332{'\n'}
                • 인터넷 사기신고센터: 1381{'\n'}
                • 스마트폰 앱: 후후, 화이트콜 등 활용
              </Text>
            </View>

            <View style={styles.tipContainer}>
              <Text style={styles.tipTitle}>💡 기억하세요</Text>
              <Text style={styles.tipText}>
                보이스 피싱은 계속 진화하고 있습니다. 
                새로운 수법이 계속 나오므로 항상 경계하고, 
                의심스러운 전화는 즉시 끊는 것이 가장 안전합니다.
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
    backgroundColor: '#FFF8E1',
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
  ruleItem: {
    flexDirection: 'row',
    marginBottom: 20,
    paddingBottom: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  ruleNumber: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#FFA726',
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    textAlignVertical: 'center',
    marginRight: 15,
    marginTop: 5,
  },
  ruleContent: {
    flex: 1,
  },
  ruleTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  ruleDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  warningContainer: {
    backgroundColor: '#FFEBEE',
    padding: 15,
    borderRadius: 10,
    marginTop: 10,
    marginBottom: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
  },
  warningTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#D32F2F',
    marginBottom: 10,
  },
  warningText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  tipContainer: {
    backgroundColor: '#F8F9FA',
    padding: 15,
    borderRadius: 10,
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