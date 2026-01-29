import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/collection_model.dart';
import 'package:intl/intl.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'payment_screen.dart';

class CollectionDetailScreen extends StatelessWidget {
  final CollectionModel collection;

  const CollectionDetailScreen({Key? key, required this.collection}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final currencyFormat = NumberFormat.currency(locale: 'ru_RU', symbol: '₽', decimalDigits: 0);

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          SliverAppBar(
            expandedHeight: 400,
            pinned: true,
            stretch: true,
            backgroundColor: const Color(0xFF12141D),
            leading: IconButton(
              icon: Container(
                padding: const EdgeInsets.all(8),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.arrow_back, color: Color(0xFF12141D), size: 20),
              ),
              onPressed: () => Navigator.pop(context),
            ),
            flexibleSpace: FlexibleSpaceBar(
              stretchModes: const [StretchMode.zoomBackground],
              background: Hero(
                tag: 'collection_image_${collection.id}',
                child: collection.imageUrl != null
                    ? Image.network(collection.imageUrl!, fit: BoxFit.cover)
                    : Container(color: Colors.grey[300]),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Transform.translate(
              offset: const Offset(0, -40),
              child: Container(
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(45)),
                ),
                padding: const EdgeInsets.fromLTRB(24, 32, 24, 24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                      decoration: BoxDecoration(
                        color: const Color(0xFF00C853).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        'МЕЖДУНАРОДНЫЙ ПРОЕКТ',
                        style: GoogleFonts.manrope(
                          color: const Color(0xFF00C853),
                          fontSize: 10,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 1,
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      collection.title,
                      style: GoogleFonts.manrope(
                        fontSize: 32,
                        fontWeight: FontWeight.w900,
                        height: 1.1,
                        color: const Color(0xFF12141D),
                        letterSpacing: -1,
                      ),
                    ),
                    const SizedBox(height: 32),
                    // Stats Box
                    Container(
                      padding: const EdgeInsets.all(24),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF8F9FA),
                        borderRadius: BorderRadius.circular(35),
                      ),
                      child: Column(
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildBigStat('Собрано', currencyFormat.format(collection.raisedAmount), true, context),
                              _buildBigStat('Цель', currencyFormat.format(collection.goalAmount), false, context),
                            ],
                          ),
                          const SizedBox(height: 24),
                          LinearPercentIndicator(
                            lineHeight: 16.0,
                            percent: collection.progress,
                            backgroundColor: Colors.white,
                            progressColor: const Color(0xFF00C853),
                            barRadius: const Radius.circular(10),
                            animation: true,
                            animationDuration: 1000,
                            padding: EdgeInsets.zero,
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Прогресс сбора: ${(collection.progress * 100).toInt()}%',
                            style: GoogleFonts.manrope(
                              color: Colors.grey[600],
                              fontSize: 14,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 40),
                    Text(
                      'О проекте',
                      style: GoogleFonts.manrope(
                        fontSize: 24,
                        fontWeight: FontWeight.w800,
                        color: const Color(0xFF12141D),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      collection.description,
                      style: TextStyle(
                        fontSize: 17,
                        height: 1.8,
                        color: Colors.grey[800],
                        letterSpacing: 0.2,
                      ),
                    ),
                    const SizedBox(height: 40),
                    Text(
                      'Этапы реализации',
                      style: GoogleFonts.manrope(
                        fontSize: 24,
                        fontWeight: FontWeight.w800,
                        color: const Color(0xFF12141D),
                      ),
                    ),
                    const SizedBox(height: 24),
                    _buildTimelineStep(context, 'Сбор средств', 'В процессе', true, true),
                    _buildTimelineStep(context, 'Закупка материалов', 'Ожидание', false, true),
                    _buildTimelineStep(context, 'Начало работ', 'Ожидание', false, true),
                    _buildTimelineStep(context, 'Завершение и отчет', 'Ожидание', false, false),
                    const SizedBox(height: 40),
                    Text(
                      'Калькулятор помощи',
                      style: GoogleFonts.manrope(
                        fontSize: 24,
                        fontWeight: FontWeight.w800,
                        color: const Color(0xFF12141D),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(24),
                      decoration: BoxDecoration(
                        color: const Color(0xFF00C853).withOpacity(0.05),
                        borderRadius: BorderRadius.circular(35),
                        border: Border.all(color: const Color(0xFF00C853).withOpacity(0.1)),
                      ),
                      child: Column(
                        children: [
                          _buildImpactItem(Icons.restaurant_rounded, '1000 ₽', '15 горячих обедов'),
                          const Divider(height: 40, color: Color(0xFF00C853), thickness: 0.1),
                          _buildImpactItem(Icons.architecture_rounded, '5000 ₽', '50 кирпичей для школы'),
                          const Divider(height: 40, color: Color(0xFF00C853), thickness: 0.1),
                          _buildImpactItem(Icons.local_drink_rounded, '10000 ₽', 'Часть системы водоснабжения'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 140),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      bottomSheet: Container(
        padding: const EdgeInsets.fromLTRB(24, 20, 24, 40),
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF12141D).withOpacity(0.08),
              blurRadius: 30,
              offset: const Offset(0, -10),
            ),
          ],
        ),
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => PaymentScreen(collection: collection)),
            );
          },
          child: const Text('ПОДДЕРЖАТЬ ПРОЕКТ'),
        ),
      ),
    );
  }

  Widget _buildBigStat(String label, String value, bool highlight, BuildContext context) {
    return Column(
      crossAxisAlignment: highlight ? CrossAxisAlignment.start : CrossAxisAlignment.end,
      children: [
        Text(
          label,
          style: GoogleFonts.manrope(
            color: Colors.grey[500],
            fontSize: 14,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: GoogleFonts.manrope(
            fontSize: 22,
            fontWeight: FontWeight.w900,
            color: highlight ? const Color(0xFF00C853) : const Color(0xFF12141D),
          ),
        ),
      ],
    );
  }

  Widget _buildTimelineStep(BuildContext context, String title, String status, bool isActive, bool hasNext) {
    return Row(
      children: [
        Column(
          children: [
            Container(
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isActive ? const Color(0xFF00C853) : Colors.grey[200],
                border: Border.all(color: Colors.white, width: 4),
                boxShadow: isActive ? [BoxShadow(color: const Color(0xFF00C853).withOpacity(0.4), blurRadius: 10)] : [],
              ),
            ),
            if (hasNext)
              Container(
                width: 2,
                height: 50,
                color: isActive ? const Color(0xFF00C853) : Colors.grey[200],
              ),
          ],
        ),
        const SizedBox(width: 20),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: GoogleFonts.manrope(
                  fontWeight: FontWeight.w800,
                  fontSize: 16,
                  color: isActive ? const Color(0xFF12141D) : Colors.grey,
                ),
              ),
              Text(
                status,
                style: GoogleFonts.manrope(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: isActive ? const Color(0xFF00C853) : Colors.grey,
                ),
              ),
              if (hasNext) const SizedBox(height: 35),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildImpactItem(IconData icon, String amount, String result) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.white,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: const Color(0xFF00C853).withOpacity(0.1),
                blurRadius: 10,
              ),
            ],
          ),
          child: Icon(icon, color: const Color(0xFF00C853), size: 24),
        ),
        const SizedBox(width: 20),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                amount,
                style: GoogleFonts.manrope(
                  fontWeight: FontWeight.w900,
                  fontSize: 20,
                  color: const Color(0xFF12141D),
                ),
              ),
              Text(
                result,
                style: GoogleFonts.manrope(
                  color: Colors.grey[600],
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

