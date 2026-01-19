# 🗺️ Complete App Routing Guide - Farm AI Assistant

## 🎉 RECENT REFACTORING - Clean Architecture Implementation

**Date:** January 6, 2026  
**Major Update:** ML Module Simplified & Restructured

### What Changed:

✅ **Eliminated Confusion** - Removed duplicate and unused ML screens  
✅ **Clean Architecture** - Proper separation of concerns  
✅ **Unified Sideview** - Single screen handles both image AND video capture  
✅ **Better Naming** - `/sideview-capture` and `/sideview-result` instead of `/ml-capture`  
✅ **Reduced Complexity** - From 7 screens down to 4 screens

### Old Structure (DEPRECATED):

```
❌ /ml-capture → MlHomeScreen
❌ /ml-result → MlResultScreen
❌ sideview_image_capture_screen.dart (unused)
❌ sideview_video_capture_screen.dart (unused)
❌ sideview_result_screen.dart (old unused)
```

### New Structure (ACTIVE):

```
✅ /sideview-capture → SideviewCaptureScreen (image + video)
✅ /sideview-result → SideviewResultScreen (unified results)
✅ /topview-capture → TopviewCaptureScreen (tree detection)
✅ /topview-result → TopviewResultScreen (tree counts)
```

---

## 📋 Table of Contents

