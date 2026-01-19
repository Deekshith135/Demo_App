# 🔥 **COMPLETE BACKEND INTEGRATION GUIDE**

## 📋 **TABLE OF CONTENTS**

1. [Backend Overview](#backend-overview)
2. [Working Endpoints](#working-endpoints)
3. [Deekshith Survey System](#deekshith-survey)
4. [Flutter Integration](#flutter-integration)
5. [Complete Workflow](#complete-workflow)
6. [Error Handling](#error-handling)
7. [Testing Guide](#testing-guide)

---

<a name="backend-overview"></a>

## 🏗️ **1. BACKEND OVERVIEW**

### **Server Configuration**

```
Host: 10.57.117.58
Port: 8000
Base URL: http://10.57.117.58:8000
API Docs: http://10.57.117.58:8000/docs
```

### **Backend Architecture**

```
Backend/
├── main.py                    # FastAPI entry point
│
├── topview/                   # Tree detection (YOLO)
│   ├── router.py              # Endpoints: /topview/*
│   └── model.py               # YOLO detection model
│
├── sideview/                  # Disease detection (Transfer Learning)
│   ├── router.py              # Endpoints: /sideview/*
│   └── model.py               # Disease classification
│
├── chat/                      # AI Chatbot (Sarvam AI)
│   └── router.py              # Endpoints: /chat/*
│
├── expert/                    # Expert consultation
│   └── router.py              # Endpoints: /expert/*
│
└── Deekshith/                 # 🌟 Survey orchestration system
    ├── survey/                # Survey CRUD
    ├── topview_link/          # Topview integration
    ├── sideview_link/         # Sideview integration
    ├── dashboard/             # Multi-level dashboards
    ├── map/                   # Health maps with visualization
    └── storage/               # File storage
```

---

<a name="working-endpoints"></a>

## 🔗 **2. ALL WORKING ENDPOINTS**

### **✅ HEALTH & STATUS**

#### `GET /health`

**Purpose**: Check backend health status

**Response**:

```json
{
  "status": "ok"
}
```

**Flutter Example**:

```dart
Future<bool> checkHealth() async {
  final response = await http.get(Uri.parse('$baseUrl/health'));
  return response.statusCode == 200;
}
```

---

### **✅ TOPVIEW - Tree Detection**

#### `POST /topview/detect`

**Purpose**: Detect trees from topview image (JSON response)

**Request**: Multipart form data with `file` field

**Response**:

```json
{
  "count": 20,
  "trees": [
    {
      "tree_number": 1,
      "cx": 340,
      "cy": 187,
      "bbox": [212.72, 66.78, 468.81, 308.97]
    },
    ...
  ]
}
```

**Flutter Example**:

```dart
Future<Map<String, dynamic>> detectTrees(File imageFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/topview/detect'),
  );

  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path),
  );

  var streamedResponse = await request.send();
  var response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Detection failed: ${response.body}');
  }
}
```

---

#### `POST /topview/detect/image`

**Purpose**: Get annotated image with tree markers

**Request**: Multipart form data with `file` field

**Response**: PNG image bytes

**Flutter Example**:

```dart
Future<Uint8List> getAnnotatedImage(File imageFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/topview/detect/image'),
  );

  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path),
  );

  var streamedResponse = await request.send();
  var response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    return response.bodyBytes;
  } else {
    throw Exception('Failed to get image');
  }
}

// Display in Flutter
Image.memory(annotatedImageBytes)
```

---

### **✅ SIDEVIEW - Disease Detection**

#### `POST /sideview/predict_image`

**Purpose**: Analyze single image for disease detection

**Request**: Multipart form data with `file` field

**Response**:

```json
{
  "success": true,
  "filename": "tree.jpg",
  "prediction": {
    "predicted_index": 5,
    "predicted_label": "Leaf Rot - Leaves",
    "status": {
      "prediction": "leaf rot",
      "confidence": 87.5
    },
    "part": {
      "prediction": "leaves",
      "confidence": 92.3
    },
    "health": "unhealthy",
    "top2": [
      { "label": "Leaf Rot - Leaves", "confidence": 87.5 },
      { "label": "Healthy - Leaves", "confidence": 10.2 }
    ]
  }
}
```

**Flutter Example**:

```dart
Future<Map<String, dynamic>> predictDisease(File imageFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/sideview/predict_image'),
  );

  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path),
  );

  var streamedResponse = await request.send();
  var response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Prediction failed: ${response.body}');
  }
}
```

---

#### `POST /sideview/process_video`

**Purpose**: Process video for comprehensive disease analysis

**Request**: Multipart form data with `file` field

**Response**:

```json
{
  "success": true,
  "filename": "tree_video.mp4",
  "predictions": [...],  // Per-frame predictions
  "dashboard": {
    "tree": {
      "health": "unhealthy",
      "score": 45.0,
      "weighted_score": 45.2,
      "primary_disease": "leaf rot",
      "confidence": 87.5
    },
    "parts": {
      "stem": {
        "health": "healthy",
        "score": 85.0,
        "diseases": []
      },
      "leaves": {
        "health": "unhealthy",
        "score": 30.0,
        "primary_disease": "leaf rot",
        "confidence": 87.5
      },
      "bud": {
        "health": "healthy",
        "score": 90.0,
        "diseases": []
      }
    },
    "meta": {
      "total_frames": 150,
      "valid_frames": 142,
      "reliability": 94.7
    }
  },
  "report_url": "/results/.../video_report.html"
}
```

**Flutter Example**:

```dart
Future<Map<String, dynamic>> processVideo(File videoFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/sideview/process_video'),
  );

  request.files.add(
    await http.MultipartFile.fromPath('file', videoFile.path),
  );

  // Video processing takes 1-5 minutes
  var streamedResponse = await request.send().timeout(
    Duration(minutes: 5),
  );
  var response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Video processing failed: ${response.body}');
  }
}
```

---

### **✅ CHAT - AI Assistant**

#### `POST /chat/llm`

**Purpose**: Chat with AI assistant

**Request**:

```json
{
  "prompt": "How do I treat leaf rot in coconut trees?"
}
```

**Response**:

```json
{
  "response": "Leaf rot can be treated by...",
  "model": "sarvam-2b-v0.5",
  "timestamp": "2026-01-06T10:12:00"
}
```

**Flutter Example**:

```dart
Future<String> chatWithAI(String question) async {
  final response = await http.post(
    Uri.parse('$baseUrl/chat/llm'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({'prompt': question}),
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return data['response'];
  } else {
    throw Exception('Chat failed: ${response.body}');
  }
}
```

---

<a name="deekshith-survey"></a>

## 🌟 **3. DEEKSHITH SURVEY SYSTEM (Complete Workflow)**

### **Overview**

The Deekshith module orchestrates the complete survey workflow:

1. Create survey
2. Upload topview images → detect trees
3. Upload tree videos → get health analysis
4. Generate dashboards (tree → topview → survey)
5. Visualize health maps with color-coded markers

---

### **📍 Survey Management**

#### `POST /survey/create`

**Purpose**: Create a new survey

**Request**:

```json
{
  "farmer_id": "F001",
  "location": {
    "lat": 12.97,
    "lon": 77.59
  }
}
```

**Response**:

```json
{
  "survey_id": 1,
  "timestamp": "2026-01-06T10:12:00",
  "status": "active"
}
```

---

#### `GET /survey/list`

**Purpose**: List all surveys

**Response**:

```json
{
  "surveys": [
    {
      "survey_id": 1,
      "farmer_id": "F001",
      "timestamp": "2026-01-06T10:12:00",
      "status": "active"
    }
  ]
}
```

---

#### `GET /survey/{survey_id}/result`

**Purpose**: Get complete survey data

**Response**: Complete nested structure with all topviews, trees, dashboards, and maps

---

### **📍 Topview Operations**

#### `POST /survey/{survey_id}/topview`

**Purpose**: Upload topview image and detect trees

**Form Data**:

- `topview_order`: "a" (or "b", "c", etc.)
- `image`: File

**Response**:

```json
{
  "topview_id": "1a",
  "tree_count": 20,
  "detection_path": "..."
}
```

**What happens internally**:

1. Saves image to storage
2. Calls `/topview/detect` to detect trees
3. Creates directory structure for trees
4. Returns tree count

---

### **📍 Tree Video Operations**

#### `POST /survey/{survey_id}/topview/{topview_order}/tree/{tree_index}/video`

**Purpose**: Upload single tree video

**Form Data**:

- `video`: File

**Response**:

```json
{
  "tree_id": "1a_tree_03",
  "tree_index": "tree_03",
  "dashboard": {
    "tree": {
      "health": "unhealthy",
      "weighted_score": 45.2,
      "primary_disease": "leaf rot"
    }
  }
}
```

**Example**: `/survey/1/topview/a/tree/3/video`

---

#### `POST /survey/{survey_id}/topview/{topview_order}/trees/videos/bulk` 🌟

**Purpose**: Upload multiple tree videos at once

**Form Data**:

- `tree_indices`: "1,2,3,4,5" (comma-separated)
- `videos`: [file1, file2, file3, ...]

**Response**:

```json
{
  "survey_id": 1,
  "topview_id": "1a",
  "total_videos": 5,
  "processed": 4,
  "failed": 1,
  "results": [
    {
      "tree_index": 1,
      "status": "success",
      "data": {...}
    }
  ],
  "errors": [
    {
      "tree_index": 5,
      "status": "failed",
      "error": "Video processing timeout"
    }
  ]
}
```

---

### **📍 Dashboard Operations**

#### `POST /survey/{survey_id}/topview/{topview_order}/dashboard`

**Purpose**: Generate topview dashboard (aggregates all tree dashboards)

**Response**:

```json
{
  "topview_id": "1a",
  "total_trees": 20,
  "healthy": 14,
  "unhealthy": 6,
  "health_score": 70.0,
  "dominant_disease": "leaf rot",
  "disease_distribution": {
    "leaf rot": 4,
    "stem bleeding": 2
  }
}
```

---

#### `POST /survey/{survey_id}/dashboard`

**Purpose**: Generate final survey dashboard (aggregates all topviews)

**Response**:

```json
{
  "survey_id": 1,
  "total_topviews": 2,
  "total_trees": 40,
  "healthy": 28,
  "unhealthy": 12,
  "overall_health_score": 70.0,
  "primary_disease": "leaf rot"
}
```

---

### **📍 Health Map Operations**

#### `GET /survey/{survey_id}/topview/{topview_order}/health-map`

**Purpose**: Get health map with tree positions and colors

**Response**:

```json
{
  "survey_id": 1,
  "topview_id": "1a",
  "total_trees": 20,
  "topview_image": "/storage/surveys/SURVEY_1/topviews/1a/image.jpg",
  "map": [
    {
      "tree": 1,
      "tree_index": "tree_01",
      "x": 340,
      "y": 187,
      "health": "healthy",
      "color": "green"
    },
    {
      "tree": 3,
      "x": 644,
      "y": 230,
      "health": "unhealthy",
      "color": "red"
    }
  ]
}
```

---

#### `GET /survey/{survey_id}/topview/{topview_order}/health-map/image` 🌟

**Purpose**: Get annotated topview image with colored health markers

**Response**: JPEG image with colored circles:

- 🟢 Green = Healthy
- 🔴 Red = Unhealthy
- ⚪ Grey = Unknown (no video uploaded)

**Flutter Example**:

```dart
String getHealthMapImageUrl(int surveyId, String order) {
  return '$baseUrl/survey/$surveyId/topview/$order/health-map/image';
}

// Display in Flutter
Image.network(
  getHealthMapImageUrl(1, 'a'),
  fit: BoxFit.contain,
)
```

---

<a name="flutter-integration"></a>

## 📱 **4. COMPLETE FLUTTER INTEGRATION**

### **Fix Required Services**

Your current Flutter app has these issues:

1. ❌ `SideviewApiService.analyzeImage()` calls `/sideview/analyze` (doesn't exist)

   - ✅ Should call `/sideview/predict_image`

2. ❌ `SideviewApiService.analyzeVideo()` calls `/api/drone/sideview` (doesn't exist)
   - ✅ Should call `/sideview/process_video`

### **Updated Services**

Create `lib/services/deekshith_survey_service.dart`:

```dart
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class DeekshithSurveyService {
  static const String baseUrl = 'http://10.57.117.58:8000';

  // Timeouts
  static const Duration normalTimeout = Duration(seconds: 30);
  static const Duration videoTimeout = Duration(minutes: 5);
  static const Duration bulkTimeout = Duration(minutes: 30);

  // 1. Create Survey
  Future<Map<String, dynamic>> createSurvey({
    required String farmerId,
    required double lat,
    required double lon,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/survey/create'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'farmer_id': farmerId,
        'location': {'lat': lat, 'lon': lon},
      }),
    ).timeout(normalTimeout);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to create survey: ${response.body}');
    }
  }

  // 2. Upload Topview
  Future<Map<String, dynamic>> uploadTopview({
    required int surveyId,
    required String order,
    required File imageFile,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/survey/$surveyId/topview'),
    );

    request.fields['topview_order'] = order;
    request.files.add(
      await http.MultipartFile.fromPath('image', imageFile.path),
    );

    var streamedResponse = await request.send().timeout(normalTimeout);
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Upload failed: ${response.body}');
    }
  }

  // 3. Upload Single Tree Video
  Future<Map<String, dynamic>> uploadTreeVideo({
    required int surveyId,
    required String topviewOrder,
    required int treeIndex,
    required File videoFile,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/survey/$surveyId/topview/$topviewOrder/tree/$treeIndex/video'),
    );

    request.files.add(
      await http.MultipartFile.fromPath('video', videoFile.path),
    );

    var streamedResponse = await request.send().timeout(videoTimeout);
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Video processing failed: ${response.body}');
    }
  }

  // 4. Bulk Upload Videos
  Future<Map<String, dynamic>> uploadMultipleVideos({
    required int surveyId,
    required String topviewOrder,
    required List<File> videoFiles,
    required List<int> treeIndices,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/survey/$surveyId/topview/$topviewOrder/trees/videos/bulk'),
    );

    request.fields['tree_indices'] = treeIndices.join(',');

    for (var videoFile in videoFiles) {
      request.files.add(
        await http.MultipartFile.fromPath('videos', videoFile.path),
      );
    }

    var streamedResponse = await request.send().timeout(bulkTimeout);
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Bulk upload failed: ${response.body}');
    }
  }

  // 5. Generate Dashboards
  Future<Map<String, dynamic>> generateTopviewDashboard({
    required int surveyId,
    required String topviewOrder,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/survey/$surveyId/topview/$topviewOrder/dashboard'),
    ).timeout(normalTimeout);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Dashboard failed: ${response.body}');
    }
  }

  // 6. Get Health Map
  Future<Map<String, dynamic>> getHealthMap({
    required int surveyId,
    required String topviewOrder,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/survey/$surveyId/topview/$topviewOrder/health-map'),
    ).timeout(normalTimeout);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Health map failed: ${response.body}');
    }
  }

  // 7. Get Health Map Image URL
  String getHealthMapImageUrl(int surveyId, String topviewOrder) {
    return '$baseUrl/survey/$surveyId/topview/$topviewOrder/health-map/image';
  }

  // 8. List Surveys
  Future<List<dynamic>> listSurveys() async {
    final response = await http.get(
      Uri.parse('$baseUrl/survey/list'),
    ).timeout(normalTimeout);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['surveys'];
    } else {
      throw Exception('List failed: ${response.body}');
    }
  }
}
```

---

<a name="complete-workflow"></a>

## 🔄 **5. COMPLETE WORKFLOW EXAMPLE**

```dart
// Complete survey workflow
Future<void> completeSurveyWorkflow() async {
  final service = DeekshithSurveyService();

  // Step 1: Create Survey
  final survey = await service.createSurvey(
    farmerId: 'F001',
    lat: 12.97,
    lon: 77.59,
  );
  final surveyId = survey['survey_id'];

  // Step 2: Upload Topview Image
  final topview = await service.uploadTopview(
    surveyId: surveyId,
    order: 'a',
    imageFile: topviewImage,
  );
  print('Detected ${topview['tree_count']} trees');

  // Step 3: Upload Tree Videos (Bulk)
  final bulkResult = await service.uploadMultipleVideos(
    surveyId: surveyId,
    topviewOrder: 'a',
    videoFiles: [video1, video2, video3],
    treeIndices: [1, 2, 3],
  );
  print('Processed: ${bulkResult['processed']}/${bulkResult['total_videos']}');

  // Step 4: Generate Dashboard
  final dashboard = await service.generateTopviewDashboard(
    surveyId: surveyId,
    topviewOrder: 'a',
  );
  print('Health Score: ${dashboard['health_score']}%');

  // Step 5: Get Health Map
  final healthMap = await service.getHealthMap(
    surveyId: surveyId,
    topviewOrder: 'a',
  );

  // Step 6: Display Health Map Image
  final imageUrl = service.getHealthMapImageUrl(surveyId, 'a');
  Image.network(imageUrl);
}
```

---

<a name="error-handling"></a>

## ⚠️ **6. ERROR HANDLING**

```dart
class ApiException implements Exception {
  final int statusCode;
  final String message;

  ApiException(this.statusCode, this.message);

  @override
  String toString() => 'API Error ($statusCode): $message';
}

// Usage
try {
  final result = await service.createSurvey(...);
} on SocketException {
  // No internet
  showError('No internet connection');
} on TimeoutException {
  // Request timeout
  showError('Request timed out. Please try again.');
} on ApiException catch (e) {
  // API error
  showError('Error: ${e.message}');
} catch (e) {
  // Unknown error
  showError('Unexpected error: $e');
}
```

---

<a name="testing-guide"></a>

## 🧪 **7. TESTING GUIDE**

### **Test Health Check**

```bash
curl http://10.57.117.58:8000/health
```

### **Test Topview Detection**

```bash
curl -X POST http://10.57.117.58:8000/topview/detect \
  -F "file=@topview.jpg"
```

### **Test Complete Survey Flow**

```bash
# 1. Create survey
curl -X POST http://10.57.117.58:8000/survey/create \
  -H "Content-Type: application/json" \
  -d '{"farmer_id": "F001", "location": {"lat": 12.97, "lon": 77.59}}'

# 2. Upload topview
curl -X POST http://10.57.117.58:8000/survey/1/topview \
  -F "topview_order=a" \
  -F "image=@topview.jpg"

# 3. Upload tree video
curl -X POST http://10.57.117.58:8000/survey/1/topview/a/tree/1/video \
  -F "video=@tree1.mp4"

# 4. Generate dashboard
curl -X POST http://10.57.117.58:8000/survey/1/topview/a/dashboard

# 5. Get health map
curl http://10.57.117.58:8000/survey/1/topview/a/health-map
```

---

## 📊 **SUMMARY**

### **Backend Capabilities**

✅ Tree detection (YOLO)  
✅ Disease detection (Transfer Learning)  
✅ Video processing with frame-by-frame analysis  
✅ Multi-level dashboards (tree → topview → survey)  
✅ Visual health maps with colored markers  
✅ Bulk video upload  
✅ Complete survey orchestration  
✅ AI chatbot  
✅ File storage with static serving

### **What You Need to Do in Flutter**

1. ✅ Fix API endpoint URLs in existing services
2. ✅ Add DeekshithSurveyService
3. ✅ Update SideviewApiService endpoints
4. ✅ Create UI for complete survey workflow
5. ✅ Add health map visualization
6. ✅ Implement bulk video upload with progress

### **Next Steps**

1. Update `api_endpoints.dart` with correct IP (already done ✅)
2. Fix `SideviewApiService` endpoints
3. Implement `DeekshithSurveyService`
4. Create survey workflow screens
5. Test complete flow

---

**Your backend is production-ready! Now integrate it properly in Flutter.** 🚀
