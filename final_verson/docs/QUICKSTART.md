# 🚀 Deekshith Quick Start Guide

## Step 1: Update Backend URL (REQUIRED)

Open `lib/core/api/deekshith_api_client.dart` and change line 9:

```dart
static const String baseUrl = "http://192.168.1.100:8000";
```

Replace `192.168.1.100` with your actual backend IP.

**Find your IP:**

- Windows: Open CMD → `ipconfig` → look for IPv4
- Mac/Linux: Terminal → `ifconfig` or `ip addr`

---

## Step 2: Install Dependencies

```bash
flutter pub get
```

---

## Step 3: Run the App

```bash
flutter run
```

---

## Step 4: Test the Flow

### Option A: Add to Existing Dashboard

Find your dashboard screen and add this button:

```dart
ElevatedButton(
  onPressed: () {
    Navigator.pushNamed(context, '/deekshith-survey-create');
  },
  child: const Text('Start Deekshith Survey'),
)
```

### Option B: Test Directly

Change `initialRoute` in `main.dart`:

```dart
initialRoute: '/deekshith-survey-create',
```

---

## Step 5: Complete One Survey

1. **Create Survey**

   - Enter farmer ID
   - Wait for GPS lock (green indicator)
   - Tap "Start Survey"

2. **Capture Topview**

   - Take/select drone photo
   - Choose order: a, b, or c
   - Tap "Upload & Detect Trees"
   - Wait for tree detection

3. **Upload Videos**

   - Tap "Upload All Videos (Bulk)"
   - Select N videos (N = tree count)
   - Tap "Upload X Videos"
   - Wait for processing

4. **View Results**

   - Tap "View Dashboard"
   - Check health score
   - Tap "View Health Map"
   - See green/red pins

5. **Survey Dashboard**
   - Go back to tree list
   - Tap navigation to survey dashboard
   - See overall statistics

---

## 🔴 Common Issues

### "Connection refused"

→ Backend not running. Start it:

```bash
cd Deekshith
python main.py
```

### GPS not working

→ Grant location permissions in phone settings

### Videos won't upload

→ Check file size limits in backend config

---

## 📝 What Each Screen Does

| Screen            | Purpose                    |
| ----------------- | -------------------------- |
| Survey Create     | Start new farmer visit     |
| Topview Capture   | Upload drone photo         |
| Tree List         | Shows detected trees       |
| Video Upload      | Record/upload tree video   |
| Bulk Upload       | Upload many videos at once |
| Health Map        | Visual green/red map       |
| Topview Dashboard | Stats for one topview      |
| Survey Dashboard  | Stats for entire survey    |

---

## ✅ Success Criteria

You've successfully integrated Deekshith when:

- ✅ Survey creates with real GPS coordinates
- ✅ Topview uploads and detects trees (count shows)
- ✅ Videos upload and generate health results
- ✅ Health map shows green/red pins
- ✅ Dashboard displays correct percentages

---

## 🎯 Next Steps After Testing

1. **Style Integration**

   - Match your app's color scheme
   - Update AppBar colors to match theme
   - Adjust button styles

2. **Add to Main Flow**

   - Add "Deekshith Survey" option in dashboard
   - Link from existing drone features
   - Add to navigation drawer

3. **Production Setup**

   - Replace development IP with production URL
   - Add authentication tokens
   - Enable error logging (Firebase Crashlytics)

4. **Field Testing**
   - Test with real drone images
   - Test with actual tree videos
   - Verify offline queue works

---

## 🆘 Need Help?

Check the full documentation: `DEEKSHITH_FLUTTER_README.md`

---

**That's it! You now have a fully functional agricultural survey system.**
