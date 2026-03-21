import 'package:flutter/material.dart';
import 'package:story_view/story_view.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../models/story_model.dart';

class StoryScreen extends StatefulWidget {
  final List<StoryModel> stories;
  final int initialIndex;
  const StoryScreen({Key? key, required this.stories, this.initialIndex = 0}) : super(key: key);

  @override
  State<StoryScreen> createState() => _StoryScreenState();
}

class _StoryScreenState extends State<StoryScreen> {
  final StoryController controller = StoryController();
  bool isLiked = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          StoryView(
            storyItems: widget.stories.map((s) {
              return StoryItem.pageImage(
                url: s.imageUrl,
                caption: Text(
                  s.caption ?? s.title,
                  style: GoogleFonts.nunito(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                ),
                controller: controller,
              );
            }).toList(),
            onStoryShow: (s, index) {},
            onComplete: () => Navigator.pop(context),
            progressPosition: ProgressPosition.top,
            repeat: false,
            controller: controller,
          ),
          // Custom Overlay for Likes and Close
          Positioned(
            top: 60,
            right: 20,
            child: IconButton(
              icon: const Icon(Icons.close_rounded, color: Colors.white, size: 32),
              onPressed: () => Navigator.pop(context),
            ),
          ),
          Positioned(
            bottom: 50,
            right: 20,
            child: GestureDetector(
              onTap: () {
                setState(() => isLiked = !isLiked);
              },
              child: Icon(
                isLiked ? Icons.favorite_rounded : Icons.favorite_border_rounded,
                color: isLiked ? const Color(0xFF00C853) : Colors.white,
                size: 45,
              ).animate(target: isLiked ? 1 : 0)
               .scale(begin: const Offset(1, 1), end: const Offset(1.3, 1.2))
               .then()
               .scale(begin: const Offset(1.3, 1.2), end: const Offset(1, 1)),
            ),
          ),
        ],
      ),
    );
  }
}
