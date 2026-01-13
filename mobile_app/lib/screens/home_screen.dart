import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/collection_provider.dart';
import '../widgets/collection_card.dart';
import 'collection_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
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
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('Сборы', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
      ),
      body: Consumer<CollectionProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (provider.collections.isEmpty) {
            return const Center(child: Text('Нет активных сборов'));
          }

          return RefreshIndicator(
            onRefresh: provider.fetchCollections,
            child: ListView.builder(
              itemCount: provider.collections.length,
              itemBuilder: (context, index) {
                final collection = provider.collections[index];
                return CollectionCard(
                  collection: collection,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CollectionDetailScreen(collection: collection),
                      ),
                    );
                  },
                );
              },
            ),
          );
        },
      ),
    );
  }
}

