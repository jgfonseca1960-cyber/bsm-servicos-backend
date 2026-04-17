import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/empresa.dart';

class EmpresaDetailScreen extends StatelessWidget {
  final Empresa empresa;

  const EmpresaDetailScreen({super.key, required this.empresa});

  // =========================
  // 📞 AÇÕES
  // =========================
  Future<void> _ligar(String? telefone) async {
    if (telefone == null || telefone.isEmpty) return;
    final uri = Uri.parse("tel:$telefone");
    await launchUrl(uri);
  }

  Future<void> _whatsapp(String? telefone) async {
    if (telefone == null || telefone.isEmpty) return;

    final numero = telefone.replaceAll(RegExp(r'[^0-9]'), '');
    final uri = Uri.parse("https://wa.me/55$numero");

    await launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  Future<void> _email(String? email) async {
    if (email == null || email.isEmpty) return;

    final uri = Uri.parse("mailto:$email");
    await launchUrl(uri);
  }

  Future<void> _mapa() async {
    if (empresa.latitude == null || empresa.longitude == null) return;

    final uri = Uri.parse(
      "https://www.google.com/maps/search/?api=1&query=${empresa.latitude},${empresa.longitude}",
    );

    await launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  // =========================
  // 🎨 UI
  // =========================
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(empresa.nome),
        backgroundColor: Colors.blue,
      ),

      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            // =========================
            // 📸 GALERIA DE FOTOS
            // =========================
            SizedBox(
              height: 220,
              child: empresa.fotos.isNotEmpty
                  ? PageView.builder(
                      itemCount: empresa.fotos.length,
                      itemBuilder: (_, index) {
                        return Image.network(
                          empresa.fotos[index],
                          fit: BoxFit.cover,
                          width: double.infinity,
                          errorBuilder: (_, __, ___) => _placeholder(),
                        );
                      },
                    )
                  : _placeholder(),
            ),

            const SizedBox(height: 16),

            // =========================
            // 📌 INFORMAÇÕES
            // =========================
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [

                  Text(
                    empresa.nome,
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 10),

                  if (empresa.descricao != null)
                    Text(
                      empresa.descricao!,
                      style: const TextStyle(fontSize: 16),
                    ),

                  const SizedBox(height: 16),

                  _infoItem(Icons.phone, empresa.telefone),
                  _infoItem(Icons.email, empresa.email),
                  _infoItem(Icons.location_on, empresa.endereco),

                  const SizedBox(height: 20),

                  // =========================
                  // 🚀 BOTÕES DE AÇÃO
                  // =========================
                  Wrap(
                    spacing: 10,
                    runSpacing: 10,
                    children: [

                      _actionButton(
                        icon: Icons.phone,
                        label: "Ligar",
                        color: Colors.green,
                        onTap: () => _ligar(empresa.telefone),
                      ),

                      _actionButton(
                        icon: Icons.chat,
                        label: "WhatsApp",
                        color: Colors.teal,
                        onTap: () => _whatsapp(empresa.telefone),
                      ),

                      _actionButton(
                        icon: Icons.email,
                        label: "Email",
                        color: Colors.orange,
                        onTap: () => _email(empresa.email),
                      ),

                      _actionButton(
                        icon: Icons.map,
                        label: "Mapa",
                        color: Colors.blue,
                        onTap: _mapa,
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // =========================
  // 🔧 COMPONENTES
  // =========================
  Widget _infoItem(IconData icon, String? text) {
    if (text == null || text.isEmpty) return const SizedBox();

    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Icon(icon, size: 18),
          const SizedBox(width: 8),
          Expanded(child: Text(text)),
        ],
      ),
    );
  }

  Widget _actionButton({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return ElevatedButton.icon(
      onPressed: onTap,
      icon: Icon(icon),
      label: Text(label),
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      ),
    );
  }

  Widget _placeholder() {
    return Container(
      color: Colors.grey[300],
      child: const Center(
        child: Icon(Icons.image_not_supported, size: 50),
      ),
    );
  }
}