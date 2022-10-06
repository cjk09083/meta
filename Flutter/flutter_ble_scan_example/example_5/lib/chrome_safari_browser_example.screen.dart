import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class MyChromeSafariBrowser extends ChromeSafariBrowser {
  @override
  void onOpened() {
    print("ChromeSafari browser opened");
  }

  @override
  void onCompletedInitialLoad() {
    print("ChromeSafari browser initial load completed");
  }

  @override
  void onClosed() {
    print("ChromeSafari browser closed");
  }
}

Future main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (Platform.isAndroid) {
    await AndroidInAppWebViewController.setWebContentsDebuggingEnabled(true);
  }

  runApp(MaterialApp(home: MyApp()));
}

class MyApp extends StatefulWidget {
  final ChromeSafariBrowser browser = new MyChromeSafariBrowser();

  @override
  _MyAppState createState() => new _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    widget.browser.addMenuItem(new ChromeSafariBrowserMenuItem(
        id: 1,
        label: 'Custom item menu 1',
        action: (url, title) {
          print('Custom item menu 1 clicked!');
        }));
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ChromeSafariBrowser Example'),
      ),
      body: Center(
        child: ElevatedButton(
            onPressed: () async {
              await widget.browser.open(
                  url: Uri.parse("https://flutter.dev/"),
                  options: ChromeSafariBrowserClassOptions(
                      android: AndroidChromeCustomTabsOptions(
                          shareState: CustomTabsShareState.SHARE_STATE_OFF),
                      ios: IOSSafariOptions(barCollapsingEnabled: true)));
            },
            child: Text("Open Chrome Safari Browser")),
      ),
    );
  }
}