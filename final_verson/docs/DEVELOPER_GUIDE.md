# Developer Quick Reference

## Common Tasks

### 1. Change Backend IP Address

**File**: `lib/features/ml/services/sideview_api_service.dart`

```dart
static const String baseUrl = 'http://YOUR_IP:8000';
```

### 2. Add New ML Analysis Screen

```dart
// 1. Create screen file
lib/features/ml/screens/new_analysis_screen.dart

// 2. Add route in main.dart
'/new-analysis': (context) => const NewAnalysisScreen(),

// 3. Navigate from another screen
Navigator.pushNamed(context, '/new-analysis', arguments: {'data': value});
```

### 3. Get Farmer ID for API Calls

```dart
import 'package:final_version/features/settings/services/farmer_service.dart';

// Get farmer ID
final farmerId = await FarmerService.getFarmerId();
if (farmerId == null) {
  // Show error: User not logged in
  return;
}

// Use in API call
await apiService.someEndpoint(farmerId: farmerId);
```

### 4. Pass Data Between Screens

```dart
// From source screen
Navigator.pushNamed(
  context,
  '/destination',
  arguments: {
    'video_file': videoFile,
    'survey_id': 123,
  },
);

// In destination screen
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  final args = ModalRoute.of(context)?.settings.arguments as Map?;
  if (args != null) {
    final videoFile = args['video_file'] as File?;
    final surveyId = args['survey_id'] as int?;
  }
}
```

### 5. Call API with File Upload

```dart
import 'package:dio/dio.dart';

Future<Map<String, dynamic>> uploadFile(File file) async {
  final formData = FormData.fromMap({
    'farmer_id': farmerId,
    'file': await MultipartFile.fromFile(
      file.path,
      filename: 'upload.jpg',
    ),
  });

  final response = await _dio.post('/api/endpoint', data: formData);
  return response.data;
}
```

### 6. Show Error/Success Messages

```dart
// Success
ScaffoldMessenger.of(context).showSnackBar(
  const SnackBar(
    content: Text('Analysis completed successfully'),
    backgroundColor: Colors.green,
  ),
);

// Error
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: Text('Error: ${error.toString()}'),
    backgroundColor: AppColors.danger,
  ),
);
```

### 7. Navigate Back with Result

```dart
// Pop with result
Navigator.pop(context, {'success': true, 'data': resultData});

// Receive result
final result = await Navigator.pushNamed(context, '/some-screen');
if (result is Map && result['success'] == true) {
  // Handle success
}
```

## File Locations Quick Reference

### Screens by Feature

**ML Analysis**

- Image capture: `lib/features/ml/screens/sideview_image_capture_screen.dart`
- Video capture: `lib/features/ml/screens/sideview_video_capture_screen.dart`
- Disease results: `lib/features/ml/screens/sideview_result_screen.dart`
- Tree detection: `lib/features/ml/screens/topview_capture_screen.dart`
- Detection results: `lib/features/ml/screens/topview_result_screen.dart`

**Services**

- Disease API: `lib/features/ml/services/sideview_api_service.dart`
- Farmer auth: `lib/features/settings/services/farmer_service.dart`

**Configuration**

- Routes: `lib/main.dart` (lines ~115-145)
- Theme colors: `lib/core/theme/app_colors.dart`
- Text styles: `lib/core/theme/app_text_styles.dart`

## Debugging Checklist

### API Call Not Working

1. ✓ Backend running? Check terminal
2. ✓ Correct IP in service file?
3. ✓ farmer_id set? Check Settings screen
4. ✓ Network connected?
5. ✓ Print response: `print(response.data)`

### Screen Not Loading

1. ✓ Route defined in main.dart?
2. ✓ Correct route name in Navigator.pushNamed()?
3. ✓ Import statement added?
4. ✓ Check console for errors

### Data Not Passing

1. ✓ Arguments passed in Navigator.pushNamed()?
2. ✓ Correct key names in Map?
3. ✓ didChangeDependencies() called?
4. ✓ Print args: `print(args)`

### Build Errors

