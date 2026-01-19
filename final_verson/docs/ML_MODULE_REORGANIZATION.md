# ML Module Reorganization Summary

## Overview

Reorganized the ML features into **3 separate, independent modules** for easier debugging and maintenance. Each module has its own folder with dedicated screens and services.

---

## 📁 New Folder Structure

```
lib/features/ml/
├── topview/                    # Tree Detection Module
│   ├── topview_capture_screen.dart
│   ├── topview_result_screen.dart
│   └── topview_service.dart
│
├── sideview/                   # Disease Detection (Image) Module
│   ├── sideview_capture_screen.dart
│   ├── sideview_result_screen.dart
│   └── sideview_service.dart
│
└── sidevideo/                  # Disease Detection (Video) Module
    ├── sidevideo_capture_screen.dart
    ├── sidevideo_result_screen.dart
    └── sidevideo_service.dart
```

---

## 🎯 Module Details

### 1. Topview Module (Tree Detection)

**Purpose:** Detect and count coconut trees from overhead/drone photos

**Files:**

- `topview_capture_screen.dart` - Capture overhead photos or upload drone images
- `topview_result_screen.dart` - Display tree count and annotated image
- `topview_service.dart` - API service for tree detection

**Backend API:**

- `POST /topview/detect` - Multi-tree detection
- `POST /topview/detect/image` - Single image detection

**Route:**

- `/topview-capture` → TopviewCaptureScreen
- `/topview-result` → TopviewResultScreen

---

### 2. Sideview Module (Disease Detection - Image)

**Purpose:** Detect diseases from side photos of coconut trees

**Files:**

- `sideview_capture_screen.dart` - Capture side photos of trees
- `sideview_result_screen.dart` - Display disease results with health status
- `sideview_service.dart` - API service for image disease detection

**Backend API:**

- `POST /sideview/predict_image` - Disease detection from image

**Route:**

- `/sideview-capture` → SideviewCaptureScreen
- `/sideview-result` → SideviewResultScreen

**Features:**

- Image capture or gallery upload
- Disease classification
- Health percentage
- Detailed recommendations
- Visual results with confidence scores

---

### 3. Sidevideo Module (Disease Detection - Video)

**Purpose:** Comprehensive disease detection from video recordings

**Files:**

- `sidevideo_capture_screen.dart` - Record or upload videos
- `sidevideo_result_screen.dart` - Display frame-by-frame analysis dashboard
- `sidevideo_service.dart` - API service for video disease detection

**Backend API:**

- `POST /sideview/process_video` - Process video for disease detection

**Route:**

- `/sidevideo-capture` → SidevideoCapture Screen
- `/sidevideo-result` → SidevideoResultScreen

**Features:**

- Video recording (1-2 minutes)
- Gallery video upload
- Frame-by-frame analysis
- Dashboard with metrics:
  - Total frames analyzed
  - Healthy frames count
  - Diseased frames count
  - Health percentage
  - Overall status
- Individual frame predictions with confidence
- Detailed recommendations based on severity

**Processing Time:** 1-5 minutes (backend processing)

---

## 🔄 Updated Files

### 1. main.dart

**Changes:**

- Updated imports to point to new module folders
- Added 6 routes (2 per module)
- Clear comments for each module

```dart
// ML Analysis - Clean Architecture (3 Independent Modules)

// Topview Module: Tree Detection from Overhead Photos
'/topview-capture': (context) => const TopviewCaptureScreen(),
'/topview-result': (context) => const TopviewResultScreen(),

// Sideview Module: Disease Detection from Side Images
'/sideview-capture': (context) => const SideviewCaptureScreen(),
'/sideview-result': (context) => const SideviewResultScreen(),

// Sidevideo Module: Disease Detection from Videos
'/sidevideo-capture': (context) => const SidevideoCapture Screen(),
'/sidevideo-result': (context) => const SidevideoResultScreen(),
```

### 2. dashboard_screen.dart

**Changes:**

- Changed "Disease Detection" button to show selection dialog
- Added `_showMLAnalysisDialog()` method
- Added `_buildAnalysisOption()` helper widget
- Users can now choose between:
  - **Image Analysis** (sideview)
  - **Video Analysis** (sidevideo)
  - **Tree Detection** (topview)

---

## 🎨 User Experience Flow

### From Dashboard:

```
Dashboard
  └─> Click "Disease Detection" Button
        └─> Dialog appears with 3 options:
              ├─> Image Analysis → /sideview-capture
              ├─> Video Analysis → /sidevideo-capture
              └─> Tree Detection → /topview-capture
```

### Image Analysis Flow (Sideview):

```
/sideview-capture
  ├─> Capture photo OR Upload from gallery
  └─> Analyze image (loading)
        └─> /sideview-result
              ├─> Disease name
              ├─> Health status
              ├─> Confidence score
              ├─> Recommendations
              └─> Action buttons
```

### Video Analysis Flow (Sidevideo):

```
/sidevideo-capture
  ├─> Record video OR Upload from gallery
  └─> Analyze video (1-5 min processing)
        └─> /sidevideo-result
              ├─> Overall health status
              ├─> Statistics (total/healthy/diseased frames)
              ├─> Frame-by-frame analysis list
              ├─> Detailed recommendations
              └─> Action buttons
```

