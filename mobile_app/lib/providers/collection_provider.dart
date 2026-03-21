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
      if (_collections.isEmpty) {
        _collections = _fallbackCollections();
      }
      if (_stories.isEmpty) {
        _stories = _fallbackStories();
      }
    } catch (e) {
      debugPrint('Error fetching collections: $e');
      // If it fails, try once more after 2 seconds
      await Future.delayed(const Duration(seconds: 2));
      try {
        _collections = await _apiService.getCollections();
        await fetchStories();
        if (_collections.isEmpty) {
          _collections = _fallbackCollections();
        }
        if (_stories.isEmpty) {
          _stories = _fallbackStories();
        }
      } catch (e2) {
        debugPrint('Second attempt failed: $e2');
        _collections = _fallbackCollections();
        _stories = _fallbackStories();
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> fetchStories() async {
    try {
      _stories = await _apiService.getStories();
      if (_stories.isEmpty) {
        _stories = _fallbackStories();
      }
      notifyListeners();
    } catch (e) {
      debugPrint('Error fetching stories: $e');
      _stories = _fallbackStories();
      notifyListeners();
    }
  }

  List<CollectionModel> _fallbackCollections() {
    final now = DateTime.now();
    return [
      CollectionModel(
        id: 'fallback-school',
        title: 'Школа в Мали',
        description:
            'Строительство школы для 300 детей. Проект включает учебные классы и базовую инфраструктуру.',
        goalAmount: 1500000,
        raisedAmount: 720000,
        imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image0.jpeg',
        images: const [
          'https://xn--80adnee0afc6kza.com/uploads/image0.jpeg',
          'https://xn--80adnee0afc6kza.com/uploads/image10.jpeg',
        ],
        category: 'Школы',
        status: 'active',
        createdAt: now,
      ),
      CollectionModel(
        id: 'fallback-water',
        title: 'Колодцы в Нигере',
        description:
            'Помощь с доступом к чистой воде. Планируется строительство 15 колодцев в сельских районах.',
        goalAmount: 900000,
        raisedAmount: 410000,
        imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image20.jpeg',
        images: const [
          'https://xn--80adnee0afc6kza.com/uploads/image20.jpeg',
        ],
        category: 'Вода',
        status: 'active',
        createdAt: now,
      ),
    ];
  }

  List<StoryModel> _fallbackStories() {
    return [
      StoryModel(
        id: 'fallback-story-1',
        title: 'Новый класс',
        imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image0.jpeg',
        caption: 'Открыли новый учебный класс для детей.',
      ),
      StoryModel(
        id: 'fallback-story-2',
        title: 'Чистая вода',
        imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image20.jpeg',
        caption: 'Еще одна деревня получила доступ к воде.',
      ),
    ];
  }
}




