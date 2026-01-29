class CollectionModel {
  final String id;
  final String title;
  final String description;
  final double goalAmount;
  final double raisedAmount;
  final String? imageUrl;
  final String? category;
  final String status;
  final DateTime createdAt;

  CollectionModel({
    required this.id,
    required this.title,
    required this.description,
    required this.goalAmount,
    required this.raisedAmount,
    this.imageUrl,
    this.category,
    required this.status,
    required this.createdAt,
  });

  factory CollectionModel.fromJson(Map<String, dynamic> json) {
    return CollectionModel(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      goalAmount: double.parse(json['goalAmount'].toString()),
      raisedAmount: double.parse(json['raisedAmount'].toString()),
      imageUrl: json['imageUrl'],
      category: json['category'],
      status: json['status'],
      createdAt: DateTime.parse(json['createdAt']),
    );
  }

  double get progress => raisedAmount / goalAmount;
}




