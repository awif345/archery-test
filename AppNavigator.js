// AppNavigator.js
import { createStackNavigator } from '@react-navigation/stack';
import AuthStack from '../screens/AuthStack';
import MainStack from '../screens/MainStack';

const Stack = createStackNavigator();

const AppNavigator = () => (
  <Stack.Navigator headerMode="none">
    <Stack.Screen name="Auth" component={AuthStack} />
    <Stack.Screen name="Main" component={MainStack} />
  </Stack.Navigator>
);

export default AppNavigator;
