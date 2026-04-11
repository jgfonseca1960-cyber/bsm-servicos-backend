class Empresa {
  final int id;
  final String nome;

  final String? telefone;
  final String? email;
  final String? endereco;

  // 🗺️ NÍVEL 6 - GEOLOCALIZAÇÃO
  final double? latitude;
  final double? longitude;

  Empresa({
    required this.id,
    required this.nome,
    this.telefone,
    this.email,
    this.endereco,
    this.latitude,
    this.longitude,
  });

  factory Empresa.fromJson(Map<String, dynamic> json) {
    return Empresa(
      id: json['id'],
      nome: json['nome'] ?? '',

      telefone: json['telefone'],
      email: json['email'],
      endereco: json['endereco'],

      // 🔥 conversão segura (backend pode vir int/double/string)
      latitude: json['latitude'] != null
          ? double.tryParse(json['latitude'].toString())
          : null,

      longitude: json['longitude'] != null
          ? double.tryParse(json['longitude'].toString())
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "nome": nome,
      "telefone": telefone,
      "email": email,
      "endereco": endereco,
      "latitude": latitude,
      "longitude": longitude,
    };
  }
}