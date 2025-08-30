from enum import Enum, auto
    
class MessageType(Enum):
    WARN = auto()
    BAN = auto()
    UNBAN = auto()
    MUTE = auto()
    UNMUTE = auto()
    KICK = auto()
    UNKNOWN = auto()

def get_message_type(message: str) -> MessageType:
    """
    Determines the type of message based on keywords.

    Args:
        message (str): The message string to analyze.

    Returns:
        MessageType: The type of message (MessageType.WARN, MessageType.BAN, MessageType.KICK, or MessageType.UNKNOWN).
    """
    lowered = message.lower()
    print(f"Analyzing message for type: {lowered}")
    if '#warn' in lowered:
        return MessageType.WARN
    elif '#ban' in lowered:
        return MessageType.BAN
    elif '#kick' in lowered:
        return MessageType.KICK
    elif '#unban' in lowered:
        return MessageType.UNBAN
    elif '#mute' in lowered or "#muta" in lowered:
        return MessageType.MUTE
    elif '#unmute' in lowered or "#unmuta" in lowered:
        return MessageType.UNMUTE
    else:
        return MessageType.UNKNOWN
