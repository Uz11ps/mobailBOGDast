import 'package:flutter/material.dart';
import '../models/collection_model.dart';
import '../services/api_service.dart';

class CollectionProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<CollectionModel> _collections = [];
  bool _isLoading = false;

  List<CollectionModel> get collections => _collections;
  bool get isLoading => _isLoading;

  Future<void> fetchCollections() async {
    _isLoading = true;
    notifyListeners();
    try {
      _collections = await _apiService.getCollections();
    } catch (e) {
      print(e);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}




