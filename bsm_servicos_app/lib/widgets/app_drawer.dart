import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  Future<void> _logout(BuildContext context) async {
    await ApiService.logout();

    if (context.mounted) {
      Navigator.pushNamedAndRemoveUntil(
        context,
        "/login",
        (route) => false,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Column(
        children: [

          // 🔥 HEADER PROFISSIONAL
          UserAccountsDrawerHeader(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.blue, Colors.blueAccent],
              ),
            ),
            accountName: const Text(
              "BSM Usuário",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            accountEmail: const Text("logado"),
            currentAccountPicture: const CircleAvatar(
              backgroundColor: Colors.white,
              child: Icon(Icons.person, size: 40, color: Colors.blue),
            ),
          ),

          // 🔥 HOME
          ListTile(
            leading: const Icon(Icons.home),
            title: const Text("Início"),
            onTap: () {
              Navigator.pushNamedAndRemoveUntil(
                context,
                "/home",
                (route) => false,
              );
            },
          ),

          // 🔥 EMPRESAS
          ListTile(
            leading: const Icon(Icons.business),
            title: const Text("Empresas"),
            onTap: () {
              Navigator.pushNamedAndRemoveUntil(
                context,
                "/home",
                (route) => false,
              );
            },
          ),

          const Divider(),

          // 🔥 SAIR
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text("Sair"),
            onTap: () => _logout(context),
          ),
        ],
      ),
    );
  }
}