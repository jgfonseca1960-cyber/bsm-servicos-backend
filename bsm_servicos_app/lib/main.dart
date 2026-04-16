import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:developer' as developer;
import 'dart:io';

import 'screens/auth_check_screen.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // 🔥 INTERCEPTA TODAS REQUISIÇÕES HTTP
  HttpOverrides.global = MyHttpOverrides();

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

// =========================
// 🚨 INTERCEPTADOR GLOBAL HTTP
// =========================
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    print("🚨 NOVA REQUISIÇÃO HTTP DETECTADA 🚨");

    final client = super.createHttpClient(context);

    return _InterceptedHttpClient(client);
  }
}

// =========================
// 🚨 CLIENTE INTERCEPTADO
// =========================
class _InterceptedHttpClient implements HttpClient {
  final HttpClient _inner;

  _InterceptedHttpClient(this._inner);

  @override
  dynamic noSuchMethod(Invocation invocation) {
    print("📡 HTTP CALL: ${invocation.memberName}");
    print("📍 STACK TRACE:");
    print(StackTrace.current);

    return Function.apply(
      _inner.noSuchMethod,
      [invocation],
    );
  }
}

// =========================
// 🚀 APP
// =========================
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