# Automatic Farmer ID Assignment - Implementation Guide

## Overview

This system automatically assigns unique farmer IDs to users upon registration/login and syncs them with the backend database. Users no longer need to manually enter their farmer ID.

## Architecture

### Backend (FastAPI + PostgreSQL)

- **Database**: `farmers` table with auto-incrementing `id` (primary key)
- **Endpoints**:
  - `POST /api/farmer/create` - Register new farmer, returns auto-assigned ID
  - `GET /api/farmer/{farmer_id}` - Get farmer details by ID
  - `GET /api/farmer/all` - List all farmers
  - `GET /api/farmer/{farmer_id}/surveys` - Get farmer's surveys

### Flutter App

- **FarmerService**: Local storage for farmer data (SharedPreferences)
- **BackendFarmerService**: API client for backend communication
- **Auto-registration**: Triggered after Firebase authentication success

## How It Works

### 1. User Registration Flow

```
User registers → Firebase Auth → Auto-register with backend → Save farmer_id locally
```

**Implementation**:

- `register_screen.dart`: After successful Firebase registration
  - Calls `BackendFarmerService.registerFarmer(name, phone)`
  - Backend creates farmer record with auto-assigned ID
  - Service automatically saves ID to `FarmerService`
  - User proceeds to onboarding with farmer_id ready

### 2. User Login Flow

```
User logs in → Firebase Auth → Check local farmer_id → If missing, register with backend
```

**Implementation**:

- `login_screen.dart`: After successful Firebase login
  - Checks if `FarmerService.getFarmerId()` returns null
  - If null, registers user with backend
  - Backend assigns unique ID
  - ID saved locally for future API calls

### 3. Phone OTP Flow

```
User verifies phone → Firebase Auth → Auto-register with backend → Save farmer_id
```

**Implementation**:

- `phone_otp_screen.dart`: After OTP verification
  - Extracts phone number from Firebase user
  - Registers with backend using phone as identifier
  - Saves farmer_id locally

## Code Components

### BackendFarmerService

**Location**: `lib/features/settings/services/backend_farmer_service.dart`

**Key Methods**:

```dart
// Register new farmer - auto-saves farmer_id locally
static Future<Map<String, dynamic>> registerFarmer({
  required String name,
  String? phone,
})

// Get farmer details by ID
static Future<Map<String, dynamic>> getFarmerDetails({
  required int farmerId,
})

// Check if farmer exists in backend
static Future<bool> farmerExists({required int farmerId})

// Sync local data with backend
static Future<bool> syncLocalWithBackend()
```

### Modified Screens

#### 1. login_screen.dart

- Added `_registerFarmerIfNeeded(User? user)` method
- Calls after successful email/Google login
- Checks if farmer_id exists locally
- Registers with backend if missing

#### 2. register_screen.dart

- Added backend registration after Firebase signup
- Uses display name from registration form
- Silent fail if backend unavailable (user can continue)

#### 3. phone_otp_screen.dart

- Added backend registration after OTP verification
- Uses phone number as identifier
- Generates name from phone if no display name

## Testing

### Prerequisites

1. **Start Backend**:

   ```bash
   cd c:\dev\backend
   python -m uvicorn main:app --reload
   ```

   Backend runs on: http://localhost:8000

2. **Check Database**:
   - PostgreSQL running on port 5432
   - Database: `vaayu_drishti`
   - Table: `farmers` (id, name, phone, created_at)

### Test Scenarios

#### Test 1: New User Registration

1. Open app → Navigate to Register screen
2. Enter name, email, password
3. Click "Sign Up"
4. **Expected**:
   - Firebase creates user
   - Backend creates farmer record
   - farmer_id saved locally
   - Redirects to welcome screen

**Verify**:

```bash
# Check database
psql -U postgres -d vaayu_drishti
SELECT * FROM farmers ORDER BY created_at DESC LIMIT 1;

# Check backend API
curl http://localhost:8000/api/farmer/all
```

#### Test 2: Existing User Login

1. Open app → Navigate to Login screen
2. Enter email/password of existing user
3. Click "Sign In"
4. **Expected**:
   - If farmer_id exists locally → Skip registration
   - If farmer_id missing → Auto-register with backend
   - Redirects to dashboard

**Verify**:

```dart
// Add debug print in settings screen
final farmerId = await FarmerService.getFarmerId();
print('Farmer ID: $farmerId');
```

#### Test 3: Google Sign-In

1. Open app → Click "Sign in with Google"
2. Complete Google authentication
3. **Expected**:
   - Firebase authenticates
   - Auto-registers with backend
   - farmer_id saved locally

#### Test 4: Phone OTP Login

1. Open app → Login screen → Switch to Phone
2. Enter +91XXXXXXXXXX
3. Verify OTP code
4. **Expected**:
   - Phone verified via Firebase
   - Auto-registers with backend using phone number
   - farmer_id saved locally

### Verification Commands

**Check Backend API**:

```bash
# List all farmers
curl http://localhost:8000/api/farmer/all

# Get specific farmer
curl http://localhost:8000/api/farmer/1

# Get farmer's surveys
curl http://localhost:8000/api/farmer/1/surveys
```

**Check Local Storage** (Add to any screen):

```dart
final farmerId = await FarmerService.getFarmerId();
final farmerName = await FarmerService.getFarmerName();
print('Farmer ID: $farmerId, Name: $farmerName');
```

