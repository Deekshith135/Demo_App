# 🥥 Farm AI Assistant – Setup Guide for Your Friend

After cloning the GitHub repo, here's exactly what your friend needs to do to get the app running.

---

## 📋 Prerequisites (Install First)

1. **Flutter SDK** (3.9.2+)

   - https://flutter.dev/docs/get-started/install
   - Verify: `flutter --version`

2. **Python 3.8+**

   - https://www.python.org/downloads/
   - Verify: `python --version`

3. **Git**

   - https://git-scm.com/

4. **Android Emulator or Physical Device**

   - Android 7+ (API 24+)

5. **Sarvam AI API Key**
   - Sign up: https://sarvam.ai
   - Get key from dashboard

---

## 🚀 Setup Steps (Copy & Paste)

### Step 1: Clone the Repository

```bash
git clone https://github.com/DeekshithAI/DemoVersion.git
cd DemoVersion
```

### Step 2: Install Flutter Dependencies

```bash
flutter pub get
```

### Step 3: Set Up Backend (Python)

Open a **separate terminal** and run:

```bash
cd backend_new/sarvam-ai

# Create virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Add Sarvam API Key

Create a file named `.env` in `backend_new/sarvam-ai/` with:

```
SARVAM_API_KEY=your_actual_api_key_here
```

**Example:**

```
SARVAM_API_KEY=sk_abc123xyz789
```

⚠️ **DO NOT commit or share this file!** It's in `.gitignore` for security.

### Step 5: Start Backend

Still in the same terminal, run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:SARVAM_API_KEY found in environment
INFO:     Initialized Sarvam/OpenAI client
```

✅ **Leave this terminal running!**

### Step 6: Start Flutter App

Open a **new terminal** in the project root and run:

```bash
flutter run
```

Select your emulator or device when prompted.

✅ **Done!** The app should launch.

---

## 🔌 Test Connectivity

### From PC (while backend is running):

```bash
# Health check
curl http://127.0.0.1:8001/health

# Expected response:
{"status":"ok","sarvam_api_key_present":true}
```

### From Phone (on same Wi-Fi):

1. Find your PC's IP: `ipconfig` (look for IPv4 Address, e.g., `192.168.1.100`)
2. Open browser: `http://192.168.1.100:8001/health`
3. Should show the same JSON

---

## ❌ Common Issues & Fixes

### "ModuleNotFoundError" in backend

```bash
# Make sure you're in the venv
.\.venv\Scripts\Activate.ps1

# Reinstall
pip install -r requirements.txt
```

### "SARVAM_API_KEY not set"

- Check `.env` file exists in `backend_new/sarvam-ai/`
- Format: `SARVAM_API_KEY=sk_xxxxx` (no quotes)
- Restart backend

### Backend port 8001 already in use

```bash
# Windows: Kill the process
netsh -ano | findstr :8001
taskkill /PID <process_id> /F

# Or use port 8002:
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Flutter can't reach backend

- **Emulator**: Uses `10.0.2.2:8001` (automatic)
- **Phone**: Ensure phone & PC on same Wi-Fi
  - Edit `lib/features/chat/services/chat_service.dart`
  - Change baseUrl to: `http://<your-pc-ip>:8001`

### "flutter: command not found"

```bash
# Add Flutter to PATH
# Windows: Set PATH in System Environment Variables
# Include: C:\path\to\flutter\bin
```

---

## 📱 Running on Android Emulator vs Phone

### Emulator (easier)

- App automatically routes to `10.0.2.2:8001`
- No extra config needed
- Slower performance

### Physical Phone

1. Ensure same Wi-Fi
2. Get PC IP: `ipconfig`
3. Edit `lib/features/chat/services/chat_service.dart`:
   ```dart
   const String baseUrl = 'http://192.168.1.100:8001';  // Your PC IP
   ```
4. Rebuild: `flutter run`

---

## 🎯 Quick Reference

| Task                 | Command                                                    |
| -------------------- | ---------------------------------------------------------- |
| Clone repo           | `git clone https://github.com/DeekshithAI/DemoVersion.git` |
| Get deps             | `flutter pub get`                                          |
| Start backend        | `uvicorn main:app --host 0.0.0.0 --port 8001 --reload`     |
| Start app            | `flutter run`                                              |
| Check backend health | `curl http://127.0.0.1:8001/health`                        |
| Clean build          | `flutter clean`                                            |
| Rebuild              | `flutter pub get && flutter run`                           |

---

## 📞 Need Help?

1. Check server logs for errors (keep backend terminal visible)
2. Run `flutter doctor` to check environment
3. Check GitHub issues or contact maintainer

---

**Happy farming! 🌾**
