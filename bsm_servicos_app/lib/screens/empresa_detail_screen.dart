import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/empresa.dart';

class EmpresaDetailScreen extends StatefulWidget {
  final int empresaId;

  const EmpresaDetailScreen({
    super.key,
    required this.empresaId,
  });

  @override
  State<EmpresaDetailScreen> createState() => _EmpresaDetailScreenState();
}

class _EmpresaDetailScreenState extends State<EmpresaDetailScreen> {
  late Future<Empresa> empresa;

  @override
  void initState() {
    super.initState();
    empresa = ApiService.getEmpresa(widget.empresaId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Detalhes da Empresa"),
      ),

      body: FutureBuilder<Empresa>(
        future: empresa,
        builder: (context, snapshot) {

          // 🔵 LOADING
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          // 🔴 ERRO
          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error, color: Colors.red, size: 40),
                  const SizedBox(height: 10),
                  const Text("Erro ao carregar empresa"),
                  const SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        empresa = ApiService.getEmpresa(widget.empresaId);
                      });
                    },
                    child: const Text("Tentar novamente"),
                  )
                ],
              ),
            );
          }

          final data = snapshot.data!;

          // 🟢 CONTEÚDO
          return Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [

                Text(
                  data.nome,
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 20),

                _info("Telefone", data.telefone),
                _info("Email", data.email),

                const SizedBox(height: 20),

                const Divider(),

                const SizedBox(height: 10),

                const Text(
                  "Status:",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),

                Text(
                  data.ativo == true ? "Ativo" : "Inativo",
                  style: TextStyle(
                    color: data.ativo == true ? Colors.green : Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _info(String label, String? value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        children: [
          Text(
            "$label: ",
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          Expanded(
            child: Text(value ?? "Não informado"),
          ),
        ],
      ),
    );
  }
}