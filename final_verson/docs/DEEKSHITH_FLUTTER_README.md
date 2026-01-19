# Deekshith Survey System - Flutter Integration

## 🎯 Overview

Deekshith is a complete **agricultural intelligence pipeline** that connects:

- **Topview ML** (tree detection & layout via YOLO)
- **Sideview ML** (tree disease & health analysis)
- **Visual Health Maps** (green/red pin visualization)
- **Dashboards** (topview & survey-level aggregation)

This Flutter app provides the complete field interface for farmers to conduct surveys.

---

## 📁 Project Structure

```
lib/
├── core/
│   └── api/
│       └── deekshith_api_client.dart          # HTTP client for backend
│
└── features/
    └── drone/
        ├── models/
        │   └── deekshith_models.dart          # All data models
        ├── services/
        │   ├── deekshith_survey_service.dart  # Service layer
        │   └── offline_queue_manager.dart     # Offline upload queue
        └── screens/
            ├── deekshith_survey_create_screen.dart           # Create survey
            ├── deekshith_topview_capture_screen.dart         # Capture topview
            ├── deekshith_tree_list_screen.dart               # List trees
            ├── deekshith_video_upload_screen.dart            # Upload single video
            ├── deekshith_bulk_video_upload_screen.dart       # Bulk video upload
            ├── deekshith_health_map_screen.dart              # Health map (server)
            ├── deekshith_health_map_canvas_screen.dart       # Health map (canvas)
            ├── deekshith_topview_dashboard_screen.dart       # Topview dashboard
            └── deekshith_survey_dashboard_screen.dart        # Survey dashboard
```

---

## 🔧 Setup Instructions

### 1. Update Backend URL

Open `lib/core/api/deekshith_api_client.dart` and update:

```dart
static const String baseUrl = "http://YOUR_BACKEND_IP:8000";
```

**Find your IP:**

- Windows: `ipconfig` (look for IPv4)
- Mac/Linux: `ifconfig` or `ip addr`
- Cloud: Use your cloud instance public IP

### 2. Required Dependencies

All required packages are already in `pubspec.yaml`:

- ✅ `http` - API calls
- ✅ `image_picker` - Camera & gallery
- ✅ `file_picker` - Video selection
- ✅ `geolocator` - GPS location
- ✅ `shared_preferences` - Offline queue
- ✅ `provider` - State management

Run:

```bash
flutter pub get
```

### 3. Permissions Setup

#### Android (`android/app/src/main/AndroidManifest.xml`)

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

#### iOS (`ios/Runner/Info.plist`)

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need GPS to record farm location</string>
<key>NSCameraUsageDescription</key>
<string>We need camera to capture topview images</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>We need access to select videos</string>
```

---

## 🚀 Usage Flow

### Complete Survey Workflow

```
1. Create Survey
   └─> DeekshithSurveyCreateScreen
       • Input: Farmer ID
       • Auto: GPS location
       • Output: survey_id

2. Capture Topview
   └─> DeekshithTopviewCaptureScreen
       • Input: Drone image
       • Select: Topview order (a, b, c...)
       • Backend: YOLO detects trees
       • Output: tree_count, topview_id

3. View Trees
   └─> DeekshithTreeListScreen
       • Shows: All detected trees (1...N)
       • Actions: Upload single OR bulk

4a. Single Video Upload
    └─> DeekshithVideoUploadScreen
        • Select video for one tree
        • Backend: Sideview ML analysis
        • Output: Tree health dashboard

4b. Bulk Video Upload
    └─> DeekshithBulkVideoUploadScreen
        • Select N videos
        • Auto-map: Video 1 → Tree 1, etc.
        • Backend: Batch processing
        • Output: Processed count

5. Health Map
   └─> DeekshithHealthMapScreen
       • Visual: Topview with colored pins
       • 🟢 Green = Healthy (score ≥ 70)
       • 🔴 Red = Unhealthy (score < 70)
       • ⚪ Grey = No video uploaded

6. Topview Dashboard
   └─> DeekshithTopviewDashboardScreen
       • Total trees
       • Healthy / Unhealthy count
       • Health percentage
       • Dominant disease

7. Survey Dashboard
   └─> DeekshithSurveyDashboardScreen
       • Aggregated across all topviews
       • Overall health score
       • Total trees surveyed
```

---

## 📡 API Endpoints Used

| Flutter Method               | Backend Endpoint                                      | Purpose            |
| ---------------------------- | ----------------------------------------------------- | ------------------ |
| `createSurvey()`             | `POST /survey/create`                                 | Start new survey   |
| `uploadTopview()`            | `POST /survey/{id}/topview`                           | Upload drone image |
| `uploadTreeVideo()`          | `POST /survey/{id}/topview/{order}/tree/{i}/video`    | Single video       |
| `uploadTreeVideosBulk()`     | `POST /survey/{id}/topview/{order}/trees/videos/bulk` | Multiple videos    |
| `getHealthMap()`             | `GET /survey/{id}/topview/{order}/health-map`         | Health JSON        |
| `getHealthMapImage()`        | `GET /survey/{id}/topview/{order}/health-map/image`   | Annotated image    |
| `generateTopviewDashboard()` | `POST /survey/{id}/topview/{order}/dashboard`         | Topview stats      |
| `generateSurveyDashboard()`  | `POST /survey/{id}/dashboard`                         | Survey stats       |

---

## 🎨 Key Features Implemented

### ✅ 1. Bulk Video Upload

- Select multiple videos at once
- Automatic tree index mapping
- Progress tracking
- Partial success handling

### ✅ 2. Health Map Visualization

Two modes:

- **Server-rendered**: Backend generates annotated image
- **Canvas-rendered**: Flutter draws pins with `CustomPainter`

### ✅ 3. Offline Queue System

Located in `offline_queue_manager.dart`:

- Records failed uploads
- Auto-retry when network returns
- Persistent storage with `SharedPreferences`

**Usage:**

```dart
final queue = OfflineQueueManager();

