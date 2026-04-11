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
  late Future<List<Empresa>> empresas;

  @override
  void initState() {
    super.initState();
    empresas = ApiService.getEmpresas();
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

      body: FutureBuilder<List<Empresa>>(
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

            return const Center(
              child: Text("Erro ao carregar empresas"),
            );
          }

          final list = snapshot.data ?? [];

          if (list.isEmpty) {
            return const Center(
              child: Text("Nenhuma empresa cadastrada"),
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
                  onTap: () async {
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
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';

import '../services/api_service.dart';
import '../models/empresa.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  GoogleMapController? mapController;

  LatLng? userLocation;
  final Set<Marker> markers = {};

  @override
  void initState() {
    super.initState();
    _initMap();
  }

  Future<void> _initMap() async {
    await _getUserLocation();
    await _loadEmpresas();
  }

  Future<void> _getUserLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return;

    LocationPermission permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.denied) return;

    final position = await Geolocator.getCurrentPosition();

    setState(() {
      userLocation = LatLng(position.latitude, position.longitude);
    });
  }

  Future<void> _loadEmpresas() async {
    final List<Empresa> empresas = await ApiService.getEmpresas();

    final Set<Marker> newMarkers = {};

    for (final e in empresas) {
      if (e.latitude == null || e.longitude == null) continue;

      newMarkers.add(
        Marker(
          markerId: MarkerId(e.id.toString()),
          position: LatLng(e.latitude!, e.longitude!),
          infoWindow: InfoWindow(
            title: e.nome,
            snippet: e.telefone ?? '',
          ),
          onTap: () {
            _showEmpresa(e);
          },
        ),
      );
    }

    setState(() {
      markers.addAll(newMarkers);
    });
  }

  void _showEmpresa(Empresa empresa) {
    showModalBottomSheet(
      context: context,
      builder: (_) {
        return Container(
          padding: const EdgeInsets.all(16),
          height: 220,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                empresa.nome,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 10),
              Text("📞 ${empresa.telefone ?? ''}"),
              Text("✉️ ${empresa.email ?? ''}"),
              Text("📍 ${empresa.endereco ?? ''}"),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Empresas próximas"),
      ),

      body: userLocation == null
          ? const Center(child: CircularProgressIndicator())
          : GoogleMap(
              initialCameraPosition: CameraPosition(
                target: userLocation!,
                zoom: 14,
              ),
              markers: markers,
              myLocationEnabled: true,
              myLocationButtonEnabled: true,
              onMapCreated: (controller) {
                mapController = controller;
              },
            ),
    );
  }
}