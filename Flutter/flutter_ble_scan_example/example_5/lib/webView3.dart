import 'dart:async';
import 'dart:collection';
import 'dart:developer' as dev;

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


class WebPage3 extends StatefulWidget {
  @override
  _WebPage createState() => new _WebPage();

}

class _WebPage extends State<WebPage3> {
  String initUrl = "https://zep.us/play/yxWJjz";
  Timer? _timer;
  var _time = 0;
  var _isRunning = false;


  final GlobalKey webViewKey = GlobalKey();
  InAppWebViewController? webViewController;
  InAppWebViewGroupOptions options = InAppWebViewGroupOptions(
      crossPlatform: InAppWebViewOptions(
          useShouldOverrideUrlLoading: true,
          mediaPlaybackRequiresUserGesture: false),
      android: AndroidInAppWebViewOptions(
        useHybridComposition: true,
      ),
      ios: IOSInAppWebViewOptions(
        allowsInlineMediaPlayback: true,
      ));

  void _start() {
    dev.log("start timer");
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
        _time++;
        var result = webViewController?.evaluateJavascript(
            source: "document.dispatchEvent(new KeyboardEvent('keydown', {key: 'w'}));"
        );
        dev.log("{$_time} $result");
    });
  }


  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('InAppWebView Example'),
      ),
      body: Center(
        child: InAppWebView(
          key: webViewKey,
          // initialData: InAppWebViewInitialData(
          //   data: initUrl,
          // ),
          initialUrlRequest: URLRequest(url: Uri.parse(initUrl)),
          initialUserScripts: UnmodifiableListView<UserScript>([]),
          initialOptions: options,

          onWebViewCreated: (InAppWebViewController controller) {
            webViewController = controller;
            _start();
          },
          onConsoleMessage: (InAppWebViewController controller, ConsoleMessage consoleMessage) {
            dev.log("Console: ${consoleMessage.message}");
            // showToast(consoleMessage.message);
          },
        ),
      ),
    );
  }
}