## Settings Screen Integration

Users can view their Farmer ID in the Settings screen:

- **Location**: Settings → Profile Section
- **Display**: Shows farmer_id with edit icon
- **Edit**: Tap edit icon to manually change ID (if needed)
- **API Sync**: Can fetch details from backend using GET endpoint

## Error Handling

### Scenario 1: Backend Unavailable

- **Behavior**: Silent fail, user can continue using app
- **Resolution**: Will auto-register on next attempt
- **User Impact**: None (features work with local data)

### Scenario 2: Duplicate Registration Attempt

- **Backend**: Returns existing farmer data
- **App**: Uses existing farmer_id
- **User Impact**: None (seamless)

### Scenario 3: Network Error

- **Behavior**: Exception caught, logged to debug console
- **Resolution**: User can manually set farmer_id in Settings
- **User Impact**: May need to retry or set manually

## API Usage in Other Features

### Drone Survey Creation

```dart
// Example: Creating survey requires farmer_id
final farmerId = await FarmerService.getFarmerId();
if (farmerId == null) {
  // Show error: "Please login first"
  return;
}

final response = await http.post(
  Uri.parse('http://localhost:8000/api/survey/create'),
  body: jsonEncode({
    'farmer_id': farmerId,  // Auto-assigned ID
    'land_location': location,
    'total_trees': treeCount,
  }),
);
```

### Sideview Analysis

```dart
// Example: Analyzing video requires farmer_id
final farmerId = await FarmerService.getFarmerId();
final formData = FormData.fromMap({
  'farmer_id': farmerId,  // Auto-assigned ID
  'survey_id': surveyId,
  'video': await MultipartFile.fromFile(videoPath),
});
```

## Migration from Manual to Auto-Assignment

### For Existing Users

If users already have manually entered farmer IDs:

1. **Keep existing IDs**: `FarmerService.getFarmerId()` returns stored ID
2. **Validate with backend**: Call `BackendFarmerService.farmerExists()`
3. **Sync if invalid**: If not found, re-register with backend

### Cleanup Old Manual Entry Code

The manual Farmer ID entry in Settings is now optional:

- Kept for backward compatibility
- Users can manually override if needed
- New users get ID automatically

## Database Schema

### farmers table

```sql
CREATE TABLE farmers (
    id SERIAL PRIMARY KEY,           -- Auto-incrementing unique ID
    name VARCHAR NOT NULL,            -- Farmer's name
    phone VARCHAR,                    -- Phone number (optional)
    created_at TIMESTAMP DEFAULT NOW() -- Registration timestamp
);
```

### surveys table

```sql
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    farmer_id INTEGER REFERENCES farmers(id), -- Foreign key to farmers
    land_location VARCHAR,
    total_trees INTEGER,
    topview_image_path VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Troubleshooting

### Issue: farmer_id is null after login

**Check**:

1. Backend running? `curl http://localhost:8000/health`
2. Database accessible? `psql -U postgres -d vaayu_drishti`
3. Firebase authentication successful?
4. Network connectivity?

**Solution**:

- Check debug logs for "Failed to register farmer"
- Manually test API: `curl -X POST http://localhost:8000/api/farmer/create -H "Content-Type: application/json" -d '{"name":"Test","phone":"123"}'`
- Verify farmer_router.py is imported in main.py

### Issue: Duplicate farmers created

**Cause**: No check for existing user before registration

**Solution**: Update BackendFarmerService to check email/phone before creating:

```dart
// Check if farmer exists by email/phone
final exists = await checkFarmerByEmail(email);
if (!exists) {
  await registerFarmer(name, phone);
}
```

### Issue: Settings screen shows "Not set"

**Check**:

1. User logged in? `await FarmerService.isLoggedIn()`
2. farmer_id stored? `await FarmerService.getFarmerId()`
3. Data persisted? Check SharedPreferences

**Solution**:

- Force re-registration: Clear app data and login again
- Manual entry: Use edit icon in Settings to set ID
- Sync with backend: Call `BackendFarmerService.syncLocalWithBackend()`

## Future Enhancements

### 1. Email/Phone Uniqueness

- Add unique constraints on email/phone in backend
- Check for existing user before creating duplicate
- Return existing farmer_id if user already registered

### 2. Profile Sync

- Add PUT /api/farmer/{id} endpoint to update farmer details
- Sync name/phone changes from Settings to backend
- Show last sync timestamp in Settings

### 3. Offline Support

- Queue registration requests when offline
- Retry when network available
- Show sync status indicator

### 4. Backend Authentication

- Add JWT token authentication to farmer endpoints
- Verify user owns farmer_id before accessing data
- Prevent unauthorized access to other farmers' data

## Summary

✅ **Auto-assignment**: Unique farmer_id assigned on registration/login
✅ **Backend sync**: All farmer data stored in PostgreSQL
✅ **Local storage**: farmer_id cached for offline access
✅ **GET endpoint**: Retrieve farmer details via `/api/farmer/{id}`
✅ **Multiple auth methods**: Email, Google, Phone OTP all supported
✅ **Error handling**: Graceful fallback if backend unavailable
✅ **Settings integration**: View and edit farmer_id in Settings screen

Users no longer need to manually enter farmer IDs. The system handles everything automatically!
