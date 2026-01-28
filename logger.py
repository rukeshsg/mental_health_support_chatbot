from datetime import datetime, timedelta
import os

LOG_FILE = "intent_log.txt"
DAYS_LIMIT = 16


# ✅ Save intent with timestamp
def save_intent(intent):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | {intent}\n"

    # Clean old logs first
    clean_old_logs()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


# ✅ Remove logs older than 16 days
def clean_old_logs():
    if not os.path.exists(LOG_FILE):
        return

    valid_lines = []
    cutoff_date = datetime.now() - timedelta(days=DAYS_LIMIT)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        try:
            timestamp_str, intent = line.strip().split(" | ")
            log_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            if log_time >= cutoff_date:
                valid_lines.append(line)
        except:
            continue

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(valid_lines)


# ✅ Get recent intents for pattern awareness
def get_recent_intents():
    if not os.path.exists(LOG_FILE):
        return []

    clean_old_logs()

    intents = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            try:
                _, intent = line.strip().split(" | ")
                intents.append(intent)
            except:
                continue

    return intents

