# Clean Architecture Guide

## Project Structure

```
lib/
├── core/                       # Core functionality used across features
│   ├── providers/             # State management (Provider pattern)
│   ├── theme/                 # App colors, text styles, themes
│   └── utils/                 # Shared utilities
│
├── features/                   # Feature-based modules (clean architecture)
│   ├── auth/                  # Authentication
│   │   ├── screens/           # UI screens
│   │   ├── services/          # Business logic & API calls
│   │   └── models/            # Data models
│   │
│   ├── ml/                    # Machine Learning Analysis
│   │   ├── screens/
│   │   │   ├── sideview_image_capture_screen.dart    # Single image disease check
│   │   │   ├── sideview_video_capture_screen.dart    # Video analysis for surveys
│   │   │   ├── sideview_result_screen.dart           # Disease results display
│   │   │   ├── topview_capture_screen.dart           # Tree detection capture
│   │   │   └── topview_result_screen.dart            # Tree count results
│   │   ├── services/
│   │   │   └── sideview_api_service.dart             # API client for disease detection
│   │   └── README.md          # Feature documentation
│   │
│   ├── drone/                 # Drone Survey Workflow
│   │   ├── screens/           # Survey flow screens
│   │   ├── services/          # API integration
│   │   └── providers/         # Survey state management
│   │
│   ├── settings/              # App Settings
│   │   ├── screens/           # Settings UI
│   │   └── services/
│   │       └── farmer_service.dart    # User authentication & profile
│   │
│   └── [other features]/      # Dashboard, Chat, History, etc.
│
├── shared/                     # Shared widgets & components
│   └── widgets/               # Reusable UI components
│
├── l10n/                      # Localization (English, Kannada)
│
└── main.dart                  # App entry point & routing

```

## Naming Conventions

### Files

- **Screens**: `{feature}_{purpose}_screen.dart`

  - ✅ `sideview_video_capture_screen.dart`
  - ✅ `topview_result_screen.dart`
  - ❌ `ml_capture_screen_new.dart` (unclear)

- **Services**: `{feature}_api_service.dart` or `{feature}_service.dart`

  - ✅ `sideview_api_service.dart`
  - ✅ `farmer_service.dart`

- **Providers**: `{feature}_provider.dart`
  - ✅ `drone_survey_provider.dart`

### Classes

- **Screens**: `{Feature}{Purpose}Screen`

  - ✅ `SideviewVideoCaptureScreen`
  - ✅ `TopviewResultScreen`

- **Services**: `{Feature}Service` or `{Feature}ApiService`
  - ✅ `SideviewApiService`
  - ✅ `FarmerService`

### Variables

- Use descriptive names, avoid abbreviations
  - ✅ `farmerId`, `surveyId`, `videoFile`
  - ❌ `id`, `f_id`, `vid`

## Code Documentation

### Class Documentation

Every class should have a doc comment explaining:

1. **Purpose**: What it does
2. **Usage**: When/where it's used
3. **Flow**: User interaction flow (for screens)
4. **API**: Which endpoints it calls (for services)

Example:

```dart
/// Sideview Video Capture Screen
///
/// Purpose: Record or upload videos for comprehensive tree health analysis
/// API: Sends to /api/drone/sideview endpoint (requires farmer_id, survey_id)
/// Flow: Record/Gallery → Video Selection → Survey ID Input → Analysis → Result Screen
///
/// Used in: Drone Survey workflow for detailed multi-tree analysis
/// Video analyzed frame-by-frame, results aggregated by tree
class SideviewVideoCaptureScreen extends StatefulWidget {
```

### Method Documentation

Public methods should document:

1. What it does
2. Parameters with descriptions
3. Return value
4. Exceptions thrown

Example:

