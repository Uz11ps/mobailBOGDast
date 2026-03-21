class StoryModel {
  final String id;
  final String title;
  final String imageUrl;
  final String? caption;

  StoryModel({
    required this.id,
    required this.title,
    required this.imageUrl,
    this.caption,
  });

  factory StoryModel.fromJson(Map<String, dynamic> json) {
    return StoryModel(
      id: json['id'],
      title: json['title'],
      imageUrl: json['imageUrl'],
      caption: json['caption'],
    );
  }
}
