// bokbok/App.js

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Toast from 'react-native-toast-message';
import { toastConfig } from './src/components/ToastConfig';

// 📌 화면들 import (src 기준으로 경로 수정)
import HomePage from './src/screens/HomePage';
import DetectPage from './src/screens/DetectPage';
import DetectLoadingPage from './src/screens/DetectLoadingPage';
import DetectResultPage from './src/screens/DetectResultPage';
import PhoneCheckPage from './src/screens/PhoneCheckPage';
import ReportPage from './src/screens/ReportPage';
// GuidePage와 SafetyPage는 HomePage 내에서 모달로 사용되므로 여기서 import하지 않음

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="HomePage"
        screenOptions={{ headerShown: false }} // ✅ 각 페이지 제목 뜨지 않게 해줌줌
      >
        <Stack.Screen name="HomePage" component={HomePage} />
        <Stack.Screen name="DetectPage" component={DetectPage} />
        <Stack.Screen name="DetectLoadingPage" component={DetectLoadingPage} />
        <Stack.Screen name="DetectResultPage" component={DetectResultPage} />
        <Stack.Screen name="PhoneCheckPage" component={PhoneCheckPage} />
        <Stack.Screen name="ReportPage" component={ReportPage} />
      </Stack.Navigator>
      <Toast />
    </NavigationContainer>
  );
}