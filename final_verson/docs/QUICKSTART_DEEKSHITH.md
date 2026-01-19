# 🚀 DEEKSHITH SYSTEM - QUICK START GUIDE

## ⚡ **3-MINUTE SETUP**

### **Step 1: Configure Backend URL** (30 seconds)

**File**: `lib/core/api/deekshith_api_client.dart`

```dart
class DeekshithApiClient {
  // 🔴 CHANGE THIS LINE
  static const String baseUrl = "http://192.168.1.100:8000";
  //                                    ↑↑↑↑↑↑↑↑↑↑↑
  //                              Your computer's IP
}
```

**How to find your IP:**

**Windows PowerShell:**

```powershell
ipconfig
```

Look for "IPv4 Address" (e.g., 192.168.1.100)

**Mac/Linux Terminal:**

```bash
ifconfig | grep "inet "
```

---

### **Step 2: Ensure Backend is Running** (1 minute)

```powershell
# Navigate to backend folder
cd "C:\Users\Rakshith R\Desktop\dev-cpy\Backend-backend-branch"

# Start backend server
python main.py
```

You should see:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### **Step 3: Test Flutter App** (90 seconds)

**Open in Android Studio/VS Code:**

```bash
cd "C:\Users\Rakshith R\Desktop\dev-cpy\final_verson"
flutter run
```

**Or use VS Code:**

1. Open `final_verson` folder
2. Press F5 or click "Run and Debug"
3. Select device (emulator/physical)

---

## 📱 **FIRST RUN - COMPLETE WORKFLOW**

### **1. Login** (If applicable)

- Use existing credentials
- Or skip to drone features

### **2. Navigate to Drone Survey**

```
Dashboard → Drone Survey → Start New Survey
```

### **3. Create Survey**

- Enter Farmer ID: `F001`
- Wait for GPS lock
- Click "Create Survey"
- **Result**: Survey ID created (e.g., 17)

### **4. Upload Topview**

- Click "Capture Topview Image"
- Take photo or select from gallery
- Choose order: `a`
- Click "Upload & Detect Trees"
- **Result**: Trees detected (e.g., 20 trees)

### **5. Upload Tree Videos**

**Option A: Single Upload**

- Click on "Tree 1"
- Record video (10-30 seconds)
- Upload
- Wait for processing
- **Result**: Tree health dashboard

**Option B: Bulk Upload** ⚡ (RECOMMENDED)

- Click "Bulk Upload Videos"
- Select videos from gallery
- Map videos to tree numbers
- Click "Upload All"
- **Result**: All tree dashboards at once

### **6. View Results**

- Click "Generate Dashboard"
- **Result**: Topview health stats
- Click "View Health Map"
- **Result**: Color-coded tree map

### **7. Final Dashboard**

- Click "Generate Survey Dashboard"
- **Result**: Complete farm health report

---

## 🎯 **TESTING CHECKLIST**

Use this to verify everything works:

- [ ] **Backend Connection**

  ```dart
  final service = DeekshithSurveyService();
  final connected = await service.testConnection();
  print('Connected: $connected'); // Should be true
  ```

- [ ] **Create Survey**

  - GPS location captured
  - Survey ID returned
  - No errors

- [ ] **Upload Topview**

  - Image uploaded successfully
  - Trees detected (count > 0)
  - Detection JSON saved

- [ ] **Upload Video**

  - Single video upload works
  - Tree dashboard returned
  - Health status shown

- [ ] **Bulk Upload**

  - Multiple videos uploaded
  - All processed successfully
  - Progress shown correctly

- [ ] **Dashboard Generation**

  - Stats calculated correctly
  - Health score accurate
  - Disease info shown

- [ ] **Health Map**
  - Image loaded
  - Pins colored correctly
  - Numbers visible

---

## 🔧 **COMMON ISSUES & FIXES**

### **❌ "Cannot connect to backend"**

