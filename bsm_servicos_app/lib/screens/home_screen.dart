import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/empresa.dart';
import '../widgets/app_drawer.dart';
import 'empresa_form_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Future<List<Empresa>>? empresas;

  @override
  void initState() {
    super.initState();

    // 🔥 NÃO CARREGA AUTOMATICAMENTE
    empresas = null;
  }

  Future<void> _carregarEmpresas() async {
    setState(() {
      empresas = ApiService.getEmpresas();
    });
  }

  Future<void> _refresh() async {
    setState(() {
      empresas = ApiService.getEmpresas();
    });
  }

  void _goToLogin() {
    Navigator.pushReplacementNamed(context, "/login");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("BSM Serviços"),
        backgroundColor: Colors.blue,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _carregarEmpresas, // 🔥 botão manual
          ),
        ],
      ),

      drawer: const AppDrawer(),

#      floatingActionButton: FloatingActionButton(
#        onPressed: () async {
#          await Navigator.push(
#            context,
#            MaterialPageRoute(
#             builder: (_) => const EmpresaFormScreen(),
#           ),
#          );
#          _refresh();
#        },
#        child: const Icon(Icons.add),
#      ),

      body: empresas == null
          ? Center(
              child: ElevatedButton(
                onPressed: _carregarEmpresas,
                child: const Text("Carregar Empresas"),
              ),
            )
          : FutureBuilder<List<Empresa>>(
              future: empresas,
              builder: (context, snapshot) {

                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }

                if (snapshot.hasError) {
                  final error = snapshot.error.toString();

                  if (error.contains("Sessão expirada")) {
                    Future.microtask(() => _goToLogin());
                  }

                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text("Erro ao carregar empresas"),
                        const SizedBox(height: 10),
                        ElevatedButton(
                          onPressed: _carregarEmpresas,
                          child: const Text("Tentar novamente"),
                        ),
                      ],
                    ),
                  );
                }

                final list = snapshot.data ?? [];

                if (list.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text("Nenhuma empresa cadastrada"),
                        const SizedBox(height: 10),
                        ElevatedButton(
                          onPressed: _carregarEmpresas,
                          child: const Text("Recarregar"),
                        ),
                      ],
                    ),
                  );
                }

                return RefreshIndicator(
                  onRefresh: _refresh,
                  child: ListView.builder(
                    padding: const EdgeInsets.all(12),
                    itemCount: list.length,
                    itemBuilder: (context, index) {
                      final empresa = list[index];

                      return GestureDetector(
#                        onTap: () async {
#                          await Navigator.push(
#                            context,
#                            MaterialPageRoute(
#                              builder: (_) => EmpresaFormScreen(
#                                empresa: empresa,
#                              ),
#                            ),
#                         );
#                          _refresh();
#                        },

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

                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Expanded(
                                      child: Text(
                                        empresa.nome,
                                        style: const TextStyle(
                                          fontSize: 18,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),

                                    Container(
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 10,
                                        vertical: 4,
                                      ),
                                      decoration: BoxDecoration(
                                        color: Colors.green.withOpacity(0.2),
                                        borderRadius: BorderRadius.circular(20),
                                      ),
                                      child: const Text(
                                        "Ativo",
                                        style: TextStyle(
                                          color: Colors.green,
                                          fontSize: 12,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),

                                const SizedBox(height: 10),

                                Row(
                                  children: [
                                    const Icon(Icons.phone, size: 16),
                                    const SizedBox(width: 6),
                                    Text(empresa.telefone ?? "Sem telefone"),
                                  ],
                                ),

                                const SizedBox(height: 6),

                                Row(
                                  children: [
                                    const Icon(Icons.email, size: 16),
                                    const SizedBox(width: 6),
                                    Text(empresa.email ?? "Sem email"),
                                  ],
                                ),

                                const SizedBox(height: 12),

                                Align(
                                  alignment: Alignment.centerRight,
                                  child: ElevatedButton.icon(
                                    onPressed: () async {
                                      await Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (_) => EmpresaFormScreen(
                                            empresa: empresa,
                                          ),
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
              },
            ),
    );
  }
}