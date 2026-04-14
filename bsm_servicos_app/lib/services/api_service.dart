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
    final response = await http
        .post(
          Uri.parse("$baseUrl/auth/login"),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: {
            "username": email,
            "password": password,
          },
        )
        .timeout(Duration(seconds: 10));

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

      print("🔥 URL FINAL: $url");
      print("🔥 TOKEN: ${await getToken()}");

      final response = await http
          .get(url, headers: await _headers())
          .timeout(Duration(seconds: 10));

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
    } catch (e) {
      print("❌ ERRO COMPLETO: $e");
      throw Exception("Falha ao carregar empresas");
    }
  }

  // =========================
  // ➕ CRIAR EMPRESA
  // =========================
  static Future<void> createEmpresa(Map<String, dynamic> data) async {
    if (data["servico_id"] == 0) {
      data.remove("servico_id");
    }

    final response = await http
        .post(
          Uri.parse("$baseUrl/empresas/"),
          headers: await _headers(),
          body: jsonEncode(data),
        )
        .timeout(Duration(seconds: 10));

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Erro ao criar empresa: ${response.body}");
    }
  }

  // =========================
  // ✏️ ATUALIZAR EMPRESA
  // =========================
  static Future<void> updateEmpresa(
    int id,
    Map<String, dynamic> data,
  ) async {
    if (data["servico_id"] == 0) {
      data.remove("servico_id");
    }

    final response = await http
        .put(
          Uri.parse("$baseUrl/empresas/$id"),
          headers: await _headers(),
          body: jsonEncode(data),
        )
        .timeout(Duration(seconds: 10));

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Erro ao atualizar empresa: ${response.body}");
    }
  }

  // =========================
  // ❌ DELETAR EMPRESA
  // =========================
  static Future<void> deleteEmpresa(int id) async {
    final response = await http
        .delete(
          Uri.parse("$baseUrl/empresas/$id"),
          headers: await _headers(),
        )
        .timeout(Duration(seconds: 10));

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Erro ao deletar empresa: ${response.body}");
    }
  }

  // =========================
  // 🛠️ LISTAR SERVIÇOS
  // =========================
  static Future<List<dynamic>> getServicos() async {
    final url = Uri.parse("$baseUrl/servicos/");

    print("🔥 BUSCANDO SERVIÇOS: $url");

    final response = await http
        .get(url, headers: await _headers())
        .timeout(Duration(seconds: 10));

    print("🔥 STATUS SERVIÇOS: ${response.statusCode}");
    print("🔥 BODY SERVIÇOS: ${response.body}");

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erro ao buscar serviços: ${response.body}");
    }
  }
}