1. [Application Entry Point](#application-entry-point)
2. [Authentication Flow](#authentication-flow)
3. [Onboarding Flow](#onboarding-flow)
4. [Main Dashboard](#main-dashboard)
5. [ML Analysis Module](#ml-analysis-module)
6. [Drone Survey System](#drone-survey-system)
7. [Deekshith Survey System](#deekshith-survey-system)
8. [Other Features](#other-features)
9. [Backend API Endpoints](#backend-api-endpoints)

---

## 🚀 Application Entry Point

**File:** `lib/main.dart`

**Initial Route:** `/dashboard`

**Providers:**

- `LanguageProvider` - Manages app language (English/Kannada)
- `DroneSurveyProvider` - Manages drone survey state

---

## 🔐 Authentication Flow

### Route: `/login`

**Screen:** `LoginScreen`
**File:** `lib/features/auth/screens/login_screen.dart`
**Purpose:** User login with email/phone
**Navigation:**

- ➡️ `/phone-otp` - After entering phone number
- ➡️ `/register` - New user registration
- ➡️ `/dashboard` - After successful login

### Route: `/phone-otp`

**Screen:** `PhoneOtpScreen`
**File:** `lib/features/auth/screens/phone_otp_screen.dart`
**Purpose:** OTP verification
**Navigation:**

- ➡️ `/dashboard` - After OTP verification

### Route: `/register`

**Screen:** `RegisterScreen`
**File:** `lib/features/auth/screens/register_screen.dart`
**Purpose:** New user registration
**Navigation:**

- ➡️ `/welcome` - After registration

---

## 🌱 Onboarding Flow

### Route: `/welcome`

**Screen:** `WelcomeOnboardingScreen`
**File:** `lib/features/onboarding/screens/welcome_onboarding_screen.dart`
**Purpose:** Welcome screen with app introduction
**Navigation:**

- ➡️ `/farm-details` - Start onboarding

### Route: `/farm-details`

**Screen:** `FarmDetailsScreen`
**File:** `lib/features/onboarding/screens/farm_details_screen.dart`
**Purpose:** Enter farm details (size, location, etc.)
**Navigation:**

- ➡️ `/crop-selection` - After farm details submission

### Route: `/crop-selection`

**Screen:** `CropSelectionScreen`
**File:** `lib/features/onboarding/screens/crop_selection_screen.dart`
**Purpose:** Select crop types (coconut, arecanut, etc.)
**Navigation:**

- ➡️ `/dashboard` - Complete onboarding

### Route: `/choose-plan`

**Screen:** `ChoosePlanScreen`
**File:** `lib/features/onboarding/screens/choose_plan_screen.dart`
**Purpose:** Select subscription plan
**Navigation:**

- ➡️ `/crop-selection` - After plan selection

---

## 🏠 Main Dashboard

### Route: `/dashboard`

**Screen:** `DashboardScreen`
**File:** `lib/features/dashboard/screens/dashboard_screen.dart`
**Purpose:** Main hub with 4 quick action cards
**Navigation:**

**Quick Actions:**

1. **Analyze Crop** ➡️ `/crop-analysis`
2. **Disease Detection** ➡️ `/sideview-capture` ✨ NEW
3. **Drone Survey** ➡️ `/drone-home`
4. **Expert Connect** ➡️ `/expert-connect`

**Bottom Navigation Bar:**

1. **Home** - Current screen
2. **History** ➡️ `/history`
3. **Chat** ➡️ `/chat`
4. **Settings** ➡️ `/settings`

---

## 🔬 ML Analysis Module

## 🔬 ML Analysis Module - CLEAN ARCHITECTURE ✨

### Overview

**REFACTORED:** The ML module now has a clean, simplified structure following clean architecture principles.

**Two Independent Modules:**

1. **Sideview Module** - Disease detection from side photos/videos
   - `sideview_capture_screen.dart` - Unified capture (handles both image AND video)
   - `sideview_result_screen_new.dart` - Display results for both types
2. **Topview Module** - Tree detection from overhead photos
   - `topview_capture_screen.dart` - Capture overhead image
   - `topview_result_screen.dart` - Display tree count

**Architecture Benefits:**

- ✅ Clean separation of concerns
- ✅ Single responsibility per screen
- ✅ Reusable service layer
- ✅ No duplicate screens
- ✅ Consistent naming

---

### Route: `/sideview-capture` ✨ NEW

**Screen:** `SideviewCaptureScreen`
**File:** `lib/features/ml/screens/sideview_capture_screen.dart`
**Purpose:** Unified disease detection - capture photos OR videos
**API Called:**

- Image: `POST /sideview/predict_image` via `SideviewApiService.analyzeImage()`
- Video: `POST /sideview/process_video` via `SideviewApiService.analyzeVideo()`

**Navigation:**

- ➡️ `/sideview-result` - After analysis (with result data)

**Features:**

- ✅ Take photo from camera
- ✅ Upload photo from gallery
- ✅ Record video (1-2 minutes)
- ✅ Backend health check indicator
- ✅ Real-time analysis progress
- ✅ Auto-save to local history database

**Capture Options:**

1. **Quick Image Analysis** - Instant disease check from single photo
2. **Comprehensive Video Analysis** - Frame-by-frame analysis (1-5 min processing)

**Backend APIs:**

- **Image:** `POST /sideview/predict_image`
  - Returns: `{prediction: {status: {...}, part: {...}}}`
- **Video:** `POST /sideview/process_video`
  - Returns: `{dashboard: {tree: {...}, parts: {...}}, predictions: [...]}`

---

### Route: `/sideview-result` ✨ NEW

**Screen:** `SideviewResultScreen`
**File:** `lib/features/ml/screens/sideview_result_screen_new.dart`
**Purpose:** Display disease detection results (image or video)
**Data Required:**

- `result` - Analysis result map
- `type` - 'image' or 'video'
- `imageFile` or `videoFile` - Original media

**Display Information:**

- 🏥 Overall health status (Healthy/Unhealthy)
- 📊 Health score percentage
- 🦠 Disease classification with confidence
- 🌴 Tree part identification (stem/leaves/bud)
- 💊 Treatment recommendations
- 📈 Video: Frame-by-frame dashboard summary

**Navigation:**

- ➡️ `/chat` - Ask AI assistant
- ➡️ `/expert-connect` - Contact expert
- ➡️ `/history` - View history
- ⬅️ Back to capture screen

**Clean Architecture Benefits:**

- Handles both image and video results intelligently
- Smart data extraction based on type
- Auto-generates disease-specific recommendations
- Pure presentation layer - no business logic

---

### Route: `/topview-capture`

**Screen:** `TopviewCaptureScreen`
**File:** `lib/features/ml/screens/topview_capture_screen.dart`
**Purpose:** Capture overhead/topview image for tree detection
**API Called:** `POST /topview/detect`
**Navigation:**

- ➡️ `/topview-result` - After tree detection

**Backend API:**

- **Endpoint:** `POST /topview/detect`
- **Service:** `TopviewApiService.detectTrees()`
- **Returns:** Tree count and bounding boxes

---

### Route: `/topview-result`

**Screen:** `TopviewResultScreen`
**File:** `lib/features/ml/screens/topview_result_screen.dart`
**Purpose:** Display tree detection results
**Data Required:**

- Tree count
- Detection image with bounding boxes

**Display Information:**

- 🌴 Total trees detected
- 📷 Annotated image with tree markers
- 📊 Detection confidence

---

### 🗂️ Old ML Screens (DEPRECATED)

**⚠️ These screens are no longer used after refactoring:**

- ❌ `ml_home_screen.dart` - Replaced by `sideview_capture_screen.dart`
- ❌ `ml_result_screen.dart` - Replaced by `sideview_result_screen_new.dart`
- ❌ `sideview_image_capture_screen.dart` - Merged into unified capture screen
- ❌ `sideview_video_capture_screen.dart` - Merged into unified capture screen
- ❌ `sideview_result_screen.dart` (old) - Replaced by new version

**✅ Clean Architecture Achievement:**

- Reduced 7 screens to 4 screens
- Eliminated duplication
- Clear separation: Sideview vs Topview
- Single screen handles image+video (sideview)

---

## 🚁 Drone Survey System (Old Flow)

### Route: `/drone-home`

**Screen:** `DroneHomeScreen`
**File:** `lib/features/drone/screens/drone_home_screen.dart`
**Purpose:** Drone survey landing page
**Navigation:**

- ➡️ `/drone-start-survey` - Start new survey
- ➡️ `/drone-history` - View past surveys

---

### Route: `/drone-start-survey`

**Screen:** `StartSurveyScreen`
**File:** `lib/features/drone/screens/start_survey_screen.dart`
**Purpose:** Initialize survey with farmer ID and location
**API Called:** `POST /api/survey/start` ⚠️ **Returns 404**
**Navigation:**

- ➡️ `/drone-upload-topview` - After survey start

**Form Fields:**

- Farmer ID (auto-filled if saved)
- GPS Location (auto-captured)

---

### Route: `/drone-upload-topview`

**Screen:** `PhotoCaptureScreen`
**File:** `lib/features/drone/screens/photo_capture_screen.dart`
**Purpose:** Upload overhead/drone photo
**API Called:** `POST /topview/detect/image`
**Navigation:**

- ➡️ `/drone-topview-detected` - After upload

---

### Route: `/drone-topview-detected`

**Screen:** `TopviewDetectedScreen`
**File:** `lib/features/drone/screens/topview_detected_screen.dart`
**Purpose:** Review detected trees from topview
**Navigation:**

- ➡️ `/drone-upload-sideview` - Proceed to sideview

**Display:**

- Annotated image with tree detections
- Tree count

---

### Route: `/drone-upload-sideview`

**Screen:** `UploadSideviewScreen`
**File:** `lib/features/drone/screens/upload_sideview_screen.dart`
**Purpose:** Upload sideview videos for each tree
**API Called:** `POST /sideview/analyze` ⚠️ **Returns 404**
**Navigation:**

- ➡️ `/drone-processing` - After uploads

---

### Route: `/drone-processing`

**Screen:** `ProcessingScreen`
**File:** `lib/features/drone/screens/processing_screen.dart`
**Purpose:** Show processing progress
**Navigation:**

- ➡️ `/drone-result` - After processing complete

---

### Route: `/drone-result`

**Screen:** `SurveyResultScreen`
**File:** `lib/features/drone/screens/survey_result_screen.dart`
**Purpose:** Display individual tree results
**Navigation:**

- ➡️ `/drone-summary` - View summary

---

### Route: `/drone-summary`

**Screen:** `SurveySummaryScreen`
**File:** `lib/features/drone/screens/survey_summary_screen.dart`
**Purpose:** Overall survey summary and health metrics
**Navigation:**

- ➡️ `/drone-home` - Return home
- ➡️ `/drone-history` - View history

---

### Route: `/drone-history`

**Screen:** `SurveyHistoryScreen`
**File:** `lib/features/drone/screens/survey_history_screen.dart`
**Purpose:** List of all completed surveys
**Navigation:**

- ➡️ `/drone-history-detail` - View specific survey
- ➡️ `/drone-home` - Back to home

---

### Route: `/drone-history-detail`

**Screen:** `SurveyHistoryDetailScreen`
**File:** `lib/features/drone/screens/survey_history_detail_screen.dart`
**Purpose:** Detailed view of completed survey

---

## 🆕 Deekshith Survey System (New Flow)

### Overview

**Complete backend-integrated survey system with full traceability**

### Route: `/deekshith-survey-create`

**Screen:** `DeekshithSurveyCreateScreen`
**File:** `lib/features/drone/screens/deekshith_survey_create_screen.dart`
**Purpose:** Create new survey with farmer ID and GPS
**API Called:** `POST /survey/create`
**Service:** `DeekshithSurveyService.createSurvey()`
**Navigation:**

- ➡️ `DeekshithTopviewCaptureScreen` (with surveyId, farmerId)

**Features:**

- Auto GPS capture
- Farmer ID input
- Creates survey record on backend
- Returns unique surveyId

---

### Screen: `DeekshithTopviewCaptureScreen`

**File:** `lib/features/drone/screens/deekshith_topview_capture_screen.dart`
**Purpose:** Capture and upload topview images (multi-topview support)
**API Called:** `POST /survey/{surveyId}/topview`
**Service:** `DeekshithSurveyService.uploadTopview()`
**Navigation:**

- ➡️ `DeekshithTreeListScreen` (after tree detection)

**Parameters:**

- `surveyId` - Survey identifier
- `farmerId` - Farmer identifier
- `topviewOrder` - "a", "b", "c" (multiple topviews per survey)

**Backend Response:**

- `topview_id` - Unique topview identifier
- `tree_count` - Number of detected trees
- `detection_image_url` - Annotated image

---

### Screen: `DeekshithTreeListScreen`

**File:** `lib/features/drone/screens/deekshith_tree_list_screen.dart`
**Purpose:** Display detected trees as a list/grid
**Navigation:**

- ➡️ `DeekshithVideoUploadScreen` (single tree)
- ➡️ `DeekshithBulkVideoUploadScreen` (multiple trees)
- ➡️ `DeekshithHealthMapScreen` (after all uploads)

**Parameters:**

- `surveyId`
- `topviewOrder`
- `topviewId`
- `treeCount`

**Features:**

- Shows Tree 1, Tree 2, Tree 3, etc.
- Upload individual or bulk videos
- Track upload status per tree

---

### Screen: `DeekshithVideoUploadScreen`

**File:** `lib/features/drone/screens/deekshith_video_upload_screen.dart`
**Purpose:** Upload single tree sideview video
**API Called:** `POST /survey/{surveyId}/topview/{topviewOrder}/tree/{treeIndex}/video`
**Service:** `DeekshithSurveyService.uploadTreeVideo()`
**Navigation:**

- ⬅️ Back to tree list

**Parameters:**

- `surveyId`
- `topviewOrder`
- `treeIndex` (1, 2, 3...)

**Backend Response:**

- Disease detection results
- Health metrics

---

### Screen: `DeekshithBulkVideoUploadScreen`

**File:** `lib/features/drone/screens/deekshith_bulk_video_upload_screen.dart`
**Purpose:** Upload multiple tree videos at once
**API Called:** `POST /survey/{surveyId}/topview/{topviewOrder}/trees/videos/bulk`
**Service:** `DeekshithSurveyService.uploadTreeVideosBulk()`
**Navigation:**

- ➡️ `DeekshithHealthMapScreen` (after processing)

**Parameters:**

- `surveyId`
- `topviewOrder`
- `treeIndices` (e.g., [1,2,3])
- `videos` (list of video files)

---

### Screen: `DeekshithHealthMapScreen`

**File:** `lib/features/drone/screens/deekshith_health_map_screen.dart`
**Purpose:** Visual health map of trees
**API Called:** `POST /survey/{surveyId}/topview/{topviewOrder}/dashboard`
**Service:** `DeekshithSurveyService.generateTopviewDashboard()`
**Navigation:**

- ➡️ `DeekshithTopviewDashboardScreen`

**Parameters:**

- `surveyId`
- `topviewOrder`

**Display:**

- Color-coded tree health (green/yellow/red)
- Interactive health map

---

### Screen: `DeekshithTopviewDashboardScreen`

**File:** `lib/features/drone/screens/deekshith_topview_dashboard_screen.dart`
**Purpose:** Topview-level statistics and charts
**Navigation:**

- ➡️ `DeekshithSurveyDashboardScreen` (if all topviews complete)
- ⬅️ Add another topview

**Parameters:**

- `surveyId`
- `topviewOrder`

**Display:**

- Tree count
- Health distribution
- Disease percentages
- Per-topview metrics

---

### Screen: `DeekshithSurveyDashboardScreen`

**File:** `lib/features/drone/screens/deekshith_survey_dashboard_screen.dart`
**Purpose:** Final survey-level dashboard (all topviews aggregated)
**API Called:** `POST /survey/{surveyId}/dashboard`
**Service:** `DeekshithSurveyService.generateSurveyDashboard()`

**Parameters:**

- `surveyId`

**Display:**

- Total trees across all topviews
- Overall health score
- Complete disease distribution
- Recommendations

---

## 💬 Chat & Expert Features

### Route: `/chat`

**Screen:** `SarvamChatScreen`
**File:** `lib/features/chat/screens/sarvam_chat_screen.dart`
**Purpose:** AI-powered chat assistant (multilingual)
**API Called:** `POST /chat/llm`
**Backend:** Sarvam AI integration

**Features:**

- English and Kannada support
- Voice input (speech-to-text)
- Text-to-speech output
- Context-aware farming advice

---

### Route: `/expert-connect`

**Screen:** `ExpertConnectScreen`
**File:** `lib/features/expert/screens/expert_connect_screen.dart`
**Purpose:** Connect with agricultural experts
**API Called:** `POST /expert/ticket`

**Features:**

- Submit help requests
- Upload problem images
- Expert ticket system

---

### Route: `/crop-analysis`

**Screen:** `CropAnalysisScreen`
**File:** `lib/features/crop_analysis/screens/crop_analysis_screen.dart`
**Purpose:** Crop health analysis tools

---

## 📜 Other Routes

### Route: `/history`

**Screen:** `HistoryScreen`
**File:** `lib/features/history/screens/history_screen.dart`
**Purpose:** View past ML analyses and surveys
**Data Source:** Local SQLite database (`DbService`)
**Navigation:**

- ➡️ `/ml-result` - Re-view past analysis

---

### Route: `/settings`

**Screen:** `SettingsScreen`
**File:** `lib/features/settings/screens/settings_screen.dart`
**Purpose:** App settings and preferences
**Navigation:**

- ➡️ `/about` - About page
- ➡️ `/login` - Logout

**Settings:**

- Language selection (English/Kannada)
- Farmer profile
- Account management

---

### Route: `/about`

**Screen:** `AboutScreen`
**File:** `lib/features/about/screens/about_screen.dart`
**Purpose:** App information and credits

---

## 🌐 Backend API Endpoints

### Current Configuration

**File:** `lib/core/constants/api_endpoints.dart`

**Base URL:** `http://10.57.117.58:8000`

### API Endpoints List

#### Health Check

- `GET /health` ✅ Working

#### ML/Analysis Endpoints

- `POST /topview/analyze` ⚠️ Not used
- `POST /topview/detect` ✅ Working
- `POST /topview/detect/image` ✅ Working
- `POST /sideview/analyze` ❌ **Returns 404**
- `POST /sideview/analyze-video` ⚠️ Not used

#### Farmer Endpoints

- `GET /api/farmer/{id}` ❌ **Returns 404**
- `POST /api/farmer/create` ⚠️ Not implemented
- `PUT /api/farmer/update` ⚠️ Not implemented
- `GET /api/farmer/list` ⚠️ Not implemented

#### Survey Endpoints (Old)

- `POST /api/survey/start` ❌ **Returns 404**
- `POST /api/survey/submit` ⚠️ Not implemented
- `GET /api/survey/history` ⚠️ Not implemented

#### Deekshith Survey Endpoints (New)

- `POST /survey/create` ⚠️ Need to verify
- `POST /survey/list` ⚠️ Need to verify
- `POST /survey/{surveyId}/full-result` ⚠️ Need to verify
- `POST /survey/{surveyId}/topview` ⚠️ Need to verify
- `POST /survey/{surveyId}/topview/{order}/tree/{index}/video` ⚠️ Need to verify
- `POST /survey/{surveyId}/topview/{order}/trees/videos/bulk` ⚠️ Need to verify
- `POST /survey/{surveyId}/topview/{order}/dashboard` ⚠️ Need to verify
- `POST /survey/{surveyId}/dashboard` ⚠️ Need to verify

#### Chat Endpoints

- `POST /chat/llm` ✅ Working
- `GET /chat/history` ⚠️ Not used

#### Expert Endpoints

- `POST /expert/ticket` ⚠️ Not implemented

---

## ⚠️ Known Issues & Confusion Points

### 1. ML Module Confusion

**Problem:** Multiple screens but unclear routing

- `ml_home_screen.dart` - Main entry (used)
- `ml_result_screen.dart` - Results display (used)
- `sideview_image_capture_screen.dart` - NOT ROUTED
- `sideview_video_capture_screen.dart` - NOT ROUTED
- `sideview_result_screen.dart` - NOT ROUTED
- `topview_capture_screen.dart` - Separate route `/topview-capture`
- `topview_result_screen.dart` - Separate route `/topview-result`

**Recommendation:**

- Remove unused sideview screens OR
- Add proper routing for complete flow

### 2. Two Survey Systems

**Problem:** Both old and new survey flows exist

**Old System:**

- `/drone-start-survey` → `/drone-upload-topview` → etc.
- Uses `DroneSurveyProvider`
- ❌ Backend endpoints return 404

**New System (Deekshith):**

- `/deekshith-survey-create` → Navigator.push with parameters
- Uses `DeekshithSurveyService`
- ✅ Proper backend integration

**Recommendation:**

- Deprecate old drone system
- Use Deekshith system as primary

### 3. Missing Backend Routes

Several frontend routes call non-existent backend endpoints:

- `/api/farmer/{id}` - 404
- `/api/survey/start` - 404
- `/sideview/analyze` - 404

**Fix:** Implement these backend routes or remove frontend calls

### 4. Named Routes vs Navigator.push

**Inconsistency:**

- Dashboard uses named routes (`Navigator.pushNamed`)
- Deekshith system uses `Navigator.push` with MaterialPageRoute

**Recommendation:** Standardize on named routes with argument passing

---

## 🎯 Usage Flow Examples

### Example 1: Quick Disease Check (NEW FLOW) ✨

```
Dashboard → Disease Detection → Take Photo → View Results → Chat/Expert
/dashboard → /sideview-capture → /sideview-result → /chat
```

### Example 2: Video Analysis (NEW FLOW) ✨

```
Dashboard → Disease Detection → Record Video → View Results
/dashboard → /sideview-capture → /sideview-result
```

### Example 3: Full Survey (Deekshith)

```
Dashboard → Deekshith Survey Create → Enter Farmer ID + GPS
→ Topview Capture → Upload Drone Photo
→ Tree List → Trees Detected
→ Video Upload → Record Tree Videos
→ Health Map → Visual Tree Health
→ Topview Dashboard → Statistics
→ (Repeat for topview b, c...)
→ Survey Dashboard → Final Report
```

### Example 4: View History

```
Dashboard → History → Select Past Analysis → View Results
/dashboard → /history → /sideview-result
```

---

## 📊 Route Summary

| Category        | Route Count | Working Status              |
| --------------- | ----------- | --------------------------- |
| Auth            | 3           | ✅ Complete                 |
| Onboarding      | 4           | ✅ Complete                 |
| Dashboard       | 1           | ✅ Complete                 |
| ML Analysis     | 4           | ⚠️ Partial (unused screens) |
| Drone (Old)     | 10          | ❌ Backend issues           |
| Deekshith (New) | 8           | ⚠️ Needs testing            |
| Chat/Expert     | 2           | ✅ Working                  |
| Settings/Other  | 3           | ✅ Complete                 |
| **TOTAL**       | **35**      | **Mixed**                   |

---

## 🔧 Recommendations

1. **Clean up ML module** - Remove or route unused screens
2. **Deprecate old drone system** - Remove `/drone-*` routes or fix backend
3. **Add missing backend endpoints** - Implement 404 routes
4. **Standardize navigation** - Use consistent routing method
5. **Document Deekshith flow** - Add user guide for new system
6. **Test all routes** - Verify each navigation path works

---

**Last Updated:** January 6, 2026
**App Version:** Final Version
**Backend:** http://10.57.117.58:8000
