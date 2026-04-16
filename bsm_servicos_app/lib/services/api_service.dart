import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/empresa.dart';

class ApiService {
  static const String baseUrl =
      "https://bsm-servicos-backend.onrender.com";

  // =========================
  // 📌 ENDPOINTS CENTRALIZADOS
  // =========================
  static const String empresaUrl =
      "$baseUrl/empresa/empresas";

  static const String authLoginUrl =
      "$baseUrl/auth/login";

  static const String servicosUrl =
      "$baseUrl/servicos";

  // =========================
  // 🔐 TOKEN
  // =========================
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString("token");
  }

  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString("token", token);
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove("token");
  }

  // =========================
  // 🔐 LOGIN
  // =========================
  static Future<String> login(String email, String password) async {
    final url = Uri.parse(authLoginUrl);

    print("🌐 LOGIN URL: $url");

    final response = await http.post(
      url,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: {
        "username": email,
        "password": password,
      },
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode >= 200 && response.statusCode < 300) {
      final data = jsonDecode(response.body);
      final token = data["access_token"];

      await saveToken(token);
      return token;
    } else {
      throw Exception("Erro no login: ${response.body}");
    }
  }

  // =========================
  // 🔥 HEADERS AUTH
  // =========================
  static Future<Map<String, String>> _headers() async {
    final token = await getToken();

    final headers = {
      "Content-Type": "application/json",
    };

    if (token != null && token.isNotEmpty) {
      headers["Authorization"] = "Bearer $token";
    }

    return headers;
  }

  // =========================
  // 🏢 EMPRESAS
  // =========================

  // 🔥 LISTAR (MODO DEBUG ATIVO)
  static Future<List<Empresa>> getEmpresas() async {
    print("🚨🚨🚨 getEmpresas FOI CHAMADO 🚨🚨🚨");
    print("📍 STACK TRACE COMPLETO:");
    print(StackTrace.current);

    // 🔴 BLOQUEIO TEMPORÁRIO (REMOVE ERRO)
    print("⛔ CHAMADA REAL BLOQUEADA TEMPORARIAMENTE");
    await Future.delayed(Duration(seconds: 1));

    return []; // evita erro no app
  }

  // =========================
  // ⚠️ RESTANTE NORMAL
  // =========================

  static Future<void> createEmpresa(
      Map<String, dynamic> data) async {
    final url = Uri.parse(empresaUrl);

    print("🌐 CREATE EMPRESA: $url");

    final response = await http.post(
      url,
      headers: await _headers(),
      body: jsonEncode(data),
    );

    if (response.statusCode < 200 ||
        response.statusCode >= 300) {
      throw Exception(
          "Erro ao criar empresa: ${response.body}");
    }
  }

  static Future<void> updateEmpresa(
      int id, Map<String, dynamic> data) async {
    final url = Uri.parse("$empresaUrl/$id");

    print("🌐 UPDATE EMPRESA: $url");

    final response = await http.put(
      url,
      headers: await _headers(),
      body: jsonEncode(data),
    );

    if (response.statusCode < 200 ||
        response.statusCode >= 300) {
      throw Exception(
          "Erro ao atualizar empresa: ${response.body}");
    }
  }

  static Future<void> deleteEmpresa(int id) async {
    final url = Uri.parse("$empresaUrl/$id");

    print("🌐 DELETE EMPRESA: $url");

    final response = await http.delete(
      url,
      headers: await _headers(),
    );

    if (response.statusCode < 200 ||
        response.statusCode >= 300) {
      throw Exception(
          "Erro ao deletar empresa: ${response.body}");
    }
  }

  // =========================
  // 🛠️ SERVIÇOS
  // =========================
  static Future<List<dynamic>> getServicos() async {
    final url = Uri.parse(servicosUrl);

    print("🌐 GET SERVIÇOS: $url");

    final response = await http.get(
      url,
      headers: await _headers(),
    );

    if (response.statusCode >= 200 &&
        response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception(
          "Erro ao buscar serviços: ${response.body}");
    }
  }
}