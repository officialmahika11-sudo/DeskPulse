import sys, json, psutil, subprocess, time

def get_screen_time():
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    return json.dumps({
        "type": "screen_time",
        "hours": hours,
        "minutes": minutes,
        "message": f"Your PC has been on for {hours} hours and {minutes} minutes."
    }, indent=2)

def get_notifications():
    ps_cmd = """
    Get-WinEvent -LogName 'Microsoft-Windows-PushNotification-Platform/Operational' `
    -MaxEvents 5 | Select-Object TimeCreated, Message | ConvertTo-Json
    """
    result = subprocess.run(["powershell", "-Command", ps_cmd],
                            capture_output=True, text=True)

    if not result.stdout.strip():
        return json.dumps({
            "type": "notifications",
            "count": 0,
            "items": [],
            "message": "No recent notifications found."
        }, indent=2)

    try:
        events = json.loads(result.stdout.strip())
        if isinstance(events, dict):
            events = [events]

        items = []
        for e in events:
            msg = e.get("Message", "")
            app = "System"
            if "AppUserModelId]" in msg:
                parts = msg.split("[AppUserModelId]")
                app = parts[0].strip().split()[-1].split("!")[-1]
            short_msg = msg.split(".")[0] + "."
            items.append({
                "app": app,
                "message": short_msg
            })

        return json.dumps({
            "type": "notifications",
            "count": len(items),
            "items": items,
            "message": f"You have {len(items)} recent notifications."
        }, indent=2)

    except:
        return json.dumps({
            "type": "error",
            "message": "Could not parse notifications."
        }, indent=2)

def unknown_command():
    return json.dumps({
        "type": "error",
        "message": "Unknown command. Try 'screen time' or 'notifications'."
    }, indent=2)

command = sys.argv[1].lower() if len(sys.argv) > 1 else ""

if "screen time" in command or "uptime" in command:
    print(get_screen_time())
elif "notification" in command:
    print(get_notifications())
else:
    print(unknown_command())