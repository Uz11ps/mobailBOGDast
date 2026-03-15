import 'package:flutter/material.dart';
import 'package:model_viewer_plus/model_viewer_plus.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';
// ignore: depend_on_referenced_packages
import 'package:webview_flutter_android/webview_flutter_android.dart';
// ignore: depend_on_referenced_packages
import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';
import 'dart:io' show Platform, Process, File, Directory;
import 'dart:convert' show Encoding, utf8;

class ImpactMapScreen extends StatefulWidget {
  const ImpactMapScreen({Key? key}) : super(key: key);

  @override
  State<ImpactMapScreen> createState() => _ImpactMapScreenState();
}

class _ImpactMapScreenState extends State<ImpactMapScreen> with TickerProviderStateMixin {
  bool _isProjectVisible = false;
  MapMarkerData? _selectedProject;
  bool _isWebViewInitialized = false;

  bool get _isSupported => kIsWeb || Platform.isAndroid || Platform.isIOS || Platform.isWindows;

  @override
  void initState() {
    super.initState();
    _ensureWebViewInitialized();
    _initWebView();
  }

  void _ensureWebViewInitialized() {
    if (!kIsWeb && WebViewPlatform.instance == null) {
      try {
        if (Platform.isIOS) {
          WebViewPlatform.instance = WebKitWebViewPlatform();
        } else if (Platform.isAndroid) {
          WebViewPlatform.instance = AndroidWebViewPlatform();
        }
        // На Windows webview_flutter автоматически использует webview_windows через плагин
      } catch (e) {
        debugPrint('WebView initialization error: $e');
      }
    }
  }

  Future<void> _initWebView() async {
    _ensureWebViewInitialized();
    // Для Windows даем больше времени на инициализацию плагина
    await Future.delayed(Duration(milliseconds: Platform.isWindows ? 1000 : 500));
    if (mounted) {
      setState(() {
        _isWebViewInitialized = true;
      });
    }
  }

  final List<MapMarkerData> _projects = [
    MapMarkerData(
      title: 'Школа в Мали',
      description: 'Построена современная школа на 300 мест. Дети получили доступ к качественному образованию.',
      imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image0.jpeg',
      category: 'Школы',
      location: 'Бамако, Мали',
      modelUrl: 'https://modelviewer.dev/shared-assets/models/Astronaut.glb', 
    ),
    MapMarkerData(
      title: 'Мечеть в Гвинее',
      description: 'Духовный центр для местной общины. Место для молитв и образования взрослых.',
      imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image10.jpeg',
      category: 'Мечети',
      location: 'Конакри, Гвинея',
      modelUrl: 'https://modelviewer.dev/shared-assets/models/Astronaut.glb',
    ),
    MapMarkerData(
      title: 'Колодцы в Нигере',
      description: '15 колодцев обеспечивают чистой питьевой водой более 5000 человек.',
      imageUrl: 'https://xn--80adnee0afc6kza.com/uploads/image20.jpeg',
      category: 'Вода',
      location: 'Диффа, Нигер',
      modelUrl: 'https://modelviewer.dev/shared-assets/models/Astronaut.glb',
    ),
  ];

