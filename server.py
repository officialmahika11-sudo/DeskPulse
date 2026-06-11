from flask import Flask, request, jsonify
import psutil, time, json, subprocess, os
from datetime import datetime, date

app = Flask(__name__)

# File to store today's usage
TRACKING_FILE = r'C:\Users\Admin\OneDrive\Desktop\n8n-assistant\screen_time.json'

def load_tracking():
    today = str(date.today())
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as f:
            data = json.load(f)
        # Reset if it's a new day
        if data.get('date') != today:
            data = {'date': today, 'minutes': 0, 'last_seen': None}
    else:
        data = {'date': today, 'minutes': 0, 'last_seen': None}
    return data

def save_tracking(data):
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f)

def update_active_time():
    data = load_tracking()
    now = time.time()
    last = data.get('last_seen')
    # If last check was less than 5 minutes ago, count it as active
    if last and (now - last) < 300:
        data['minutes'] += 1
    data['last_seen'] = now
    save_tracking(data)
    return data

def get_screen_time():
    data = load_tracking()
    minutes = data.get('minutes', 0)
    hours = minutes // 60
    mins = minutes % 60
    return jsonify({
        "type": "screen_time",
        "hours": hours,
        "minutes": mins,
        "total_minutes": minutes,
        "message": f"You have actively used your PC for {hours} hours and {mins} minutes today."
    })

def get_notifications():
    ps_cmd = """
    $apps = Get-ChildItem "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings" |
    Where-Object { $_.PSChildName -notmatch "^windows" -and $_.PSChildName -notmatch "^Microsoft" } |
    Select-Object -ExpandProperty PSChildName

    $result = @()
    foreach ($app in $apps) {
        $result += [PSCustomObject]@{
            App = $app.Split("_")[0].Split(".")[-1]
        }
    }
    $result | ConvertTo-Json
    """
    result = subprocess.run(["powershell", "-Command", ps_cmd],
                            capture_output=True, text=True)
    try:
        if not result.stdout.strip() or result.stdout.strip() == "null":
            return jsonify({
                "type": "notifications",
                "count": 0,
                "items": [],
                "message": "No pending notifications right now."
            })

        events = json.loads(result.stdout.strip())
        if isinstance(events, dict):
            events = [events]

        items = [{"app": e.get("App", "Unknown")} for e in events if e.get("App")]

        return jsonify({
            "type": "notifications",
            "count": len(items),
            "items": items,
            "message": f"You have {len(items)} apps with notifications: {', '.join([i['app'] for i in items])}"
        })
    except:
        return jsonify({
            "type": "notifications",
            "count": 0,
            "items": [],
            "message": "No notifications found or could not read them."
        })

@app.route('/assistant', methods=['POST'])
def assistant():
    data = request.get_json()
    command = data.get('command', '').lower()

    if 'screen time' in command or 'uptime' in command:
        return get_screen_time()
    elif 'notification' in command:
        return get_notifications()
    else:
        return jsonify({"type": "error", "message": "Unknown command. Try 'screen time' or 'notifications'."})

# Background tracker — called every minute by monitor.py
@app.route('/track', methods=['POST'])
def track():
    data = update_active_time()
    return jsonify({"status": "ok", "minutes": data['minutes']})

if __name__ == '__main__':
    app.run(port=5000)