```dart
/// Analyze sideview video and get aggregated health results
///
/// Parameters:
/// - [videoFile]: MP4/MOV video file (<100MB recommended)
/// - [farmerId]: Farmer ID from FarmerService (required for tracking)
/// - [surveyId]: Survey session ID (links to database)
///
/// Returns: Map with total_trees, farmer_id, survey_id, and trees array
///
/// Throws: Exception with error message if API call fails
Future<Map<String, dynamic>> analyzeVideo({...}) async {
```

## Feature Organization

### 1. Screens (UI Layer)

- Handle user interaction
- Display data
- Call services for business logic
- Navigate to other screens

**Do:**

- Keep screens focused on UI
- Extract business logic to services
- Use clear, descriptive names

**Don't:**

- Put API calls directly in screens (use services)
- Mix multiple features in one screen
- Use generic names like "Screen1", "NewScreen"

### 2. Services (Business Logic Layer)

- API calls
- Data transformation
- Business rules

**Do:**

- One service per API/domain
- Clear method names
- Proper error handling
- Comprehensive documentation

**Don't:**

- Mix UI logic in services
- Ignore errors (always handle or throw)
- Use generic names like "Service", "Helper"

### 3. Providers (State Management)

- Manage feature state
- Notify listeners on changes
- Share data across screens

**Do:**

- Use for complex state
- Notify listeners appropriately
- Document state changes

**Don't:**

- Overuse for simple data
- Mix multiple features in one provider

## Routes

Routes should be descriptive and follow REST-like patterns:

```dart
// ✅ Good
'/sideview-video-capture'
'/topview-result'
'/drone-start-survey'

// ❌ Bad
'/ml-capture'  // Unclear which type
'/screen1'     // No meaning
'/new-feature' // Not descriptive
```

## API Integration

### Base URL Configuration

Store in service constants:

```dart
class SideviewApiService {
  static const String baseUrl = 'http://192.168.1.100:8000';
  // Easy to update when backend changes
}
```

### Error Handling

Always handle API errors:

```dart
try {
  final response = await _dio.post('/api/endpoint', data: data);
  return response.data;
} on DioException catch (e) {
  throw Exception('Failed to process: ${e.message}');
}
```

## Testing & Debugging

### Quick Debugging Checklist

1. **API not working?**

   - Check backend is running
   - Verify IP in service file
   - Check network connectivity

2. **Authentication errors?**

   - Verify farmer_id is set (FarmerService.getFarmerId())
   - Check Settings screen shows Farmer ID

3. **Screen not showing?**

   - Verify route in main.dart
   - Check navigation call uses correct route name

4. **Data not passing between screens?**
   - Verify arguments in Navigator.pushNamed()
   - Check ModalRoute.of(context)?.settings.arguments

## Adding New Features

### Step-by-Step Guide

1. **Create feature folder**

   ```
   lib/features/new_feature/
   ├── screens/
   ├── services/
   └── README.md
   ```

2. **Create screens with clear names**

   - `new_feature_action_screen.dart`
   - Follow naming convention

3. **Create services for API calls**

   - `new_feature_api_service.dart`
   - Add documentation

4. **Add routes in main.dart**

   ```dart
   // New Feature
   '/new-feature-action': (context) => const NewFeatureActionScreen(),
   ```

5. **Document in feature README.md**
   - Explain purpose
   - Document data flow
   - Add API details

## Code Review Checklist

Before committing:

- [ ] All classes have doc comments
- [ ] File names follow convention
- [ ] No compilation errors
- [ ] API errors handled properly
- [ ] Routes added to main.dart
- [ ] README updated if needed
- [ ] No unused imports
- [ ] Descriptive variable names

## Resources

- **ML Feature**: See `lib/features/ml/README.md`
- **State Management**: Provider package docs
- **API Client**: Dio package docs
- **Local Storage**: SharedPreferences (used in FarmerService)

## Support

For questions about architecture or debugging, check:

1. Feature README files
2. Class documentation comments
3. This guide

Common patterns and examples are documented in the codebase.
