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


class WebPage extends StatefulWidget {
  final ChromeSafariBrowser browser = new MyChromeSafariBrowser();

  @override
  _WebPage createState() => new _WebPage();

  // @override
  // Widget build(BuildContext context) {
  //   return const WebView(
  //     // initialUrl: 'https://app.gather.town/app/WF84QVdIhiE0smuf/home',
  //     initialUrl: 'https://www.gather.town/',
  //     javascriptMode: JavascriptMode.unrestricted,  // javascript 활성화
  //     gestureNavigationEnabled: true, // 스와이프 활성화
  //     userAgent: "random",  // 구글 로그인을 위한 userAgent 부여
  //   );
  // }
}

class _WebPage extends State<WebPage> {
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
                  url: Uri.parse("https://app.gather.town/app/WF84QVdIhiE0smuf/home"),
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