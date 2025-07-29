import re
from datetime import datetime
from typing import List, Dict

def parse_whatsapp_txt(file_path: str) -> List[Dict]:
    pattern = re.compile(r"^(\d{2}/\d{2}/\d{2})[ ,]+(\d{2}[:.]\d{2}) - ([^:]+): (.+)$")
    parsed = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            match = pattern.match(line)
            if match:
                date, time, sender, message = match.groups()
                # Normalize time separator to ':'
                time = time.replace('.', ':')
                timestamp = f"20{date[-2:]}-{date[3:5]}-{date[0:2]} {time}"
                parsed.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "message": message
                })
    return parsed

# Example usage:
# result = parse_whatsapp_txt('chat.txt')
# print(result)
