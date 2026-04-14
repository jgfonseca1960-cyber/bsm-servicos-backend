import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/empresa.dart';

class ApiService {
  static const String baseUrl = "https://bsm-servicos-backend.onrender.com";

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
    final url = Uri.parse("$baseUrl/auth/login");

    print("🌐 LOGIN:");
    print("➡️ URL: $url");
    print("📍 STACK TRACE:");
    print(StackTrace.current);

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
  // 🏢 LISTAR EMPRESAS
  // =========================
  static Future<List<Empresa>> getEmpresas() async {
    try {
      final url = Uri.parse("$baseUrl/empresas/");

      print("🌐 GET EMPRESAS:");
      print("➡️ URL: $url");
      print("📍 STACK TRACE:");
      print(StackTrace.current);

      final response = await http.get(url, headers: await _headers());

      print("🔥 STATUS: ${response.statusCode}");
      print("🔥 BODY: ${response.body}");

      if (response.statusCode >= 200 && response.statusCode < 300) {
        final decoded = jsonDecode(response.body);

        final List data = decoded is List
            ? decoded
            : decoded["empresas"] ?? [];

        return data.map((e) => Empresa.fromJson(e)).toList();
      } else {
        throw Exception("Erro ${response.statusCode}: ${response.body}");
      }
    } catch (e, stack) {
      print("❌ ERRO: $e");
      print("📍 STACK TRACE ERRO:");
      print(stack);
      throw Exception("Falha ao carregar empresas");
    }
  }

  // =========================
  // ➕ CRIAR EMPRESA
  // =========================
  static Future<void> createEmpresa(Map<String, dynamic> data) async {
    final url = Uri.parse("$baseUrl/empresas/");

    print("🌐 CREATE EMPRESA:");
    print("➡️ URL: $url");
    print("📍 STACK TRACE:");
    print(StackTrace.current);

    final response = await http.post(
      url,
      headers: await _headers(),
      body: jsonEncode(data),
    );

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Erro ao criar empresa: ${response.body}");
    }
  }

  // =========================
  // ✏️ ATUALIZAR EMPRESA
  // =========================
  static Future<void> updateEmpresa(int id, Map<String, dynamic> data) async {
    final url = Uri.parse("$baseUrl/empresas/$id");

    print("🌐 UPDATE EMPRESA:");
    print("➡️ URL: $url");
    print("📍 STACK TRACE:");
    print(StackTrace.current);

    final response = await http.put(
      url,
      headers: await _headers(),
      body: jsonEncode(data),
    );

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Erro ao atualizar empresa: ${response.body}");
    }
  }

  // =========================
  // ❌ DELETAR EMPRESA
  // =========================
  static Future<void> deleteEmpresa(int id) async {
    final url = Uri.parse("$baseUrl/empresas/$id");

    print("🌐 DELETE EMPRESA:");
    print("➡️ URL: $url");
    print("📍 STACK TRACE:");
    print(StackTrace.current);

    final response = await http.delete(
      url,
      headers: await _headers(),
    );

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Erro ao deletar empresa: ${response.body}");
    }
  }

  // =========================
  // 🛠️ LISTAR SERVIÇOS
  // =========================
  static Future<List<dynamic>> getServicos() async {
    final url = Uri.parse("$baseUrl/servicos/");

    print("🌐 GET SERVIÇOS:");
    print("➡️ URL: $url");
    print("📍 STACK TRACE:");
    print(StackTrace.current);

    final response = await http.get(url, headers: await _headers());

    print("🔥 STATUS SERVIÇOS: ${response.statusCode}");

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erro ao buscar serviços: ${response.body}");
    }
  }
}