### Tree Detection Flow (Topview):

```
/topview-capture
  ├─> Capture overhead photo OR Upload
  └─> Detect trees (loading)
        └─> /topview-result
              ├─> Tree count
              ├─> Annotated image
              ├─> Detection confidence
              └─> Action buttons
```

---

## 🔧 Backend API Integration

### API Endpoints Used:

```
Topview Module:
  POST /topview/detect
  POST /topview/detect/image

Sideview Module:
  POST /sideview/predict_image

Sidevideo Module:
  POST /sideview/process_video
```

### Base URL:

```dart
http://10.57.117.58:8000
```

Defined in: `lib/core/constants/api_endpoints.dart`

---

## 🗂️ Service Files

Each module has a dedicated service file:

### topview_service.dart

```dart
class TopviewService {
  Future<Map<String, dynamic>> detectTrees({
    required File imageFile,
  }) async { ... }
}
```

### sideview_service.dart

```dart
class SideviewService {
  Future<Map<String, dynamic>> analyzeImage({
    required File imageFile,
  }) async { ... }
}
```

### sidevideo_service.dart

```dart
class SidevideoService {
  Future<Map<String, dynamic>> analyzeVideo({
    required File videoFile,
  }) async { ... }
}
```

---

## ✅ Benefits of New Structure

1. **Easy Debugging:**

   - Each module is isolated
   - Clear separation of concerns
   - No confusion between image/video flows

2. **Maintainable:**

   - One module = one folder
   - Related files grouped together
   - Easy to locate and fix issues

3. **Scalable:**

   - Add new features per module without affecting others
   - Each module can evolve independently

4. **Clean Architecture:**

   - UI screens separated from business logic (services)
   - Services handle all API communication
   - Clear data flow: Screen → Service → API

5. **User-Friendly:**
   - Clear dialog showing all analysis options
   - Users understand the difference between image/video
   - Separate routes for each feature

---

## 🚀 Next Steps

### Immediate:

- ✅ All 3 modules created
- ✅ Routes updated in main.dart
- ✅ Dashboard updated with selection dialog
- ✅ Services configured for API calls

### Testing Checklist:

- [ ] Test topview: Photo capture → Tree detection → Result display
- [ ] Test sideview: Image capture → Disease detection → Result display
- [ ] Test sidevideo: Video recording → Frame analysis → Dashboard display
- [ ] Test navigation: Dashboard → Dialog → Each module
- [ ] Test back navigation from each result screen
- [ ] Verify API calls with backend

### Optional Enhancements:

- [ ] Add history screen updates for new structure
- [ ] Update crop_analysis_screen.dart references if needed
- [ ] Add loading animations specific to each module
- [ ] Add error handling for network failures
- [ ] Add offline mode indicators

---

## 📊 Module Comparison

| Feature             | Topview                      | Sideview                  | Sidevideo                 |
| ------------------- | ---------------------------- | ------------------------- | ------------------------- |
| **Input**           | Overhead photos              | Side photos               | Video (1-2 min)           |
| **Purpose**         | Count trees                  | Detect diseases           | Comprehensive analysis    |
| **Processing Time** | ~2-5 seconds                 | ~2-5 seconds              | 1-5 minutes               |
| **Output**          | Tree count + annotated image | Disease + health status   | Frame dashboard + metrics |
| **API Endpoint**    | `/topview/detect`            | `/sideview/predict_image` | `/sideview/process_video` |
| **Best For**        | Farm planning, surveys       | Quick diagnosis           | Detailed assessment       |

---

## 🔗 Related Documentation

- **API Endpoints:** `lib/core/constants/api_endpoints.dart`
- **Complete Routing Guide:** `COMPLETE_APP_ROUTING_GUIDE.md`
- **Architecture:** `ARCHITECTURE.md`
- **Backend Integration:** `BACKEND_INTEGRATION_GUIDE.md`

---

## 📝 Code Examples

### Using Topview Service:

```dart
final service = TopviewService();
final result = await service.detectTrees(imageFile: myPhoto);
// result contains: tree_count, annotated_image_url
```

### Using Sideview Service:

```dart
final service = SideviewService();
final result = await service.analyzeImage(imageFile: myPhoto);
// result contains: disease_name, health_status, confidence, recommendations
```

### Using Sidevideo Service:

```dart
final service = SidevideoService();
final result = await service.analyzeVideo(videoFile: myVideo);
// result contains: dashboard with predictions, summary, frame analysis
```

---

## 🎯 Summary

Successfully reorganized ML module into **3 independent, clean, and debuggable modules**:

1. **Topview** → Tree detection from overhead photos
2. **Sideview** → Disease detection from images
3. **Sidevideo** → Comprehensive disease detection from videos

Each module is self-contained with:

- ✅ Capture screen
- ✅ Result screen
- ✅ Dedicated service
- ✅ Clear routing
- ✅ Proper API integration

**Result:** Easier debugging, better organization, clearer user experience! 🎉