**Solution 1**: Check backend is running

```powershell
# In backend folder
python main.py
```

**Solution 2**: Verify IP address

```powershell
ipconfig
# Update deekshith_api_client.dart with correct IP
```

**Solution 3**: Check firewall

```powershell
# Allow port 8000 through firewall
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8000
```

---

### **❌ "GPS not working"**

**Android**:
Add to `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

**iOS**:
Add to `ios/Runner/Info.plist`:

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to create surveys</string>
```

Then run:

```bash
flutter clean
flutter pub get
```

---

### **❌ "Video upload timeout"**

**Solution 1**: Increase timeout

```dart
// Already set to 120 seconds in deekshith_api_client.dart
static const Duration timeout = Duration(seconds: 120);
```

**Solution 2**: Compress videos

- Keep videos under 30 seconds
- Use lower resolution if needed

---

### **❌ "Health map not showing"**

**Solution**: Check topview detection has tree positions

```dart
// In tree dashboard, verify:
- tree_number exists
- cx, cy coordinates present
```

---

## 📊 **DEMO DATA FOR TESTING**

### **Test Farmer IDs**

```
F001 - Demo Farmer 1
F002 - Demo Farmer 2
TEST123 - Test Account
```

### **Test Workflow**

1. Create survey with `F001`
2. Upload topview (any farm image)
3. Wait for detection
4. Upload 3-5 tree videos (any coconut tree)
5. Generate dashboard
6. View health map

---

## 🎨 **UI NAVIGATION MAP**

```
App Launch
    ↓
Login Screen (/)
    ↓
Dashboard (/dashboard)
    ↓
┌────────────────────┐
│   Drone Survey     │
│   Button Click     │
└────────────────────┘
    ↓
Drone Home (/drone-home)
    ↓
┌────────────────────┐
│ Start New Survey   │
└────────────────────┘
    ↓
Survey Create (/deekshith-survey-create)
    ├─ Enter Farmer ID
    ├─ Get GPS Location
    └─ Create Survey → surveyId = 17
    ↓
Topview Capture
    ├─ Capture/Select Image
    ├─ Choose Order: a, b, c
    └─ Upload → Detection
    ↓
Tree List (20 trees detected)
    ├─ Option 1: Single Upload
    │   └─ Upload Tree Video (per tree)
    ├─ Option 2: Bulk Upload ⚡
    │   └─ Upload Multiple Videos
    ↓
Topview Dashboard
    ├─ Total: 20 trees
    ├─ Healthy: 15 (75%)
    ├─ Unhealthy: 5 (25%)
    └─ Dominant Disease: Leaf Rot
    ↓
Health Map 🗺️
    ├─ Topview Image with Pins
    ├─ Green: Healthy
    ├─ Red: Unhealthy
    └─ Grey: No Video
    ↓
Survey Dashboard (Final Report)
    ├─ All Topviews Aggregated
    ├─ Farm-Level Health
    └─ Export PDF/Share
```

---

## 🔍 **API ENDPOINT TESTING**

You can also test backend directly using Swagger UI:

**Browser**: `http://YOUR_IP:8000/docs`

Example:

```
http://192.168.1.100:8000/docs
```

This shows all API endpoints with interactive testing.

---

## 📱 **SCREEN FLOW DIAGRAM**

