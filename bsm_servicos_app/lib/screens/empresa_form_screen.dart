import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/empresa.dart';

class EmpresaFormScreen extends StatefulWidget {
  final Empresa? empresa;

  const EmpresaFormScreen({super.key, this.empresa});

  @override
  State<EmpresaFormScreen> createState() => _EmpresaFormScreenState();
}

class _EmpresaFormScreenState extends State<EmpresaFormScreen> {
  final _formKey = GlobalKey<FormState>();

  late TextEditingController nome;
  late TextEditingController telefone;
  late TextEditingController email;

  bool loading = false;

  @override
  void initState() {
    super.initState();

    nome = TextEditingController(text: widget.empresa?.nome ?? "");
    telefone = TextEditingController(text: widget.empresa?.telefone ?? "");
    email = TextEditingController(text: widget.empresa?.email ?? "");
  }

  Future<void> salvar() async {
    setState(() => loading = true);

    final data = {
      "nome": nome.text,
      "telefone": telefone.text,
      "email": email.text,
      "servico_id": 1, // 🔥 EVITA ERRO (NÃO DEIXAR 0)
    };

    try {
      if (widget.empresa == null) {
        await ApiService.createEmpresa(data);
      } else {
        await ApiService.updateEmpresa(widget.empresa!.id!, data);
      }

      Navigator.pop(context, true);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString())),
      );
    }

    setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.empresa == null
            ? "Criar Empresa"
            : "Editar Empresa"),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: nome,
                decoration: const InputDecoration(labelText: "Nome"),
              ),
              TextFormField(
                controller: telefone,
                decoration: const InputDecoration(labelText: "Telefone"),
              ),
              TextFormField(
                controller: email,
                decoration: const InputDecoration(labelText: "Email"),
              ),

              const SizedBox(height: 20),

              ElevatedButton(
                onPressed: loading ? null : salvar,
                child: Text(loading ? "Salvando..." : "Salvar"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}