import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/collection_provider.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CollectionProvider()),
      ],
      child: const CharityApp(),
    ),
  );
}

class CharityApp extends StatelessWidget {
  const CharityApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Charity App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: Colors.white,
        fontFamily: 'SF Pro Display', // standard iOS font, might need to add as asset
      ),
      home: const HomeScreen(),
    );
  }
}
