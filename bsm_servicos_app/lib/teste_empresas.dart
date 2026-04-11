import 'package:flutter/material.dart';
import 'api_service.dart';

class TesteEmpresas extends StatefulWidget {
  const TesteEmpresas({super.key});

  @override
  State<TesteEmpresas> createState() => _TesteEmpresasState();
}

class _TesteEmpresasState extends State<TesteEmpresas> {

  @override
  void initState() {
    super.initState();

    print("🔥 TELA ABRIU");

    ApiService.getEmpresas().then((data) {
      print("🔥 EMPRESAS: ${data.length}");
    }).catchError((e) {
      print("🔥 ERRO: $e");
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Teste Empresas")),
      body: Center(
        child: Text("Ver console"),
      ),
    );
  }
}