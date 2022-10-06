import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart' as web;

class WebPage extends StatelessWidget {
  const WebPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const web.WebView(
      // initialUrl: 'https://app.gather.town/app/WF84QVdIhiE0smuf/home',
      initialUrl: 'https://zep.us/play/yxWJjz',
      javascriptMode: web.JavascriptMode.unrestricted,
      gestureNavigationEnabled: true,
    );
  }
}