import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:image_picker/image_picker.dart';

import '../models/empresa.dart';

class ApiService {
#  static const String baseUrl = "https://bsm-servicos-backend.onrender.com";
#  static const String empresaUrl = "https://ERRO-TESTE-123.com/empresa/";
static const String baseUrl = "https://ERRO-ABSURDO-123456.com";

  // ✅ URL CORRETA (SEM /listar)
  static const String empresaUrl = "$baseUrl/empresa";

  static const String authLoginUrl = "$baseUrl/auth/login";

  // =========================
  // 🔐 TOKEN
  // =========================
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString("token");
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove("token");
  }

  static Future<Map<String, String>> _headers() async {
    final token = await getToken();

    return {
      "Content-Type": "application/json",
      if (token != null) "Authorization": "Bearer $token",
    };
  }

  // =========================
  // 🔐 LOGIN
  // =========================
  static Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse(authLoginUrl),
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: {"username": email, "password": password},
    );

    print("🔐 LOGIN STATUS: ${response.statusCode}");
    print("🔐 LOGIN BODY: ${response.body}");

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final token = data["access_token"];

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("token", token);

      return token;
    } else {
      throw Exception("Erro no login: ${response.body}");
    }
  }

  // =========================
  // 📌 LISTAR EMPRESAS (CORRIGIDO)
  // =========================

  static Future<List<Empresa>> getEmpresas() async {
    print("🔥🔥🔥 CHAMOU API NOVA 🔥🔥🔥");

    final response = await http.get(
      Uri.parse(empresaUrl), // ✅ SEM /listar
      headers: await _headers(),
    );

    print("STATUS: ${response.statusCode}");

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((e) => Empresa.fromJson(e)).toList();
    }

    throw Exception("Erro ao buscar empresas");
  }

  // =========================
  // 📸 UPLOAD FOTO
  // =========================
  static Future<void> uploadFoto(int empresaId, XFile imagem) async {
    final url = "$baseUrl/empresa/$empresaId/upload-foto";

    print("📸 UPLOAD URL: $url");

    final request = http.MultipartRequest("POST", Uri.parse(url));

    final token = await getToken();

    if (token != null) {
      request.headers["Authorization"] = "Bearer $token";
    }

    request.files.add(await http.MultipartFile.fromPath("file", imagem.path));

    final response = await request.send();

    print("📸 STATUS UPLOAD: ${response.statusCode}");

    if (response.statusCode != 200) {
      throw Exception("Erro ao enviar foto");
    }
  }
}
