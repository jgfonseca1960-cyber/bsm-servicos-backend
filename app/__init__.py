Future<void> _init() async {
  await obterLocalizacao();

  await Future.wait([
    carregarEmpresas(),
    carregarUsuario(),
    carregarServicos(),
  ]);
}