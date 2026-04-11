import 'package:flutter/material.dart';
import 'screens/auth_check_screen.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';


## Temporario

home: TesteEmpresas(),

##

void main() {
  throw Exception("🔥 TESTE MAIN 🔥");
}

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'BSM Serviços',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),

      // 🔥 ROTAS DO SISTEMA
      initialRoute: "/",
      routes: {
        "/": (context) => const AuthCheckScreen(),
        "/login": (context) => const LoginScreen(),
        "/home": (context) => const HomeScreen(),
      },
    );
  }
}

