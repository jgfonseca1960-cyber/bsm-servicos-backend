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
    final response = await http.post(
      Uri.parse("$baseUrl/auth/login"),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: {
        "username": email,
        "password": password,
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final token = data["access_token"];

      await saveToken(token);
      return token;
    } else {
      throw Exception("Erro no login");
    }
  }

  // =========================
  // 🔥 HEADERS AUTH
  // =========================
  static Future<Map<String, String>> _headers() async {
    final token = await getToken();

    return {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token",
    };
  }

  // =========================
  // 🏢 LISTAR EMPRESAS
  // =========================

static Future<List<Empresa>> getEmpresas() async {
  final url = "https://bsm-servicos-backend.onrender.com/empresas/";

  print("🔥 URL FINAL: $url");

  final response = await http.get(
    Uri.parse(url),
    headers: await _headers(),
  );

  print("🔥 STATUS: ${response.statusCode}");
  print("🔥 BODY: ${response.body}");

  if (response.statusCode == 200) {
    List data = jsonDecode(response.body);
    return data.map((e) => Empresa.fromJson(e)).toList();
  } else {
    throw Exception("Erro ao buscar empresas");
  }
}
 
  // =========================
  // ➕ CRIAR EMPRESA
  // =========================
  static Future<void> createEmpresa(Map<String, dynamic> data) async {
    // 🔥 REMOVE servico_id = 0 (BUG QUE VOCÊ TEVE)
    if (data["servico_id"] == 0) {
      data.remove("servico_id");
    }

    final response = await http.post(
      Uri.parse("$baseUrl/empresas/"),
      headers: await _headers(),
      body: jsonEncode(data),
    );

    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception("Erro ao criar empresa");
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

    final response = await http.put(
      Uri.parse("$baseUrl/empresas/$id"),
      headers: await _headers(),
      body: jsonEncode(data),
    );

    if (response.statusCode != 200) {
      throw Exception("Erro ao atualizar empresa");
    }
  }

  // =========================
  // ❌ DELETAR EMPRESA
  // =========================
  static Future<void> deleteEmpresa(int id) async {
    final response = await http.delete(
      Uri.parse("$baseUrl/empresas/$id"),
      headers: await _headers(),
    );

    if (response.statusCode != 200) {
      throw Exception("Erro ao deletar empresa");
    }
  }
}