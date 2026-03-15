import 'package:flutter/material.dart';
import 'dart:math' as math;
import 'package:provider/provider.dart';
import 'package:shimmer/shimmer.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../providers/collection_provider.dart';
import '../widgets/collection_card.dart';
import '../widgets/custom_bottom_bar.dart';
import 'collection_detail_screen.dart';
import 'profile_screen.dart';
import 'story_screen.dart';
import 'impact_map_screen.dart';
import 'my_impact_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _selectedCategory = 'Все';
  final List<String> _categories = ['Все', 'Школы', 'Мечети', 'Питание', 'Срочно'];
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<CollectionProvider>().fetchCollections();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      body: IndexedStack(
        index: _currentIndex,
        children: [
          _buildHomeContent(),
          const ImpactMapScreen(),
          _buildHomeContent(), // Center heart button also shows home for now
          const MyImpactScreen(),
          const ProfileScreen(),
        ],
      ),
      bottomNavigationBar: CustomBottomBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
        },
      ),
      extendBody: true,
    );
  }

  Widget _buildHomeContent() {
    return Consumer<CollectionProvider>(
      builder: (context, provider, child) {
        return CustomScrollView(
          physics: const BouncingScrollPhysics(),
          slivers: [
            SliverAppBar(
              floating: true,
              snap: true,
              expandedHeight: 120,
              backgroundColor: Colors.white,
              surfaceTintColor: Colors.transparent,
              title: Padding(
                padding: const EdgeInsets.only(top: 10),
                child: Row(
                  children: [
                    Image.asset(
                      'assets/logo.png',
                      width: 40,
                      height: 40,
                      fit: BoxFit.contain,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'НОВАЯ ЖИЗНЬ',
                            style: GoogleFonts.manrope(
                              color: const Color(0xFF12141D),
                              fontSize: 24,
                              fontWeight: FontWeight.w900,
                              letterSpacing: -1,
                            ),
                          ).animate().fadeIn(duration: 600.ms).slideX(begin: -0.2),
                          Text(
                            'Помогать легко ✨',
                            style: TextStyle(
                              color: Colors.grey[600],
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                            ),
                          ).animate().fadeIn(delay: 200.ms, duration: 600.ms),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
                actions: [
                  Container(
                    margin: const EdgeInsets.only(right: 16),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF8F9FA),
                      shape: BoxShape.circle,
                    ),
                    child: IconButton(
                      icon: const Icon(Icons.search_rounded, color: Color(0xFF12141D)),
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Поиск пока в разработке')),
                        );
                      },
                    ),
                  ),
                ],
            ),
            // Stories Section
            SliverToBoxAdapter(
              child: Container(
                height: 120,
                margin: const EdgeInsets.symmetric(vertical: 10),
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: provider.stories.length,
                  itemBuilder: (context, index) {
                    final story = provider.stories[index];
                    return Padding(
                      padding: const EdgeInsets.only(right: 18),
                      child: GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => StoryScreen(
                                stories: provider.stories,
                                initialIndex: index,
                              ),
                            ),
                          );
                        },
                        child: Column(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(3),
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                gradient: const LinearGradient(
                                  colors: [Color(0xFF00C853), Color(0xFFFFD600)],
                                  begin: Alignment.topLeft,
                                  end: Alignment.bottomRight,
                                ),
                              ),
                              child: Container(
                                padding: const EdgeInsets.all(2),
                                decoration: const BoxDecoration(
                                  color: Colors.white,
                                  shape: BoxShape.circle,
                                ),
                                child: CircleAvatar(
                                  radius: 32,
                                  backgroundImage: NetworkImage(story.imageUrl),
                                ),
                              ),
                            ).animate().scale(delay: (index * 100).ms, duration: 400.ms, curve: Curves.easeOutBack),
                            const SizedBox(height: 8),
                            Text(
                              story.title,
                              style: GoogleFonts.nunito(
                                fontSize: 11,
                                fontWeight: FontWeight.w800,
                                color: const Color(0xFF12141D),
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
            // Impact Banner
            SliverToBoxAdapter(
              child: Container(
                margin: const EdgeInsets.all(16),
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: const Color(0xFF12141D),
                  borderRadius: BorderRadius.circular(32),
                  image: DecorationImage(
                    image: const NetworkImage('https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800'),
                    fit: BoxFit.cover,
                    opacity: 0.3,
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: const Color(0xFF00C853),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        'ИТОГИ МЕСЯЦА',
                        style: GoogleFonts.manrope(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Вместе мы собрали\n3 359 255 ₽',
                      style: GoogleFonts.manrope(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.w900,
                        height: 1.1,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Это 15 построенных колодцев и 2 школы в Гвинее',
                      style: TextStyle(
                        color: Colors.white.withOpacity(0.7),
                        fontSize: 13,
                      ),
                    ),
                  ],
                ),
              ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.2),
            ),
            // Category Filter Bar
            SliverPersistentHeader(
              pinned: true,
              delegate: _SliverAppBarDelegate(
                minHeight: 60.0,
                maxHeight: 60.0,
                child: Container(
                  color: const Color(0xFFF8F9FA),
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                    itemCount: _categories.length,
                    itemBuilder: (context, index) {
                      final category = _categories[index];
                      final isSelected = _selectedCategory == category;
                      return Padding(
                        padding: const EdgeInsets.only(right: 10),
                        child: InkWell(
                          onTap: () => setState(() => _selectedCategory = category),
                          borderRadius: BorderRadius.circular(18),
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 300),
                            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                            decoration: BoxDecoration(
                              color: isSelected ? const Color(0xFF12141D) : Colors.white,
                              borderRadius: BorderRadius.circular(18),
                              border: Border.all(
                                color: isSelected ? const Color(0xFF12141D) : Colors.grey[200]!,
                                width: 1,
                              ),
                            ),
                            child: Text(
                              category,
                              style: GoogleFonts.manrope(
                                color: isSelected ? Colors.white : const Color(0xFF12141D),
                                fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),
            ),
            if (provider.isLoading)
              SliverPadding(
                padding: const EdgeInsets.all(16),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (context, index) => _buildShimmerCard(),
                    childCount: 3,
                  ),
                ),
              )
            else if (provider.collections.isEmpty)
              SliverFillRemaining(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.wifi_off_rounded, size: 60, color: Colors.grey),
                      const SizedBox(height: 16),
                      const Text('Не удалось загрузить данные', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      TextButton(
                        onPressed: () => provider.fetchCollections(),
                        child: const Text('ПОПРОБОВАТЬ СНОВА', style: TextStyle(color: Color(0xFF00C853))),
                      ),
                    ],
                  ),
                ),
              )
            else
              SliverPadding(
                padding: const EdgeInsets.only(top: 10, bottom: 120),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (context, index) {
                      final collection = provider.collections[index];
                      return CollectionCard(
                        collection: collection,
                        onTap: () {
                          Navigator.push(
                            context,
                            PageRouteBuilder(
                              transitionDuration: const Duration(milliseconds: 600),
                              pageBuilder: (context, animation, secondaryAnimation) => 
                                CollectionDetailScreen(collection: collection),
                              transitionsBuilder: (context, animation, secondaryAnimation, child) {
                                return FadeTransition(opacity: animation, child: child);
                              },
                            ),
                          );
                        },
                      ).animate().fadeIn(delay: (index * 100).ms).slideY(begin: 0.1);
                    },
                    childCount: provider.collections.length,
                  ),
                ),
              ),
          ],
        );
      },
    );
  }

  Widget _buildShimmerCard() {
    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      height: 300,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Shimmer.fromColors(
        baseColor: Colors.grey[300]!,
        highlightColor: Colors.grey[100]!,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: 200,
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(height: 20, width: 200, color: Colors.white),
                  const SizedBox(height: 10),
                  Container(height: 10, width: double.infinity, color: Colors.white),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SliverAppBarDelegate extends SliverPersistentHeaderDelegate {
  _SliverAppBarDelegate({
    required this.minHeight,
    required this.maxHeight,
    required this.child,
  });
  final double minHeight;
  final double maxHeight;
  final Widget child;

  @override
  double get minExtent => minHeight;
  @override
  double get maxExtent => math.max(maxHeight, minHeight);

  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    return SizedBox.expand(child: child);
  }

  @override
  bool shouldRebuild(_SliverAppBarDelegate oldDelegate) {
    return maxHeight != oldDelegate.maxHeight ||
        minHeight != oldDelegate.minHeight ||
        child != oldDelegate.child;
  }
}
