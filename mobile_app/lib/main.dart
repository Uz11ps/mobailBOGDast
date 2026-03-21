import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'providers/collection_provider.dart';
import 'screens/home_screen.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:webview_flutter_android/webview_flutter_android.dart';
import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Инициализация WebView платформы при запуске приложения
  if (!kIsWeb && WebViewPlatform.instance == null) {
    try {
      if (Platform.isAndroid) {
        WebViewPlatform.instance = AndroidWebViewPlatform();
      } else if (Platform.isIOS) {
        WebViewPlatform.instance = WebKitWebViewPlatform();
      }
      // На Windows webview_flutter автоматически использует webview_windows через плагин
      // Даем время на инициализацию плагина
      if (Platform.isWindows) {
        await Future.delayed(const Duration(milliseconds: 500));
      }
    } catch (e) {
      debugPrint('WebView initialization error: $e');
    }
  }

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
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00C853),
          primary: const Color(0xFF00C853),
          secondary: const Color(0xFFFFD600),
          surface: Colors.white,
          onSurface: const Color(0xFF12141D),
        ),
        scaffoldBackgroundColor: const Color(0xFFF8F9FA),
        textTheme: GoogleFonts.nunitoTextTheme(
          Theme.of(context).textTheme,
        ).copyWith(
          displayLarge: GoogleFonts.manrope(
            fontWeight: FontWeight.w900,
            color: const Color(0xFF12141D),
            letterSpacing: -2,
          ),
          displayMedium: GoogleFonts.manrope(
            fontWeight: FontWeight.w900,
            color: const Color(0xFF12141D),
            letterSpacing: -1,
          ),
          headlineMedium: GoogleFonts.manrope(
            fontWeight: FontWeight.w800,
            color: const Color(0xFF12141D),
            letterSpacing: -0.5,
          ),
          titleLarge: GoogleFonts.manrope(
            fontWeight: FontWeight.w800,
            color: const Color(0xFF12141D),
          ),
        ),
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.white,
          elevation: 0,
          scrolledUnderElevation: 0,
          centerTitle: false,
          titleTextStyle: GoogleFonts.manrope(
            color: const Color(0xFF12141D),
            fontSize: 24,
            fontWeight: FontWeight.w900,
            letterSpacing: -0.5,
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF12141D),
            foregroundColor: Colors.white,
            minimumSize: const Size(double.infinity, 60),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
            textStyle: GoogleFonts.manrope(
              fontWeight: FontWeight.w800,
              fontSize: 16,
            ),
          ),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