  void _selectProject(MapMarkerData project) {
    setState(() {
      _selectedProject = project;
      _isProjectVisible = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!_isWebViewInitialized) {
      return const Scaffold(
        backgroundColor: Color(0xFF0A0B10),
        body: Center(
          child: CircularProgressIndicator(color: Color(0xFF00C853)),
        ),
      );
    }

    return Scaffold(
      backgroundColor: const Color(0xFF0A0B10),
      body: Stack(
        children: [
          // 3D EARTH GLOBE
          if (_isSupported)
            _buildModelViewer(
              'https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/Earth/glTF-Binary/Earth.glb',
              "3D Earth Globe",
              true,
            )
          else
            _buildUnsupportedView(),

          // Custom UI Overlay
          if (_isProjectVisible && _selectedProject != null)
            _buildProjectDetailView(),

          // Top Header
          _buildHeader(),

          // Bottom Project Selector
          if (!_isProjectVisible)
            _buildBottomSelector(),
        ],
      ),
    );
  }

  Widget _buildModelViewer(String src, String alt, bool autoRotate) {
    // Для Windows используем WebView с HTML, для других платформ - model_viewer_plus
    if (Platform.isWindows) {
      return _buildWebViewModelViewer(src, alt, autoRotate);
    }
    
    // Для Android/iOS используем model_viewer_plus если WebViewPlatform инициализирован
    _ensureWebViewInitialized();
    
    if (WebViewPlatform.instance == null) {
      return Container(
        color: const Color(0xFF0A0B10),
        child: const Center(
          child: CircularProgressIndicator(color: Color(0xFF00C853)),
        ),
      );
    }
    
    return ModelViewer(
      backgroundColor: const Color(0xFF0A0B10),
      src: src,
      alt: alt,
      autoRotate: autoRotate,
      cameraControls: true,
      shadowIntensity: 1,
      environmentImage: 'neutral',
      exposure: 1,
      poster: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800',
    );
  }

  Widget _buildWebViewModelViewer(String src, String alt, bool autoRotate) {
    return FutureBuilder<WebViewController?>(
      future: _createWebViewController(src, alt, autoRotate),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Container(
            color: const Color(0xFF0A0B10),
            child: const Center(
              child: CircularProgressIndicator(color: Color(0xFF00C853)),
            ),
          );
        }

        if (snapshot.hasError || snapshot.data == null) {
          debugPrint('Error creating WebView: ${snapshot.error}');
          return _buildFallbackViewer(src, alt, autoRotate);
        }

        return WebViewWidget(controller: snapshot.data!);
      },
    );
  }

  Widget _buildFallbackViewer(String src, String alt, bool autoRotate) {
    final htmlContent = _getHtmlContent(src, alt, autoRotate);
    
    return Container(
      color: const Color(0xFF0A0B10),
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 60),
              const Icon(Icons.language_rounded, color: Color(0xFF00C853), size: 80),
              const SizedBox(height: 20),
              Text(
                '3D Глобус Добра',
                style: GoogleFonts.manrope(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 15),
              Text(
                'Нажмите кнопку ниже,\nчтобы открыть 3D модель в браузере',
                textAlign: TextAlign.center,
                style: GoogleFonts.nunito(
                  color: Colors.white.withOpacity(0.7),
                  fontSize: 14,
                ),
              ),
              const SizedBox(height: 30),
              ElevatedButton.icon(
                onPressed: () async {
                  try {
                    if (Platform.isWindows) {
                      final tempDir = Directory.systemTemp;
                      final htmlFile = File('${tempDir.path}/model_viewer_${DateTime.now().millisecondsSinceEpoch}.html');
                      await htmlFile.writeAsString(htmlContent, encoding: utf8);
                      await Process.run(
                        'cmd',
                        ['/c', 'start', '', htmlFile.absolute.path],
                        runInShell: true,
                      );
                    }
                  } catch (e) {
                    debugPrint('Error launching browser: $e');
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(
                            'Не удалось открыть браузер.',
                            style: GoogleFonts.nunito(),
                          ),
                          backgroundColor: Colors.red,
                        ),
                      );
                    }
                  }
                },
                icon: const Icon(Icons.open_in_browser, size: 24),
                label: Text(
                  'ОТКРЫТЬ В БРАУЗЕРЕ',
                  style: GoogleFonts.manrope(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF00C853),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(25),
                  ),
                ),
              ),
              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }

  String _getHtmlContent(String src, String alt, bool autoRotate) {
    return '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>3D Model Viewer</title>
  <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.3.0/model-viewer.min.js"></script>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #0A0B10;
    }
    model-viewer {
      width: 100%;
      height: 100%;
      background-color: #0A0B10;
    }
  </style>
</head>
<body>
  <model-viewer
    src="$src"
    alt="$alt"
    ${autoRotate ? 'auto-rotate' : ''}
    camera-controls
    shadow-intensity="1"
    environment-image="neutral"
    exposure="1"
    poster="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800"
    style="width: 100%; height: 100%; background-color: #0A0B10;">
  </model-viewer>
