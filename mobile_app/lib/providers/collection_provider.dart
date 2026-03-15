import 'package:flutter/material.dart';
import '../models/collection_model.dart';
import '../models/story_model.dart';
import '../services/api_service.dart';

class CollectionProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<CollectionModel> _collections = [];
  List<StoryModel> _stories = [];
  bool _isLoading = false;

  List<CollectionModel> get collections => _collections;
  List<StoryModel> get stories => _stories;
  bool get isLoading => _isLoading;

  Future<void> fetchCollections() async {
    _isLoading = true;
    notifyListeners();
    try {
      _collections = await _apiService.getCollections();
      await fetchStories();
    } catch (e) {
      debugPrint('Error fetching collections: $e');
      // If it fails, try once more after 2 seconds
      await Future.delayed(const Duration(seconds: 2));
      try {
        _collections = await _apiService.getCollections();
        await fetchStories();
      } catch (e2) {
        debugPrint('Second attempt failed: $e2');
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> fetchStories() async {
    try {
      _stories = await _apiService.getStories();
      notifyListeners();
    } catch (e) {
      debugPrint('Error fetching stories: $e');
    }
  }
}




