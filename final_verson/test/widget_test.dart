// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';
import 'package:final_version/main.dart';
import 'package:final_version/core/providers/language_provider.dart';

void main() {
  testWidgets('App loads and shows login screen', (WidgetTester tester) async {
    // Initialize language provider
    final languageProvider = LanguageProvider();
    await languageProvider.loadSavedLanguage();

    // Build our app and trigger a frame.
    await tester.pumpWidget(MyApp(languageProvider: languageProvider));

    // Wait for the app to settle
    await tester.pumpAndSettle();

    // Verify that we're on the login screen
    expect(find.text('Farm AI Assistant'), findsWidgets);
  });
}
