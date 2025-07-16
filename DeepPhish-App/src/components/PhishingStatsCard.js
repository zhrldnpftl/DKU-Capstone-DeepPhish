// components/PhishingStatsCard.js
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import axios from 'axios';

export default function PhishingStatsCard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        setError(null);

        // 바로 작동하는 방법으로 시작 (Decoding된 키 사용)
        await tryAlternativeMethods();
      } catch (error) {
        console.error('📛 API 호출 완전 실패:', error);
        setError(`데이터를 불러올 수 없습니다: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    // 대안 API 호출 방법들
    const tryAlternativeMethods = async () => {
      const alternatives = [
        // 방법 2: Decoding된 키 사용
        {
          url: 'https://api.odcloud.kr/api/15063815/v1/uddi:754afc24-fc2f-49f6-8b2b-e232e6455bd4',
          key: 'mB4BJmr2CO5yJhiswG0fXVPTqyJnDbWCo2sfp2Ax7TwzpOTm7/nDHpyamB7kBfvuJ73/bfudbE/TmOZsNQjByA=='
        },
        // 방법 3: 다른 데이터셋 시도 (통계 데이터)
        {
          url: 'https://api.odcloud.kr/api/15063815/v1/uddi:099dbb6a-84f0-4394-90b2-d4d2a839f842',
          key: 'mB4BJmr2CO5yJhiswG0fXVPTqyJnDbWCo2sfp2Ax7TwzpOTm7%2FnDHpyamB7kBfvuJ73%2FbfudbE%2FTmOZsNQjByA%3D%3D'
        }
      ];

      for (const alt of alternatives) {
        try {
          console.log(`🔄 API 호출 시작: ${alt.url}`);
          
          const response = await axios.get(alt.url, {
            params: {
              page: 1,
              perPage: alt.perPage || 100,
              returnType: 'json',
              serviceKey: alt.key,
            },
            timeout: 10000,
          });

          console.log(`✅ API 호출 성공:`, response.data);
          console.log(`📊 총 ${response.data?.totalCount}개 데이터 중 ${response.data?.currentCount}개 조회`);
          
          if (response.data && response.data.data && response.data.data.length > 0) {
            // 최신 데이터 찾기
            const sortedData = response.data.data.sort((a, b) => {
              const yearA = parseInt(a.구분) || 0;
              const yearB = parseInt(b.구분) || 0;
              return yearB - yearA;
            });
            
            const latestData = sortedData[0];
            console.log(`🎯 선택된 최신 데이터 (${latestData.구분}년):`, latestData);
            
            setStats(latestData);
            setError(null);
            return; // 성공하면 루프 종료
          }
        } catch (altError) {
          console.error(`❌ API 호출 실패:`, altError.message);
        }
      }
      
      // 모든 방법이 실패한 경우
      setError('모든 API 호출 방법이 실패했습니다.');
    };

    fetchStats();
  }, []);

  const renderStatsContent = () => {
    if (loading) {
      return <Text style={styles.cardItem}>📊 데이터 불러오는 중...</Text>;
    }

    if (error) {
      return (
        <View>
          <Text style={[styles.cardItem, styles.errorText]}>⚠️ {error}</Text>
          <Text style={styles.cardItem}>잠시 후 다시 시도해주세요.</Text>
        </View>
      );
    }

    if (!stats) {
      return <Text style={styles.cardItem}>데이터를 찾을 수 없습니다.</Text>;
    }

    return (
      <View style={styles.scrollableContent}>
        <Text style={styles.cardSubtitle}>📅 {stats.구분}년 데이터</Text>
        <Text style={styles.sourceText}>출처: 공공데이터 포털 경찰청_보이스피싱 통계</Text>
        
        {/* 가로 배치된 통계 컨테이너 */}
        <View style={styles.horizontalStatsContainer}>
          {/* 기관사칭형 (좌측) */}
          <View style={styles.leftStatsSection}>
            <Text style={styles.sectionTitle}>🏛️ 기관사칭형</Text>
            <Text style={styles.cardItem}>• 발생: {stats.기관사칭형_발생건수?.toLocaleString() || 'N/A'}건</Text>
            <Text style={styles.cardItem}>• 피해액: {stats.기관사칭형_피해액_억원?.toLocaleString() || 'N/A'}억원</Text>
            <Text style={styles.cardItem}>• 검거: {stats.기관사칭형_검거건수?.toLocaleString() || 'N/A'}건</Text>
            {stats.기관사칭형_검거인원 && (
              <Text style={styles.cardItem}>• 검거인원: {stats.기관사칭형_검거인원?.toLocaleString()}명</Text>
            )}
          </View>
          
          {/* 구분선 */}
          <View style={styles.divider} />
          
          {/* 대출사기형 (우측) */}
          <View style={styles.rightStatsSection}>
            <Text style={styles.sectionTitle}>💳 대출사기형</Text>
            <Text style={styles.cardItem}>• 발생: {stats.대출사기형_발생건수?.toLocaleString() || 'N/A'}건</Text>
            <Text style={styles.cardItem}>• 피해액: {stats.대출사기형_피해액_억원?.toLocaleString() || 'N/A'}억원</Text>
            <Text style={styles.cardItem}>• 검거: {stats.대출사기형_검거건수?.toLocaleString() || 'N/A'}건</Text>
            {stats.대출사기형_검거인원 && (
              <Text style={styles.cardItem}>• 검거인원: {stats.대출사기형_검거인원?.toLocaleString()}명</Text>
            )}
          </View>
        </View>
        
        <View style={styles.summaryContainer}>
          <Text style={styles.summaryTitle}>📊 총합</Text>
          <Text style={styles.summaryItem}>
            • 총 발생: {((stats.기관사칭형_발생건수 || 0) + (stats.대출사기형_발생건수 || 0)).toLocaleString()}건
          </Text>
          <Text style={styles.summaryItem}>
            • 총 피해액: {((stats.기관사칭형_피해액_억원 || 0) + (stats.대출사기형_피해액_억원 || 0)).toLocaleString()}억원
          </Text>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.card}>
      <Text style={styles.cardTitle}>📊 보이스 피싱 현황</Text>
      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={true}
        nestedScrollEnabled={true}
      >
        {renderStatsContent()}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    marginTop: 30,
    backgroundColor: '#F8F8F8',
    borderRadius: 10,
    width: '100%',
    height: 400, // 고정 높이 설정 - 스크롤을 위해 필수
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    padding: 20,
    paddingBottom: 10,
    color: '#333',
    textAlign: 'center',
    backgroundColor: '#F8F8F8',
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 20,
  },
  scrollContent: {
    paddingBottom: 20,
  },
  scrollableContent: {
    width: '100%',
  },
  cardSubtitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 5,
    color: '#555',
    textAlign: 'center',
  },
  sourceText: {
    fontSize: 11,
    color: '#888',
    textAlign: 'center',
    marginBottom: 15,
    fontStyle: 'italic',
  },
  cardItem: {
    fontSize: 14,
    marginVertical: 3,
    color: '#666',
    lineHeight: 20,
    textAlign: 'center',
  },
  errorText: {
    color: '#D32F2F',
    fontWeight: '500',
  },
  // 가로 배치를 위한 스타일들
  horizontalStatsContainer: {
    flexDirection: 'row',
    marginVertical: 10,
    minHeight: 120,
  },
  leftStatsSection: {
    flex: 1,
    paddingRight: 10,
    alignItems: 'center',
  },
  rightStatsSection: {
    flex: 1,
    paddingLeft: 10,
    alignItems: 'center',
  },
  divider: {
    width: 1,
    backgroundColor: '#D0D0D0',
    marginHorizontal: 5,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
    textAlign: 'center',
  },
  summaryContainer: {
    marginTop: 15,
    padding: 15,
    backgroundColor: '#E8F5E8',
    borderRadius: 8,
    alignItems: 'center',
  },
  summaryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#2E7D32',
    textAlign: 'center',
  },
  summaryItem: {
    fontSize: 14,
    marginVertical: 2,
    color: '#2E7D32',
    fontWeight: '500',
    textAlign: 'center',
  },
  // 추가 정보 섹션
  additionalInfo: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#FFF3E0',
    borderRadius: 8,
  },
  additionalTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#F57C00',
    textAlign: 'center',
  },
  additionalText: {
    fontSize: 13,
    marginVertical: 3,
    color: '#666',
    textAlign: 'center',
    lineHeight: 18,
  },
  // 신고 안내 섹션
  reportInfo: {
    marginTop: 15,
    padding: 15,
    backgroundColor: '#FFEBEE',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
  },
  reportTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#D32F2F',
    textAlign: 'center',
  },
  reportText: {
    fontSize: 13,
    marginVertical: 2,
    color: '#666',
    textAlign: 'center',
  },
});