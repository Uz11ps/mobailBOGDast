import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';

class CustomBottomBar extends StatelessWidget {
  final int currentIndex;
  final Function(int) onTap;

  const CustomBottomBar({Key? key, required this.currentIndex, required this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 90,
      margin: const EdgeInsets.fromLTRB(24, 0, 24, 30),
      decoration: BoxDecoration(
        color: const Color(0xFF12141D),
        borderRadius: BorderRadius.circular(35),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF12141D).withOpacity(0.3),
            blurRadius: 30,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildItem(0, Icons.home_rounded, "Главная"),
          _buildItem(1, Icons.public_rounded, "Карта"),
          _buildCenterItem(),
          _buildItem(3, Icons.eco_rounded, "Вклад"),
          _buildItem(4, Icons.person_rounded, "Профиль"),
        ],
      ),
    );
  }

  Widget _buildItem(int index, IconData icon, String label) {
    final isSelected = currentIndex == index;
    return GestureDetector(
      onTap: () => onTap(index),
      behavior: HitTestBehavior.opaque,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            icon,
            color: isSelected ? const Color(0xFF00C853) : Colors.white.withOpacity(0.5),
            size: 24,
          ).animate(target: isSelected ? 1 : 0).scale(begin: const Offset(1, 1), end: const Offset(1.2, 1.2)),
          const SizedBox(height: 4),
          Text(
            label,
            style: GoogleFonts.manrope(
              color: isSelected ? const Color(0xFF00C853) : Colors.white.withOpacity(0.5),
              fontSize: 9,
              fontWeight: FontWeight.w800,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCenterItem() {
    return GestureDetector(
      onTap: () => onTap(2), // Index 2 for the heart button (center)
      child: Container(
        height: 55,
        width: 55,
        decoration: BoxDecoration(
          color: const Color(0xFF00C853),
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF00C853).withOpacity(0.4),
              blurRadius: 15,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: const Icon(Icons.favorite_rounded, color: Colors.white, size: 28),
      ).animate(onPlay: (controller) => controller.repeat(reverse: true))
       .scale(begin: const Offset(1, 1), end: const Offset(1.1, 1.1), duration: 1000.ms, curve: Curves.easeInOut),
    );
  }
}
