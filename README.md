# Profile-touch
Naukari auto update


# profile-touch

Keep a Naukri profile marked as recently updated.

A Windows laptop opens real Google Chrome, edits one character in **Resume headline**, clicks Save, and exits. Task Scheduler runs it four times a day.

This is a personal visibility script. It is not an official Naukri tool. Use it only on your own account.

## What you need

- Windows
- Git Bash
- Google Chrome
- Windows Task Scheduler (already installed)
- Python 3.12


In Git Bash:
1. Check gitbash
```bash
python --version
If Windows Store opens, Python is not installed. Go to step 2.

**2. Install Python**
Bashwinget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
Close Git Bash. Open a new window.
Bashpython --version
You want Python 3.12.x.
If Store still opens:
Settings → Apps → Advanced app settings → App execution aliases
Turn off python.exe and python3.exe.

**3. Project folder**
Bashmkdir -p "$HOME/profile-touch"
cd "$HOME/profile-touch"
python -m venv venv
source venv/Scripts/activate
Layout:
textC:\Users\YOUR_ID\profile-touch\
  venv\
  update_profile.py
  .env
  chrome-profile\     created on first run
  screenshots\        created on first run

**4. Libraries**
Stay inside the venv ((venv) in the prompt):
Bashpip install playwright python-dotenv
pip show playwright
Expect Playwright 1.62 or similar.
This can fail. Skip it if you see a certificate error:
Bashplaywright install chromium
The script uses the Chrome already installed on the laptop.

**5. Secrets**
Bashcd "$HOME/profile-touch"
notepad .env
textPORTAL_EMAIL=your_email
PORTAL_PASSWORD=your_password
Save.
Never commit .env. Never paste it on YouTube, Confluence, or chat.

**6. Script**
Bashnotepad update_profile.py
Paste update_profile.py from this repo.
Default profile page:
texthttps://www.naukri.com/mnjuser/profile
Change it on the laptop if your page is different.

**7. First run**
Watch the Chrome window. Do not schedule yet.
Bashcd "$HOME/profile-touch"
source venv/Scripts/activate
python update_profile.py

Chrome opens.
You complete login and OTP yourself.
Terminal should print SAVED: True.
Open screenshots\success.png.
Check the last-updated time on Naukri.

Run it a second time. You should stay logged in. No OTP.
If the second run still asks for OTP, chrome-profile did not persist. Fix that before scheduling.

**8. Schedule**
Task Scheduler → Create Task → name: VisibilityKeeper
General

Run only when user is logged on
Highest privileges: off

**Triggers**

Daily 08:00
Daily 10:00
Daily 16:00
Daily 17:00

**Actions**

Program: C:\Users\YOUR_ID\profile-touch\venv\Scripts\python.exe
Arguments: C:\Users\YOUR_ID\profile-touch\update_profile.py
Start in: C:\Users\YOUR_ID\profile-touch

Replace YOUR_ID with your Windows username.

**Conditions**
Untick “Start only if on AC power”

Do not add --headless.
OK → right-click the task → Run once.
After that it starts on its own.
Laptop off = that time is skipped.
How the edit works
The script finds the Resume headline card, opens edit, then either removes a trailing . or adds one. Then it clicks Save. One character is enough for Naukri to refresh the timestamp.
Do not upload

.env
chrome-profile\ (logged-in browser)
screenshots that show your name or email

**License**
Use at your own risk. Naukri can change the page and break the selectors at any time.