```
┌─────────────────────────────────────────────────┐
│         DeekshithSurveyCreateScreen            │
│  • Input: Farmer ID                             │
│  • Auto: GPS Location                           │
│  • Output: surveyId                             │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│        DeekshithTopviewCaptureScreen           │
│  • Input: Topview Image, Order (a/b/c)         │
│  • Process: ML Detection                        │
│  • Output: treeCount, detections               │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│          DeekshithTreeListScreen               │
│  • Display: All detected trees                  │
│  • Actions: Single/Bulk Upload                  │
└──────┬────────────────────────┬─────────────────┘
       ↓                        ↓
┌──────────────────┐   ┌────────────────────────┐
│ Single Upload    │   │    Bulk Upload ⚡      │
│ (Per Tree)       │   │  (Multiple Trees)      │
└─────┬────────────┘   └────────┬───────────────┘
      ↓                         ↓
      └────────┬────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│      DeekshithTopviewDashboardScreen           │
│  • Aggregate: All tree dashboards               │
│  • Display: Health stats, disease info         │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│        DeekshithHealthMapScreen                │
│  • Display: Annotated topview image             │
│  • Overlay: Color-coded health pins             │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│      DeekshithSurveyDashboardScreen            │
│  • Aggregate: All topviews                      │
│  • Display: Farm-level health                   │
│  • Export: PDF/Share Report                     │
└─────────────────────────────────────────────────┘
```

---

## 💡 **PRO TIPS**

### **1. Faster Testing**

Skip login and go directly to Deekshith:

```dart
// In main.dart, change:
initialRoute: '/deekshith-survey-create',
```

### **2. Mock Data**

For UI testing without backend:

```dart
// Create mock service
class MockDeekshithSurveyService extends DeekshithSurveyService {
  @override
  Future<int> createSurvey(...) async {
    await Future.delayed(Duration(seconds: 1));
    return 999; // Mock survey ID
  }
}
```

### **3. Debug Logging**

Add logging to API calls:

```dart
// In deekshith_api_client.dart
print('🌐 API Call: $path');
print('📤 Body: ${jsonEncode(body)}');
print('📥 Response: ${res.body}');
```

### **4. Error Tracking**

Use Firebase Crashlytics:

```dart
try {
  await service.createSurvey(...);
} catch (e, stack) {
  FirebaseCrashlytics.instance.recordError(e, stack);
  rethrow;
}
```

---

## 🎯 **SUCCESS INDICATORS**

Your integration is working when you see:

✅ **Create Survey**

```
Survey created: ID = 17
GPS: 12.971598, 77.594566
```

✅ **Upload Topview**

```
Topview uploaded: 17a
Trees detected: 20
Detection saved
```

✅ **Upload Video**

```
Video uploaded: Tree 1
Processing...
Health: healthy (Score: 85)
```

✅ **Bulk Upload**

```
Uploading 5 videos...
Success: 5/5
Failed: 0/5
```

✅ **Health Map**

```
Health map generated
Green: 15 trees
Red: 3 trees
Grey: 2 trees
```

---

## 🔥 **KEYBOARD SHORTCUTS**

**VS Code**:

- `F5` - Run app
- `Shift+F5` - Stop app
- `Ctrl+F5` - Run without debugging
- `r` in terminal - Hot reload
- `R` in terminal - Hot restart

**Android Studio**:

- `Shift+F10` - Run
- `Ctrl+F2` - Stop
- `Ctrl+\\` - Hot reload

---

## 📞 **NEED HELP?**

### **Check These Files First**

1. `DEEKSHITH_INTEGRATION_COMPLETE.md` - Full documentation
2. `lib/core/api/deekshith_api_client.dart` - HTTP client
3. `lib/features/drone/services/deekshith_survey_service.dart` - API wrapper
4. Backend: `Backend-backend-branch/Deekshith/README.md`

### **Debug Checklist**

- [ ] Backend running (`python main.py`)
- [ ] Correct IP in `deekshith_api_client.dart`
- [ ] Flutter dependencies installed (`flutter pub get`)
- [ ] Permissions granted (GPS, Camera)
- [ ] Network accessible (same WiFi)

---

## 🏆 **YOU'RE READY!**

Everything is connected and configured. Just:

1. Update backend URL with your IP
2. Start backend server
3. Run Flutter app
4. Follow the workflow

**Happy Testing!** 🚀

---

**Last Updated**: January 6, 2026  
**Status**: Production Ready  
**Setup Time**: 3 minutes
