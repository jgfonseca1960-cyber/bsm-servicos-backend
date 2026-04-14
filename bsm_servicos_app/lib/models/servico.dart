class Servico {
  final int id;
  final String nome;

  Servico({
    required this.id,
    required this.nome,
  });

  factory Servico.fromJson(Map<String, dynamic> json) {
    return Servico(
      id: json['id'],
      nome: json['nome'],
    );
  }
}