1. ✓ Run: `flutter clean`
2. ✓ Run: `flutter pub get`
3. ✓ Check imports (unused/missing?)
4. ✓ Check for typos in class names

## Route Reference

| Route                     | Screen                     | Purpose                    |
| ------------------------- | -------------------------- | -------------------------- |
| `/ml-capture`             | SideviewImageCaptureScreen | Single image disease check |
| `/sideview-video-capture` | SideviewVideoCaptureScreen | Video disease analysis     |
| `/sideview-result`        | SideviewResultScreen       | Show disease results       |
| `/topview-capture`        | TopviewCaptureScreen       | Tree counting              |
| `/topview-result`         | TopviewResultScreen        | Show tree count            |
| `/dashboard`              | DashboardScreen            | Main dashboard             |
| `/settings`               | SettingsScreen             | App settings               |
| `/drone-home`             | DroneHomeScreen            | Drone survey start         |

## API Endpoints Reference

### Sideview (Disease Detection)

- **POST** `/api/drone/sideview` - Analyze video

  - Params: `farmer_id`, `survey_id`, `file` (video)
  - Returns: Tree health results

- **POST** `/sideview/analyze` - Analyze image
  - Params: `file` (image)
  - Returns: Disease prediction

### Topview (Tree Detection)

- **POST** `/api/drone/topview` - Detect trees
  - Params: `farmer_id`, `survey_id`, `file` (image)
  - Returns: Tree count + locations

### Farmer

- Managed locally via `FarmerService` (SharedPreferences)
- No API calls for auth currently

## Code Snippets

### Image Picker

```dart
import 'package:image_picker/image_picker.dart';

final picker = ImagePicker();

// Camera
final XFile? image = await picker.pickImage(source: ImageSource.camera);

// Gallery
final XFile? image = await picker.pickImage(source: ImageSource.gallery);

// Video
final XFile? video = await picker.pickVideo(source: ImageSource.camera);
```

### Loading Indicator

```dart
bool _isLoading = false;

Widget build(BuildContext context) {
  return Stack(
    children: [
      // Your content
      if (_isLoading)
        Container(
          color: Colors.black54,
          child: const Center(
            child: CircularProgressIndicator(),
          ),
        ),
    ],
  );
}
```

### Async Button Handler

```dart
bool _isProcessing = false;

Future<void> _handleSubmit() async {
  if (_isProcessing) return; // Prevent double-tap

  setState(() => _isProcessing = true);

  try {
    await someAsyncOperation();
    // Success
  } catch (e) {
    // Error
  } finally {
    if (mounted) {
      setState(() => _isProcessing = false);
    }
  }
}
```

## Environment Setup

### Backend Requirements

- Python 3.10
- TensorFlow 2.10.0
- FastAPI
- PostgreSQL

### Flutter Requirements

- Flutter 3.35.7+
- Dart SDK 3.9.2+

### Running Backend

```bash
cd C:\dev\backend
py -3.10 main.py
# Server starts on http://localhost:8000
```

### Running Flutter App

```bash
cd C:\dev\final_verson
flutter run
```

## Git Workflow

```bash
# Check current changes
git status

# Create feature branch
git checkout -b feature/new-analysis-screen

# Commit changes
git add .
git commit -m "Add new analysis screen with documentation"

# Push to remote
git push origin feature/new-analysis-screen
```

## Performance Tips

1. **Large images**: Compress before upload

   ```dart
   final XFile? image = await picker.pickImage(
     source: ImageSource.camera,
     imageQuality: 85, // 0-100
   );
   ```

2. **Long lists**: Use ListView.builder

   ```dart
   ListView.builder(
     itemCount: items.length,
     itemBuilder: (context, index) => ItemWidget(items[index]),
   );
   ```

3. **Async operations**: Always check `mounted`
   ```dart
   if (mounted) {
     setState(() => _data = newData);
   }
   ```

## Need More Help?

1. Check feature README: `lib/features/{feature}/README.md`
2. Read class documentation in code
3. See ARCHITECTURE.md for detailed guide
4. Check error console output
