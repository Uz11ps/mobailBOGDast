import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/collection_model.dart';
import '../models/user_model.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Используем домен в формате Punycode (новаяжизнь.com)
  static const String baseUrl = 'http://xn--80adfb7ajbc4as6e.com/api'; 

  Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('token');
  }

  Future<List<CollectionModel>> getCollections() async {
    final response = await http.get(Uri.parse('$baseUrl/collections'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => CollectionModel.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load collections');
    }
  }

  Future<Map<String, dynamic>> login(String phone) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'phone': phone}),
    );
    if (response.statusCode == 200) {
      final result = json.decode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', result['token']);
      return result;
    } else {
      throw Exception('Login failed');
    }
  }

  Future<UserModel> getProfile() async {
    final token = await _getToken();
    final response = await http.get(
      Uri.parse('$baseUrl/auth/profile'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );
    if (response.statusCode == 200) {
      return UserModel.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load profile');
    }
  }
}

