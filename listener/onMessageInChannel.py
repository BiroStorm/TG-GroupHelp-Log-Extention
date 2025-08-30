import logging
import time
from src.filters.typeFilter import MessageType, get_message_type
from src.database import db
import re
from datetime import datetime


async def onMessageInChannel(event):
    if db is not None:
        logging.info(f"Inserting message into DB: {event.message.text}")
        text = event.message.text
        text = text.split("\n") 
        # default log msg has at least 4 rows [Type, From, Target, Group, Reason?]
        if len(text) < 4:
            return
        typeMsg = get_message_type(text[0])
        print(f"Detected message type: {typeMsg}")
        if typeMsg == MessageType.UNKNOWN:
            return
        
        # Example: text[1] = "• Di: [Biro](http://t.me/BiroDev) [`510456529`]"
        id_match = re.search(r'\[`(\d+)`\]', text[1])

        ################## From User ####################
        link_match = re.search(r'\((http[s]?://t\.me/([^\)]+))\)', text[1])
        username = link_match.group(2) if link_match else None
        extracted_id = id_match.group(1) if id_match else None
        
        print(f"Extracted Name: {username}, Extracted ID: {extracted_id}")
        if extracted_id is None:
            logging.warning("Assertion Failed: No valid user ID found in the 'From' field.")
            print("No valid user ID found, skipping log entry.")
            return
        
        ################## Target User ####################
        # Example: text[2] = "**• A:** [.](tg://user?id=1281387868) [`1281387868`]"
        
        targets = []
        for line in text[2:]:
            if line.startswith("**• A:**"):
                target_id_match = re.search(r'\[`(\d+)`\]', line)
                if target_id_match:
                    targets.append(int(target_id_match.group(1)))
        print(f"Extracted Target IDs: {targets}")
        
        ################## Group #####################
        # Example: text[3] = "**• Gruppo:** 🦄 • 🎮 🅟🅔🅝🅣🅐🅖🅤🅢 [`-1001849609819`]"
        groups = []
        for line in text[3:]:
            if line.startswith("**• Gruppo:**"):
                group_id_match = re.search(r'\[`(-?\d+)`\]', line)
                if group_id_match:
                    groups.append(int(group_id_match.group(1)))
        print(f"Extracted Group IDs: {groups}")
        
        if len(targets) == 0 or len(groups) == 0:
            print("No targets or groups found, skipping log entry.")
            return
        
        ################## Reason ####################
        # Example: ['**• Gruppo:** 🦄 • 🎮 🅟🅔🅝🅣🅐🅖🅤🅢 [`-1001849609819`]', '**• Motivo:** Test Motivo', 'su ', 'più', 'righe, Se nel caso', 'funzionasse...', '• [👀 Vai al messaggio](http://t.me/c/1849609819/184028)', '#id5015015438']
        reason_lines = []
        motivo_found = False
        for line in text[3:]:
            if line.startswith("**• Motivo:**"):
                motivo_found = True
                reason_lines.append(line.replace("**• Motivo:**", "").strip())
            elif motivo_found:
                # Stop if we reach a line that starts with something else (e.g., a new section or link)
                if line.startswith("**• "):
                    break
                reason_lines.append(line.strip())
        reason = " ".join(reason_lines) if reason_lines else None
        print(f"Extracted Reason: {reason}")
        
        new_log_entry = {
            'type': typeMsg.name,
            'from': {"username": username, "id": int(extracted_id)},
            'targets': targets,
            'groups': groups,
            'date': datetime.now(),
        }
        if reason:
            new_log_entry['reason'] = reason
        
        print(f"Inserting log entry: {new_log_entry}")
        messages = db.messages
        messages.insert_one(new_log_entry)