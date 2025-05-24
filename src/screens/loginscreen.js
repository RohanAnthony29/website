import React, {useState} from 'react';
import { View, Text, TextInput,Button,StyleSheet} from 'react-native';

export default function LoginScreen({NavigationActivation, route}){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const user = route.params?.user;

    const handleLogin = () => {
        if (email && password && user &&email ===user.email && password === user.password) {
            navigation.replace('Profile', {user});
        } else {
            alert('Invalid credentials or user not found');
        }
    };
    return(
        <View style={StyleSheet.container}>
            <Text style={Styles.title}>Welcome To Steak's Login Page</Text>
            <TextInput placeholder="Email Address" value={email} onChangeText={setEmail} style={style.input} />
            

    )