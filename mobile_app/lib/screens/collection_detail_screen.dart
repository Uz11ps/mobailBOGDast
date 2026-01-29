import 'package:flutter/material.dart';
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
            expandedHeight: 350,
            pinned: true,
            stretch: true,
            backgroundColor: Theme.of(context).primaryColor,
            leading: IconButton(
              icon: Container(
                padding: const EdgeInsets.all(8),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.arrow_back, color: Colors.black, size: 20),
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
              offset: const Offset(0, -30),
              child: Container(
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
                ),
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.flash_on_rounded, size: 14, color: Theme.of(context).primaryColor),
                          const SizedBox(width: 4),
                          Text(
                            'ВАЖНЫЙ СБОР',
                            style: TextStyle(
                              color: Theme.of(context).primaryColor,
                              fontSize: 10,
                              fontWeight: FontWeight.w900,
                              letterSpacing: 1,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      collection.title,
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.w900,
                        height: 1.2,
                        letterSpacing: -0.5,
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF8F9FA),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Column(
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text('Собрано', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
                                  Text(
                                    currencyFormat.format(collection.raisedAmount),
                                    style: TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                      color: Theme.of(context).primaryColor,
                                    ),
                                  ),
                                ],
                              ),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.end,
                                children: [
                                  Text('Цель', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
                                  Text(
                                    currencyFormat.format(collection.goalAmount),
                                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          LinearPercentIndicator(
                            lineHeight: 14.0,
                            percent: collection.progress,
                            backgroundColor: Colors.white,
                            progressColor: Theme.of(context).primaryColor,
                            barRadius: const Radius.circular(10),
                            animation: true,
                            animationDuration: 1000,
                            padding: EdgeInsets.zero,
                          ),
                          const SizedBox(height: 12),
                          Text(
                            '${(collection.progress * 100).toInt()}% от цели достигнуто',
                            style: TextStyle(color: Colors.grey[600], fontSize: 12, fontWeight: FontWeight.w500),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 32),
                    const Text(
                      'История сбора',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      collection.description,
                      style: TextStyle(
                        fontSize: 16,
                        height: 1.7,
                        color: Colors.grey[800],
                      ),
                    ),
                    const SizedBox(height: 32),
                    const Text(
                      'Этапы реализации',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    _buildTimelineStep(context, 'Сбор средств', 'В процессе', true, true),
                    _buildTimelineStep(context, 'Закупка материалов', 'Ожидание', false, true),
                    _buildTimelineStep(context, 'Начало работ', 'Ожидание', false, true),
                    _buildTimelineStep(context, 'Завершение и отчет', 'Ожидание', false, false),
                    const SizedBox(height: 32),
                    const Text(
                      'Калькулятор помощи',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor.withOpacity(0.05),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: Theme.of(context).primaryColor.withOpacity(0.1)),
                      ),
                      child: Column(
                        children: [
                          _buildImpactItem(Icons.restaurant, '1000 ₽', '15 горячих обедов'),
                          const Divider(height: 30),
                          _buildImpactItem(Icons.architecture, '5000 ₽', '50 кирпичей для школы'),
                          const Divider(height: 30),
                          _buildImpactItem(Icons.local_drink, '10000 ₽', 'Часть системы водоснабжения'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 120),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      bottomSheet: Container(
        padding: const EdgeInsets.fromLTRB(24, 16, 24, 32),
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 20,
              offset: const Offset(0, -5),
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
          style: ElevatedButton.styleFrom(
            backgroundColor: Theme.of(context).primaryColor,
            foregroundColor: Colors.white,
            minimumSize: const Size(double.infinity, 64),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            elevation: 0,
          ),
          child: const Text(
            'Поддержать проект',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }

  Widget _buildTimelineStep(BuildContext context, String title, String status, bool isActive, bool hasNext) {
    return Row(
      children: [
        Column(
          children: [
            Container(
              width: 20,
              height: 20,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isActive ? Theme.of(context).primaryColor : Colors.grey[300],
                border: Border.all(color: Colors.white, width: 3),
                boxShadow: isActive ? [BoxShadow(color: Theme.of(context).primaryColor.withOpacity(0.4), blurRadius: 8)] : [],
              ),
            ),
            if (hasNext)
              Container(
                width: 2,
                height: 40,
                color: isActive ? Theme.of(context).primaryColor : Colors.grey[300],
              ),
          ],
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: isActive ? Colors.black : Colors.grey)),
              Text(status, style: TextStyle(fontSize: 12, color: isActive ? Theme.of(context).primaryColor : Colors.grey)),
              if (hasNext) const SizedBox(height: 25),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildImpactItem(IconData icon, String amount, String result) {
    return Row(
      children: [
        Icon(icon, color: const Color(0xFF00C853)),
        const SizedBox(width: 15),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(amount, style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
              Text(result, style: const TextStyle(color: Colors.grey, fontSize: 13)),
            ],
          ),
        ),
      ],
    );
  }
}