// Add to queue
await queue.addToQueue(UploadTask(
  id: 'task_123',
  type: UploadType.topview,
  filePath: '/path/to/image.jpg',
  surveyId: 17,
  topviewOrder: 'a',
));

// Process queue
final result = await queue.processQueue();
print('Successful: ${result.successful}, Failed: ${result.failed}');
```

### ✅ 4. GPS Auto-location

- Automatic GPS capture on survey creation
- Permission handling
- Error states for denied/unavailable location

### ✅ 5. Interactive Image Viewer

- Pinch to zoom health maps
- Pan & zoom topview images
- Min scale: 0.5x, Max scale: 4x

---

## 🔴 Important Notes

### Backend Compatibility

✅ All endpoints match your Deekshith backend exactly
✅ Request/response formats validated
✅ Error handling for network failures

### File Size Considerations

- Topview images: Compressed to 85% quality, max 1920x1080
- Videos: No compression (handled by backend)
- Large files: Show progress indicators

### Tree Numbering

⚠️ **CRITICAL**: Tree indices start at 1 (not 0)

- Backend expects: `tree_01`, `tree_02`, ...
- Flutter displays: Tree 1, Tree 2, ...
- Bulk upload: Video 1 → Tree 1, Video 2 → Tree 2

### Health Color Rules (Single Source of Truth)

Decision made in backend (`sideview_link/service.py`):

```python
if reliability >= 70 and weighted_score >= 70:
    health = "healthy"  # 🟢
else:
    health = "unhealthy"  # 🔴
```

Flutter NEVER recalculates health — only displays backend result.

---

## 🧪 Testing Checklist

### Before Field Testing

- [ ] Update `baseUrl` in `deekshith_api_client.dart`
- [ ] Test backend connection: `DeekshithApiClient.testConnection()`
- [ ] Verify permissions (Camera, GPS, Storage)
- [ ] Test with sample images/videos
- [ ] Check offline queue behavior (airplane mode)

### Test Scenarios

1. **Happy Path**: Full survey from create → dashboard
2. **Network Failure**: Upload with no internet → queue → retry
3. **Multiple Topviews**: Survey with 2+ topview areas
4. **Bulk Upload**: 10+ videos at once
5. **GPS Issues**: Denied permission, no signal
6. **Large Files**: 100MB+ videos

---

## 🐛 Troubleshooting

### "Connection refused" Error

- Check `baseUrl` is correct
- Ensure backend is running: `python main.py`
- Ping backend IP from phone: `ping YOUR_IP`

### Videos Not Uploading

- Check file exists: `File(path).exists()`
- Verify file picker permissions
- Check backend logs for errors

### GPS Not Working

- Enable location services on device
- Grant app permissions in Settings
- Check if using emulator (use mock location)

### Health Map Not Loading

- Ensure videos are uploaded first
- Check dashboard generation succeeded
- Verify image endpoint returns 200

---

## 📱 Navigation Example

```dart
// From any screen, start new survey:
Navigator.pushNamed(context, '/deekshith-survey-create');

// Navigate with parameters:
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => DeekshithTopviewCaptureScreen(
      surveyId: 17,
      farmerId: 'FARMER_123',
    ),
  ),
);
```

---

## 🔥 Production Readiness Checklist

- [ ] Replace `baseUrl` with production server
- [ ] Add proper error logging (Sentry, Firebase Crashlytics)
- [ ] Implement retry logic with exponential backoff
- [ ] Add upload progress callbacks
- [ ] Compress videos before upload (optional)
- [ ] Add authentication headers to API client
- [ ] Implement survey history screen
- [ ] Add export/share survey results
- [ ] Cache topview images locally
- [ ] Add survey deletion feature

---

## 🎓 Architecture Highlights

### Why This Design is Production-Grade

1. **Separation of Concerns**

   - API Client → Service Layer → UI
   - No business logic in widgets
   - Reusable service methods

2. **Error Handling**

   - Try-catch at every network call
   - User-friendly error messages
   - Offline queue for reliability

3. **State Management**

   - Stateful widgets for local state
   - `Provider` for shared state (if needed)
   - No god objects

4. **Scalability**
   - Easy to add new endpoints
   - Models match backend 1:1
   - Can migrate to GetX/Riverpod easily

---

## 📞 Support

For backend questions: Refer to `Deekshith/README.md`
For Flutter questions: Check Flutter docs

---

## ✅ What You Can Say to Your Mentor/Investor

> "We built a complete agricultural intelligence pipeline called **Deekshith** that connects drone-based tree detection (YOLO) with disease analysis (Sideview ML). The Flutter app provides a field-ready interface where farmers can:
>
> 1. Create surveys with GPS
> 2. Upload topview drone images → auto-detect trees
> 3. Record sideview videos per tree (single or bulk)
> 4. Generate visual health maps (green/red pins)
> 5. View aggregated health dashboards
>
> The system handles offline scenarios with an upload queue, supports multiple topview areas per survey, and visualizes results with interactive maps. All ML is decoupled — this layer only orchestrates and visualizes."

---

**🎉 You're ready to run end-to-end agricultural surveys!**
