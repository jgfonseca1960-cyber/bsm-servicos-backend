class Empresa {
  final int id;
  final String nome;
  final String? telefone;
  final String? email;
  final String? endereco;
  final double? latitude;
  final double? longitude;
  final List<String> fotos;

  Empresa({
    required this.id,
    required this.nome,
    this.telefone,
    this.email,
    this.endereco,
    this.latitude,
    this.longitude,
    required this.fotos,
  });

  factory Empresa.fromJson(Map<String, dynamic> json) {
    return Empresa(
      id: json["id"],
      nome: json["nome"] ?? "",
      telefone: json["telefone"],
      email: json["email"],
      endereco: json["endereco"],
      latitude: json["latitude"] != null
          ? double.tryParse(json["latitude"].toString())
          : null,
      longitude: json["longitude"] != null
          ? double.tryParse(json["longitude"].toString())
          : null,

      // 🔥 TRATAMENTO DE FOTOS
      fotos: (json["fotos"] as List?)
              ?.map((f) => f["url"].toString())
              .toList() ??
          [],
    );
  }
}