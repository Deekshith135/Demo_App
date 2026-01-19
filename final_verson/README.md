+# Final Version – Crop AI Assistant

This app includes:

- ML analysis with results (recommendations + fertilizers)
- Chatbot powered by the Sarvam backend
- Text-to-Speech (TTS) for recommendations/fertilizers on results screen
- Speech-to-Text (STT) mic beside chatbot input

## Prerequisites

- Flutter SDK installed
- Python 3.8+ for the backend
- On Windows, PowerShell available (script auto-uses `pwsh` if present)

## Backend – Start Services

From the backend folder:

```powershell
cd c:\dev\final\endGa+-me\final_verson\backend_new
.\start-backend.ps1
```

This launches the Sarvam AI service on `http://127.0.0.1:8001` (desktop) or `http://10.0.2.2:8001` (Android emulator). If you use virtualenvs, the script will activate them when present.

Services used now:

- `sarvam-ai/` (port 8001): Chatbot endpoint at `POST /llm`

Tip: Ensure `SARVAM_API_KEY` is set in `backend_new/sarvam-ai/.env` if required by your environment.

## Flutter App – Install and Run

Install dependencies and run:

```powershell
cd c:\dev\final\endGame\final_verson
flutter pub get
flutter run
```

Networking notes:

- Android emulator reaches host via `10.0.2.2` (configured in-app).
- Desktop/web uses `127.0.0.1`.

## Permissions

Android:

- `INTERNET` for API calls
- `RECORD_AUDIO` for microphone (STT)

iOS:

- `NSMicrophoneUsageDescription`
- `NSSpeechRecognitionUsageDescription`

These are already configured in `android/app/src/main/AndroidManifest.xml` and `ios/Runner/Info.plist`.

## Features

- ML Result Screen (`lib/features/ml/screens/ml_result_screen.dart`)

  - “Speak” buttons read out Recommendations and Recommended Fertilizers using `flutter_tts`.
  - TTS language auto-selects `kn-IN` when device locale is Kannada, otherwise `en-US`.

- Chatbot Screen (`lib/features/chat/screens/sarvam_chat_screen.dart`)
  - Mic button uses `speech_to_text` to fill the text field with recognized speech.
  - Send button posts to the Sarvam backend and displays the reply.

## Troubleshooting

- Backend not responding:

  - Verify the Sarvam service is running on port 8001.
  - Check that your firewall allows local connections.

- Android device can’t reach backend:

  - Use the emulator’s special host IP `10.0.2.2` (already handled by the app).

- STT not working:
  - Ensure microphone permission is granted.
  - Some devices/locales may not support certain languages; try English.

## Developer Notes

Static analysis:

```powershell
flutter analyze
```

(There may be minor infos; functionality is unaffected.)
