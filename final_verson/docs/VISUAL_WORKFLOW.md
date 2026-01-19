# 📊 Deekshith System - Complete Visual Workflow

## 🎯 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEEKSHITH SYSTEM                             │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Flutter    │───▶│   Backend    │───▶│      ML      │     │
│  │     App      │◀───│   FastAPI    │◀───│   Services   │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│   Orchestration       Coordination        • Topview YOLO      │
│   Visualization       Storage             • Sideview Disease  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Complete Survey Workflow

### Step 1: Create Survey

```
┌──────────────────────────────────┐
│  DeekshithSurveyCreateScreen     │
├──────────────────────────────────┤
│  👤 Input: Farmer ID             │
│  📍 Auto: GPS Location           │
│  ✅ Action: Create Survey        │
└─────────────┬────────────────────┘
              │
              ▼
      📋 survey_id = 17
              │
              ▼
```

### Step 2: Capture Topview (Drone Image)

```
┌──────────────────────────────────┐
│ DeekshithTopviewCaptureScreen    │
├──────────────────────────────────┤
│  📷 Input: Drone Photo           │
│  🔤 Select: Order (a, b, c...)   │
│  ☁️  Upload to Backend            │
└─────────────┬────────────────────┘
              │
              ▼
    Backend: YOLO Detection
    ┌─────────────────────────┐
    │  • Detect trees         │
    │  • Assign numbers 1-N   │
    │  • Store positions x,y  │
    └─────────────┬───────────┘
                  │
                  ▼
        topview_id = "17a"
        tree_count = 20
                  │
                  ▼
```

### Step 3: View Detected Trees

```
┌──────────────────────────────────┐
│    DeekshithTreeListScreen       │
├──────────────────────────────────┤
│  🌳 Tree 1  ───────────► 📹      │
│  🌳 Tree 2  ───────────► 📹      │
│  🌳 Tree 3  ───────────► 📹      │
│  ...                             │
│  🌳 Tree 20 ───────────► 📹      │
├──────────────────────────────────┤
│  [Upload All Videos (Bulk)]      │
└─────────────┬────────────────────┘
              │
              ▼
        Choose Path
              │
     ┌────────┴────────┐
     ▼                 ▼
```

### Step 4a: Single Video Upload

```
┌──────────────────────────────────┐
│  DeekshithVideoUploadScreen      │
├──────────────────────────────────┤
│  🎥 Select: Tree video           │
│  ☁️  Upload to Backend            │
└─────────────┬────────────────────┘
              │
              ▼
    Backend: Sideview ML
    ┌─────────────────────────┐
    │  • Detect diseases      │
    │  • Calculate health     │
    │  • Generate dashboard   │
    └─────────────┬───────────┘
                  │
                  ▼
        tree_dashboard.json
        {
          health: "healthy",
          reliability_score: 85,
          weighted_score: 75,
          dominant_disease: null
        }
```

### Step 4b: Bulk Video Upload

```
┌──────────────────────────────────┐
│ DeekshithBulkVideoUploadScreen   │
├──────────────────────────────────┤
│  📹 Select: Multiple videos      │
│  🔢 Auto-map: Video → Tree       │
│      Video 1 → Tree 1            │
│      Video 2 → Tree 2            │
│      ...                         │
│  ☁️  Upload all at once           │
└─────────────┬────────────────────┘
              │
              ▼
    Backend: Batch Processing
    ┌─────────────────────────┐
    │  • Process all videos   │
    │  • Generate dashboards  │
    │  • Return summary       │
    └─────────────┬───────────┘
                  │
                  ▼
        {
          processed: 18,
          failed: 2
        }
```

### Step 5: Health Map Visualization

```
┌──────────────────────────────────┐
│   DeekshithHealthMapScreen       │
├──────────────────────────────────┤
│                                  │
│    🌳 🟢 (Tree 1 - Healthy)      │
│      🟢 (Tree 2 - Healthy)       │
│    🌳 🔴 (Tree 3 - Unhealthy)    │
│        🟢 (Tree 4 - Healthy)     │
│      🔴 (Tree 5 - Unhealthy)     │
│    🌳   ⚪ (Tree 6 - No video)   │
│                                  │
│  Legend:                         │
│  🟢 Green  = Healthy (≥70%)      │
│  🔴 Red    = Unhealthy (<70%)    │
│  ⚪ Grey   = No video uploaded   │
└──────────────────────────────────┘
```

### Step 6: Topview Dashboard

```
┌──────────────────────────────────┐
│ DeekshithTopviewDashboardScreen  │
├──────────────────────────────────┤
│                                  │
│         🟢 75%                    │
│     Excellent Health             │
│                                  │
│  Total Trees:        20          │
│  Healthy:            15  🟢      │
│  Unhealthy:           5  🔴      │
│                                  │
│  Dominant Disease: Leaf Rot      │
│                                  │
│  [View Health Map]               │
└──────────────────────────────────┘
```

