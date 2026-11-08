import sys
import time
from datetime import datetime, timedelta

import pyautogui

# Usage: python send_continue.py 14:30
hour, minute = map(int, sys.argv[1].split(":"))

now = datetime.now()
target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
if target <= now:
    target += timedelta(days=1)

print(f"Sending 'continue' at {target:%Y-%m-%d %H:%M}. Keep the agent window focused. Ctrl+C cancels.")

time.sleep((target - datetime.now()).total_seconds())

pyautogui.write("continue", interval=0.05)
pyautogui.press("enter")
pyautogui.press("enter")
print("Sent.")