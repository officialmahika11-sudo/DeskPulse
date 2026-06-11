import time, psutil, requests
from plyer import notification
import winsound

LIMIT_SECONDS = 600  # 10 min break reminder
active_seconds = 0
CHECK_INTERVAL = 60  # every 1 minute

def is_user_active():
    return psutil.cpu_percent(interval=2) > 5

while True:
    if is_user_active():
        active_seconds += CHECK_INTERVAL

        # Ping the tracker every minute
        try:
            requests.post('http://127.0.0.1:5000/track', timeout=2)
        except:
            pass

    else:
        active_seconds = 0

    if active_seconds >= LIMIT_SECONDS:
        notification.notify(
            title="⏰ Break Reminder!",
            message="You've been working for 10+ minutes. Take a break!",
            timeout=10
        )
        winsound.Beep(1000, 1500)
        active_seconds = 0

    time.sleep(CHECK_INTERVAL)