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