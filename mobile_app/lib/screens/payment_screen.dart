import 'package:flutter/material.dart';
import '../models/collection_model.dart';
import '../services/api_service.dart';

class PaymentScreen extends StatefulWidget {
  final CollectionModel collection;

  const PaymentScreen({Key? key, required this.collection}) : super(key: key);

  @override
  State<PaymentScreen> createState() => _PaymentScreenState();
}

class _PaymentScreenState extends State<PaymentScreen> {
  final List<int> _amounts = [100, 500, 1000, 5000];
  int _selectedAmount = 500;
  final TextEditingController _customAmountController = TextEditingController();
  bool _isProcessing = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Пожертвование'),
        elevation: 0,
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Выберите сумму для "${widget.collection.title}"',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 2.5,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
              ),
              itemCount: _amounts.length,
              itemBuilder: (context, index) {
                final amount = _amounts[index];
                final isSelected = _selectedAmount == amount;
                return ChoiceChip(
                  label: Container(
                    width: double.infinity,
                    alignment: Alignment.center,
                    child: Text('$amount ₽', style: TextStyle(
                      color: isSelected ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    )),
                  ),
                  selected: isSelected,
                  selectedColor: Colors.green,
                  backgroundColor: Colors.grey[100],
                  onSelected: (selected) {
                    setState(() {
                      _selectedAmount = amount;
                      _customAmountController.clear();
                    });
                  },
                );
              },
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _customAmountController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                hintText: 'Другая сумма',
                filled: true,
                fillColor: Colors.grey[100],
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  setState(() {
                    _selectedAmount = int.tryParse(value) ?? 0;
                  });
                }
              },
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: _isProcessing ? null : _processPayment,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                minimumSize: const Size(double.infinity, 56),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              ),
              child: _isProcessing
                  ? const CircularProgressIndicator(color: Colors.white)
                  : Text('Оплатить $_selectedAmount ₽', style: const TextStyle(fontSize: 18, color: Colors.white)),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Future<void> _processPayment() async {
    setState(() => _isProcessing = true);
    
    try {
      // 1. Create intent
      // 2. Mock payment gateway
      // 3. Confirm payment
      
      // For now we just simulate a delay
      await Future.delayed(const Duration(seconds: 2));
      
      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Спасибо!'),
            content: const Text('Ваше пожертвование успешно принято.'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                },
                child: const Text('ОК'),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Ошибка при оплате')),
      );
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }
}

