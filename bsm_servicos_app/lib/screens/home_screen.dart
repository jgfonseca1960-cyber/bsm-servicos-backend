import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/empresa.dart';
import '../widgets/app_drawer.dart';
import 'empresa_form_screen.dart';
import 'empresa_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Empresa> empresas = [];
  bool carregando = false;
  String? erro;

  @override
  void initState() {
    super.initState();
    carregarEmpresas();
  }

  Future<void> carregarEmpresas() async {
    setState(() {
      carregando = true;
      erro = null;
    });

    try {
      final data = await ApiService.getEmpresas();

      setState(() {
        empresas = data;
      });
    } catch (e) {
      print("❌ ERRO REAL: $e");

      setState(() {
        erro = "Falha ao conectar com servidor";
      });
    } finally {
      setState(() {
        carregando = false;
      });
    }
  }

  Future<void> _refresh() async {
    await carregarEmpresas();
  }

  void _mostrarErroDetalhado() {
    if (erro == null) return;

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text("Erro"),
        content: Text(erro!),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Fechar"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("BSM Serviços"),
        backgroundColor: Colors.blue,
      ),
      drawer: const AppDrawer(),

      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const EmpresaFormScreen(),
            ),
          );
          _refresh();
        },
        child: const Icon(Icons.add),
      ),

      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (carregando) {
      return const Center(child: CircularProgressIndicator());
    }

    if (erro != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Erro ao carregar empresas",
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 10),

            ElevatedButton(
              onPressed: carregarEmpresas,
              child: const Text("Tentar novamente"),
            ),

            const SizedBox(height: 10),

            TextButton(
              onPressed: _mostrarErroDetalhado,
              child: const Text("Ver detalhes do erro"),
            ),
          ],
        ),
      );
    }

    if (empresas.isEmpty) {
      return const Center(
        child: Text("Nenhuma empresa cadastrada"),
      );
    }

    return RefreshIndicator(
      onRefresh: _refresh,
      child: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: empresas.length,
        itemBuilder: (context, index) {
          final empresa = empresas[index];

          return GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => EmpresaDetailScreen(empresa: empresa),
                ),
              );
            },
            child: Container(
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.08),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [

                    // 📸 FOTO
                    if (empresa.fotos.isNotEmpty)
                      ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.network(
                          empresa.fotos.first,
                          height: 150,
                          width: double.infinity,
                          fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) => _placeholder(),
                        ),
                      )
                    else
                      _placeholder(),

                    const SizedBox(height: 10),

                    // 📌 NOME
                    Text(
                      empresa.nome,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 6),

                    Text(empresa.telefone ?? "Sem telefone"),
                    Text(empresa.email ?? "Sem email"),

                    const SizedBox(height: 10),

                    // ✏️ EDITAR
                    Align(
                      alignment: Alignment.centerRight,
                      child: ElevatedButton.icon(
                        onPressed: () async {
                          await Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  EmpresaFormScreen(empresa: empresa),
                            ),
                          );
                          _refresh();
                        },
                        icon: const Icon(Icons.edit),
                        label: const Text("Editar"),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _placeholder() {
    return Container(
      height: 150,
      decoration: BoxDecoration(
        color: Colors.grey[300],
        borderRadius: BorderRadius.circular(12),
      ),
      child: const Center(
        child: Icon(Icons.image_not_supported),
      ),
    );
  }
}