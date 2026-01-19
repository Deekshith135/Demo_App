App Routing & Screen Inventory — Farm AI Assistant

Overview

This document lists all registered app routes (from `lib/main.dart`), the screen class that handles each route, the file path, and a concise description of the screen's purpose and key behavior (inputs, navigation targets, and important functions).

Usage: open the linked files to inspect implementation details.

---

Routes (registered in `lib/main.dart`)

- Authentication

  - `/login`: LoginScreen — [lib/features/auth/screens/login_screen.dart](lib/features/auth/screens/login_screen.dart#L1-L200)
    - Purpose: User login form (phone/email depending on implementation). Handles authentication flow and on success navigates to `/dashboard`.
    - Key behavior: calls backend/auth provider, stores farmer id and navigates.
  - `/register`: RegisterScreen — [lib/features/auth/screens/register_screen.dart](lib/features/auth/screens/register_screen.dart#L1-L200)
    - Purpose: Registration UI to create a new account or farmer.
    - Key behavior: collects name/phone, calls registration API, likely uses `BackendFarmerService`.
  - `/phone-otp`: PhoneOtpScreen — [lib/features/auth/screens/phone_otp_screen.dart](lib/features/auth/screens/phone_otp_screen.dart#L1-L200)
    - Purpose: OTP verification screen used during phone login/registration.

- Onboarding

  - `/welcome`: WelcomeOnboardingScreen — [lib/features/onboarding/screens/welcome_onboarding_screen.dart](lib/features/onboarding/screens/welcome_onboarding_screen.dart#L1-L200)
    - Purpose: App onboarding intro slides / welcome flow.
  - `/farm-details`: FarmDetailsScreen — [lib/features/onboarding/screens/farm_details_screen.dart](lib/features/onboarding/screens/farm_details_screen.dart#L1-L200)
    - Purpose: Collect farm-related data (size, location, crop selection).
  - `/choose-plan`: ChoosePlanScreen — [lib/features/onboarding/screens/choose_plan_screen.dart](lib/features/onboarding/screens/choose_plan_screen.dart#L1-L200)
    - Purpose: Let user choose subscription / plan.
  - `/crop-selection`: CropSelectionScreen — [lib/features/onboarding/screens/crop_selection_screen.dart](lib/features/onboarding/screens/crop_selection_screen.dart#L1-L200)
    - Purpose: Choose crop(s) to track (e.g., coconut)

- Main features

  - `/dashboard`: DashboardScreen — [lib/features/dashboard/screens/dashboard_screen.dart](lib/features/dashboard/screens/dashboard_screen.dart#L1-L200)
    - Purpose: App home/dashboard showing key metrics and shortcuts to features.
  - `/chat`: SarvamChatScreen — [lib/features/chat/screens/sarvam_chat_screen.dart](lib/features/chat/screens/sarvam_chat_screen.dart#L1-L200)
    - Purpose: Chat interface (support or LLM chat). Connects to chat endpoints.
  - `/crop-analysis`: CropAnalysisScreen — [lib/features/crop_analysis/screens/crop_analysis_screen.dart](lib/features/crop_analysis/screens/crop_analysis_screen.dart#L1-L200)
    - Purpose: Entry to crop analysis feature; offers Top View or Side View analysis options.
    - Behavior: pressing Side View navigates to `/ml-capture`; Top View navigates to `/topview-capture`.

- ML / AI Analysis (single-image flow)

  - `/ml-capture`: MlHomeScreen — [lib/features/ml/screens/ml_home_screen.dart](lib/features/ml/screens/ml_home_screen.dart#L1-L200)
    - Purpose: ML image capture / selection screen. The app now uses `MlHomeScreen` as the single-image entry point.
    - Key behavior: picks image from camera/gallery, then calls `Ml2ApiService.predict(File)` to send an image to the ML backend and navigates to `/ml-result` with arguments `{'result': result, 'imageFile': File(...)}`.
    - Important functions: `_pickImage(ImageSource)`, `_checkBackendHealth()`, uses `Ml2ApiService.getHealth()` to show backend status.
  - `/ml-result`: MlResultScreen — [lib/features/ml/screens/ml_result_screen.dart](lib/features/ml/screens/ml_result_screen.dart#L1-L200)
    - Purpose: Display the ML prediction / diagnosis results for a given image.
    - Expected arguments: `{'result': Map<String,dynamic>, 'imageFile': File}` or `{'result': Map<String,dynamic>, 'isFromHistory': true}` when opened from history.
    - Key behavior: shows predictions, confidence, parts/status, recommendations, and may allow saving to history.

- ML / AI Analysis (top-view tree detection)

  - `/topview-capture`: TopviewCaptureScreen — [lib/features/ml/screens/topview_capture_screen.dart](lib/features/ml/screens/topview_capture_screen.dart#L1-L200)
    - Purpose: Capture/select top-down images used for tree detection.
  - `/topview-result`: TopviewResultScreen — [lib/features/ml/screens/topview_result_screen.dart](lib/features/ml/screens/topview_result_screen.dart#L1-L200)
    - Purpose: Show results for top-view detection (tree counts, positions, map overlays).

- Drone survey / video analysis (survey workflows)

  - `/drone-home`: DroneHomeScreen — [lib/features/drone/screens/drone_home_screen.dart](lib/features/drone/screens/drone_home_screen.dart#L1-L200)
    - Purpose: Entry point for drone survey features.
  - `/drone-start-survey`: StartSurveyScreen — [lib/features/drone/screens/start_survey_screen.dart](lib/features/drone/screens/start_survey_screen.dart#L1-L200)
    - Purpose: Start or configure a drone-based survey session.
  - `/drone-upload-topview`: PhotoCaptureScreen — [lib/features/drone/screens/photo_capture_screen.dart](lib/features/drone/screens/photo_capture_screen.dart#L1-L200)
    - Purpose: Upload / capture top-view photos for drone survey.
  - `/drone-topview-detected`: TopviewDetectedScreen — [lib/features/drone/screens/topview_detected_screen.dart](lib/features/drone/screens/topview_detected_screen.dart#L1-L200)
    - Purpose: Display top-view detection results within the survey flow.
  - `/drone-upload-sideview`: UploadSideviewScreen — [lib/features/drone/screens/upload_sideview_screen.dart](lib/features/drone/screens/upload_sideview_screen.dart#L1-L200)
    - Purpose: Upload side-view video for sideview analysis (used by drone survey).
  - `/drone-processing`: ProcessingScreen — [lib/features/drone/screens/processing_screen.dart](lib/features/drone/screens/processing_screen.dart#L1-L200)
    - Purpose: Screen that shows progress while server processes uploaded survey data/video.
  - `/drone-result`: SurveyResultScreen — [lib/features/drone/screens/survey_result_screen.dart](lib/features/drone/screens/survey_result_screen.dart#L1-L200)
    - Purpose: Show aggregated results of a drone survey (per-tree health, map, counts).
  - `/drone-summary`: SurveySummaryScreen — [lib/features/drone/screens/survey_summary_screen.dart](lib/features/drone/screens/survey_summary_screen.dart#L1-L200)
    - Purpose: Summarize the survey session (stats, recommendations).
  - `/drone-history`: SurveyHistoryScreen — [lib/features/drone/screens/survey_history_screen.dart](lib/features/drone/screens/survey_history_screen.dart#L1-L200)
    - Purpose: List past drone surveys.
  - `/drone-history-detail`: SurveyHistoryDetailScreen — [lib/features/drone/screens/survey_history_detail_screen.dart](lib/features/drone/screens/survey_history_detail_screen.dart#L1-L200)
    - Purpose: Detail view for a single past survey.

- Other features
  - `/history`: HistoryScreen — [lib/features/history/screens/history_screen.dart](lib/features/history/screens/history_screen.dart#L1-L200)
    - Purpose: Local analysis history (reads from local sqflite DB via `DbService`). This screen calls `Ml2ApiService.getLocalHistory()` to obtain persisted analysis items and display them. Tapping an item opens `/ml-result` with `{'result': item, 'isFromHistory': true}`.
  - `/settings`: SettingsScreen — [lib/features/settings/screens/settings_screen.dart](lib/features/settings/screens/settings_screen.dart#L1-L200)
    - Purpose: App settings; contains actions for backend health checks and maybe farmer management.
  - `/about`: AboutScreen — [lib/features/about/screens/about_screen.dart](lib/features/about/screens/about_screen.dart#L1-L200)
    - Purpose: Shows app metadata and uses `Ml2ApiService.getHealth()` to display backend health.
  - `/expert-connect`: ExpertConnectScreen — [lib/features/expert/screens/expert_connect_screen.dart](lib/features/expert/screens/expert_connect_screen.dart#L1-L200)
    - Purpose: Contact / request expert assistance.

---

Notes about ML services and routing consistency

- The app centralizes ML single-image flow on `MlHomeScreen` → `MlResultScreen` and uses `Ml2ApiService` for prediction and `getHealth()` checks. See:

  - `Ml2ApiService` implementation: [lib/features/ml/services/ml2_api_service.dart](lib/features/ml/services/ml2_api_service.dart#L1-L200)
  - API endpoints used in code: `ApiEndpoints.baseUrl` and `ApiEndpoints.predict` defined in [lib/core/constants/api_endpoints.dart](lib/core/constants/api_endpoints.dart#L1-L200).

- Drone-related sideview video upload remains handled by drone services and uses separate endpoints (e.g., `/api/drone/sideview`) implemented in drone services (see `lib/features/drone/services/drone_api_client.dart`). That flow is distinct from the single-image `/ml-capture` flow.

- Local history is implemented using `DbService` and `HistoryItem` model under `lib/features/history/`. `HistoryScreen` reads history via `Ml2ApiService.getLocalHistory()` (wrapper that returns DB items as maps).

---

How to use this document

- To update routing: edit `lib/main.dart` and adjust the `routes` map. Use the path and screen mapping above to locate files.
- To change ML flow endpoint or unify services: update `ApiEndpoints` (`lib/core/constants/api_endpoints.dart`) and `Ml2ApiService` or `SideviewApiService` depending on which flow you want to keep.
- To inspect an individual screen, open the linked file path; I included the most relevant line ranges.

---

If you want, I can:

- Expand each screen entry to include a function-level breakdown (public methods, lifecycle hooks, and widgets used) by reading each file and extracting docstrings and method signatures.
- Produce a visual map (graph) of routes and navigation flows.
- Remove legacy `sideview_*` screens or consolidate services to reduce confusion.

Tell me which follow-up you'd like and I'll update `APP_ROUTING.md` with more detail (I can add per-screen function lists on request).