</body>
</html>
    ''';
  }

  Future<WebViewController?> _createWebViewController(String src, String alt, bool autoRotate) async {
    final htmlContent = _getHtmlContent(src, alt, autoRotate);

    // На Windows создаем временный HTML файл и загружаем его через file://
    if (Platform.isWindows) {
      try {
        final tempDir = Directory.systemTemp;
        final htmlFile = File('${tempDir.path}/model_viewer_${DateTime.now().millisecondsSinceEpoch}.html');
        await htmlFile.writeAsString(htmlContent, encoding: utf8);
        await Future.delayed(const Duration(milliseconds: 200));
        
        // Пытаемся создать WebViewController с увеличивающимися задержками
        for (int i = 0; i < 5; i++) {
          try {
            await Future.delayed(Duration(milliseconds: 400 + (i * 200)));
            final controller = WebViewController()
              ..setJavaScriptMode(JavaScriptMode.unrestricted)
              ..setBackgroundColor(const Color(0xFF0A0B10))
              ..setNavigationDelegate(
                NavigationDelegate(
                  onPageFinished: (String url) {
                    debugPrint('Page finished loading: $url');
                  },
                  onWebResourceError: (WebResourceError error) {
                    debugPrint('WebView error: ${error.description}');
                  },
                ),
              )
              ..loadRequest(Uri.file(htmlFile.absolute.path));
            return controller;
          } catch (e) {
            debugPrint('Windows attempt ${i + 1} failed: $e');
            if (i == 4) {
              // Последняя попытка - пробуем data URI
              try {
                final controller = WebViewController()
                  ..setJavaScriptMode(JavaScriptMode.unrestricted)
                  ..setBackgroundColor(const Color(0xFF0A0B10))
                  ..setNavigationDelegate(
                    NavigationDelegate(
                      onPageFinished: (String url) {
                        debugPrint('Page finished loading: $url');
                      },
                      onWebResourceError: (WebResourceError error) {
                        debugPrint('WebView error: ${error.description}');
                      },
                    ),
                  )
                  ..loadRequest(
                    Uri.dataFromString(
                      htmlContent,
                      mimeType: 'text/html',
                      encoding: Encoding.getByName('utf-8'),
                    ),
                  );
                return controller;
              } catch (e2) {
                debugPrint('Data URI also failed: $e2');
                return null;
              }
            }
          }
        }
        return null;
      } catch (e) {
        debugPrint('Error creating HTML file: $e');
        return null;
      }
    }

    // Для других платформ
    try {
      await Future.delayed(const Duration(milliseconds: 300));
      final controller = WebViewController()
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..setBackgroundColor(const Color(0xFF0A0B10))
        ..setNavigationDelegate(
          NavigationDelegate(
            onPageFinished: (String url) {
              debugPrint('Page finished loading: $url');
            },
            onWebResourceError: (WebResourceError error) {
              debugPrint('WebView error: ${error.description}');
            },
          ),
        )
        ..loadRequest(
          Uri.dataFromString(
            htmlContent,
            mimeType: 'text/html',
            encoding: Encoding.getByName('utf-8'),
          ),
        );
      return controller;
    } catch (e) {
      debugPrint('Error creating WebViewController: $e');
      return null;
    }
  }

  Widget _buildHeader() {
    return Positioned(
      top: 60,
      left: 20,
      right: 20,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          borderRadius: BorderRadius.circular(25),
          border: Border.all(color: Colors.white.withOpacity(0.1)),
        ),
        child: Row(
          children: [
            const Icon(Icons.language_rounded, color: Color(0xFF00C853), size: 28),
            const SizedBox(width: 15),
            Text(
              'AR Глобус Добра',
              style: GoogleFonts.manrope(
                fontSize: 18,
                fontWeight: FontWeight.w900,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ).animate().fadeIn().slideY(begin: -1),
    );
  }

  Widget _buildBottomSelector() {
    return Positioned(
      bottom: 120,
      left: 0,
      right: 0,
      child: SizedBox(
        height: 80,
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 20),
          itemCount: _projects.length,
          itemBuilder: (context, index) {
            final p = _projects[index];
            return GestureDetector(
              onTap: () => _selectProject(p),
              child: Container(
                margin: const EdgeInsets.only(right: 15),
                padding: const EdgeInsets.symmetric(horizontal: 20),
                decoration: BoxDecoration(
                  color: const Color(0xFF1F2232),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.white.withOpacity(0.1)),
                ),
                child: Center(
                  child: Text(
                    p.location,
                    style: GoogleFonts.manrope(
                      color: Colors.white,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
              ),
            ).animate().fadeIn(delay: (index * 100).ms).slideX(begin: 0.5);
          },
        ),
      ),
    );
  }

  Widget _buildProjectDetailView() {
    return Positioned.fill(
      child: Container(
        color: Colors.black.withOpacity(0.85),
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 40),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SizedBox(
                  height: 300,
                  width: double.infinity,
                  child: _buildModelViewer(
                    _selectedProject!.modelUrl,
                    "Project Model",
                    true,
                  ),
                ).animate().scale(duration: 800.ms, curve: Curves.elasticOut).fadeIn(),
                
                const SizedBox(height: 40),
                
                Container(
                  margin: const EdgeInsets.symmetric(horizontal: 30),
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1F2232),
                    borderRadius: BorderRadius.circular(30),
                    border: Border.all(color: Colors.white.withOpacity(0.1)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        _selectedProject!.category.toUpperCase(),
                        style: GoogleFonts.manrope(
                          color: const Color(0xFF00C853),
                          fontSize: 10,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        _selectedProject!.title,
                        style: GoogleFonts.manrope(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        _selectedProject!.description,
                        style: GoogleFonts.nunito(
                          color: Colors.white.withOpacity(0.7),
                          fontSize: 14,
                        ),
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: () => setState(() => _isProjectVisible = false),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00C853),
                          minimumSize: const Size(double.infinity, 55),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                        ),
                        child: const Text('ВЕРНУТЬСЯ К ГЛОБУСУ'),
                      ),
                    ],
                  ),
                ).animate().slideY(begin: 0.5, duration: 600.ms),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildUnsupportedView() {
    return Container(
      color: const Color(0xFF0A0B10),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.language_rounded, color: Color(0xFF00C853), size: 100),
            const SizedBox(height: 20),
            Text(
              '3D Глобус не поддерживается\nна этом устройстве',
              textAlign: TextAlign.center,
              style: GoogleFonts.manrope(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }
}

class MapMarkerData {
  final String title;
  final String description;
  final String imageUrl;
  final String category;
  final String location;
  final String modelUrl;

  MapMarkerData({
    required this.title,
    required this.description,
    required this.imageUrl,
    required this.category,
    required this.location,
    required this.modelUrl,
  });
}