### Step 7: Survey Dashboard (Final)

```
┌──────────────────────────────────┐
│ DeekshithSurveyDashboardScreen   │
├──────────────────────────────────┤
│                                  │
│      Overall Farm Health         │
│            72%                   │
│                                  │
│  Topviews:           2           │
│  Total Trees:       40           │
│                                  │
│  ┌─────────────────────────────┐│
│  │  🟢 28 Healthy    70%       ││
│  │  🔴 12 Unhealthy  30%       ││
│  └─────────────────────────────┘│
│                                  │
│  Survey Summary                  │
│  ├─ Topview a: 20 trees          │
│  └─ Topview b: 20 trees          │
│                                  │
│  [Add Another Topview]           │
│  [Back to Home]                  │
└──────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA FLOW                                │
└─────────────────────────────────────────────────────────────────┘

Survey Creation
    │
    ├─→ POST /survey/create
    │       Input: {farmer_id, location{lat, lon}}
    │       Output: {survey_id}
    │
    └─→ Storage: SURVEY_17/meta.json

Topview Upload
    │
    ├─→ POST /survey/17/topview
    │       Input: image.jpg + topview_order="a"
    │       ML: YOLO detection
    │       Output: {topview_id: "17a", tree_count: 20}
    │
    └─→ Storage: SURVEY_17/topviews/17a/
                     ├─ image.jpg
                     ├─ topview_detection.json
                     └─ trees/
                           ├─ tree_01/
                           ├─ tree_02/
                           └─ ...

Sideview Upload (Single)
    │
    ├─→ POST /survey/17/topview/a/tree/1/video
    │       Input: tree_01.mp4
    │       ML: Disease detection
    │       Output: {status: "success"}
    │
    └─→ Storage: SURVEY_17/topviews/17a/trees/tree_01/
                     ├─ tree_01.mp4
                     ├─ dashboard.json
                     └─ sideview_full_result.json

Sideview Upload (Bulk)
    │
    ├─→ POST /survey/17/topview/a/trees/videos/bulk
    │       Input: [video1.mp4, video2.mp4, ...]
    │       tree_indices: "1,2,3,..."
    │       ML: Batch disease detection
    │       Output: {processed: 18, failed: 2}
    │
    └─→ Storage: Multiple tree_XX/ folders created

Dashboard Generation
    │
    ├─→ POST /survey/17/topview/a/dashboard
    │       Input: (none)
    │       Process: Aggregate all tree dashboards
    │       Output: {total_trees, healthy, unhealthy, health_score, ...}
    │
    └─→ Storage: SURVEY_17/topviews/17a/dashboard_17a.json

    │
    ├─→ POST /survey/17/dashboard
    │       Input: (none)
    │       Process: Aggregate all topview dashboards
    │       Output: {total_topviews, total_trees, overall_health_score, ...}
    │
    └─→ Storage: SURVEY_17/dashboard_17.json

Health Map
    │
    ├─→ POST /survey/17/topview/a/health-map
    │       Input: (none)
    │       Output: [{tree, x, y, health, color}, ...]
    │
    ├─→ GET /survey/17/topview/a/health-map/image
    │       Output: Annotated image (PNG/JPG)
    │
    └─→ Storage: SURVEY_17/topviews/17a/
                     ├─ health_map_17a.json
                     └─ health_map_annotated_17a.jpg
```

---

## 🔄 State Transitions

```
Survey State Machine:

    START
      │
      ├─→ CREATED (survey_id assigned)
      │       │
      │       ├─→ TOPVIEW_UPLOADED (trees detected)
      │       │       │
      │       │       ├─→ VIDEOS_UPLOADING (0 to N videos)
      │       │       │       │
      │       │       │       ├─→ VIDEOS_COMPLETE (all uploaded)
      │       │       │       │       │
      │       │       │       │       ├─→ DASHBOARD_GENERATED (stats ready)
      │       │       │       │       │       │
      │       │       │       │       │       └─→ COMPLETE ✅
      │       │       │       │       │
      │       │       │       │       └─→ PARTIAL_COMPLETE ⚠️
      │       │       │       │
      │       │       │       └─→ UPLOAD_FAILED ❌
      │       │       │
      │       │       └─→ NO_VIDEOS (can still view topview)
      │       │
      │       └─→ TOPVIEW_FAILED ❌
      │
      └─→ CREATION_FAILED ❌
```

---

## 🎨 UI/UX Flow

