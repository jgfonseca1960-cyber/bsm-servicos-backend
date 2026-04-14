import 'package:flutter/material.dart';
import 'dart:developer' as developer;

import 'screens/auth_check_screen.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // 🔥 CAPTURA TODOS OS ERROS DO FLUTTER
  FlutterError.onError = (FlutterErrorDetails details) {
    print("🔥 ERRO FLUTTER:");
    print(details.exception);
    print(details.stack);
  };

  // 🔥 CAPTURA ERROS GERAIS (ASYNC)
  runZonedGuarded(() {
    runApp(const MyApp());
  }, (error, stack) {
    print("💥 ERRO GLOBAL:");
    print(error);
    print(stack);
  });
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
      initialRoute: "/",
      routes: {
        "/": (context) => const AuthCheckScreen(),
        "/login": (context) => const LoginScreen(),
        "/home": (context) => const HomeScreen(),
      },
    );
  }
}