```
User Journey:

1. Dashboard
   │
   ├─→ [Start Deekshith Survey] button
   │
   └─→ Survey Create Screen
           │
           ├─→ Enter Farmer ID
           ├─→ Wait for GPS (automatic)
           └─→ [Start Survey] button
                   │
                   └─→ Topview Capture Screen
                           │
                           ├─→ [Camera] or [Gallery]
                           ├─→ Select order: a, b, c...
                           └─→ [Upload & Detect Trees]
                                   │
                                   └─→ Tree List Screen
                                           │
                                           ├─→ Option A: Tap individual tree
                                           │      └─→ Video Upload Screen
                                           │             └─→ Upload video
                                           │                    └─→ Back to tree list
                                           │
                                           ├─→ Option B: [Upload All Videos (Bulk)]
                                           │      └─→ Bulk Upload Screen
                                           │             └─→ Select N videos
                                           │                    └─→ Upload all
                                           │                           └─→ Success summary
                                           │
                                           └─→ [View Dashboard]
                                                   │
                                                   └─→ Topview Dashboard Screen
                                                           │
                                                           ├─→ [View Health Map]
                                                           │      └─→ Health Map Screen
                                                           │             ├─→ Server image view
                                                           │             └─→ Canvas view
                                                           │
                                                           └─→ Navigate to Survey Dashboard
                                                                   └─→ Survey Dashboard Screen
                                                                           └─→ [Back to Home]
```

---

## 📱 Screen Hierarchy

```
App
├── Login/Dashboard (existing)
│
└── Deekshith Survey System
    │
    ├── 1. Survey Create Screen
    │   └── Creates: survey_id
    │
    ├── 2. Topview Capture Screen
    │   └── Creates: topview_id, tree_count
    │
    ├── 3. Tree List Screen
    │   ├── Shows: All detected trees
    │   │
    │   ├── Branch A: Single Upload
    │   │   └── 4a. Video Upload Screen
    │   │       └── Uploads: One video at a time
    │   │
    │   └── Branch B: Bulk Upload
    │       └── 4b. Bulk Video Upload Screen
    │           └── Uploads: Multiple videos at once
    │
    ├── 5. Health Map Screen
    │   ├── Server-rendered view
    │   └── Canvas-rendered view (CustomPainter)
    │
    ├── 6. Topview Dashboard Screen
    │   └── Stats for one topview area
    │
    └── 7. Survey Dashboard Screen
        └── Aggregated stats for entire survey
```

---

## 🎯 Health Decision Logic

```
Backend Logic (Single Source of Truth):

  IF (reliability_score >= 70) AND (weighted_score >= 70)
      THEN health = "healthy" 🟢
  ELSE
      health = "unhealthy" 🔴

Flutter Logic:
  - Read health from backend
  - Display color based on health value
  - NEVER recalculate health status
```

---

## 📦 Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLUTTER APP LAYERS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                    UI LAYER (Screens)                    │   │
│  │  • Survey Create                                         │   │
│  │  • Topview Capture                                       │   │
│  │  • Tree List                                             │   │
│  │  • Video Upload (Single & Bulk)                         │   │
│  │  • Health Map (Server & Canvas)                         │   │
│  │  • Dashboards (Topview & Survey)                        │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │                                             │
│  ┌────────────────▼─────────────────────────────────────────┐   │
│  │              SERVICE LAYER                               │   │
│  │  • DeekshithSurveyService                               │   │
│  │  • OfflineQueueManager                                  │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │                                             │
│  ┌────────────────▼─────────────────────────────────────────┐   │
│  │              API CLIENT                                  │   │
│  │  • DeekshithApiClient                                    │   │
│  │    - HTTP POST (JSON)                                    │   │
│  │    - HTTP POST (Multipart)                               │   │
│  │    - HTTP GET (Images)                                   │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │                                             │
│                   ▼                                             │
│              BACKEND API                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security & Permissions

```
Required Permissions:

📍 Location (GPS)
   ├─ Android: ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
   └─ iOS: NSLocationWhenInUseUsageDescription

📷 Camera
   ├─ Android: CAMERA
   └─ iOS: NSCameraUsageDescription

📁 Storage
   ├─ Android: READ_EXTERNAL_STORAGE
   └─ iOS: NSPhotoLibraryUsageDescription

🌐 Internet
   └─ Android: INTERNET (always granted)
```

---

## ✅ Success Metrics

```
Survey Complete When:

✅ Survey created with GPS
✅ Topview uploaded → trees detected
✅ Videos uploaded (all or most)
✅ Health map generated (green/red pins visible)
✅ Dashboards display correct percentages
✅ No critical errors in logs
```

---

**This visual workflow shows exactly how data flows through the entire Deekshith system from field to dashboard.**
