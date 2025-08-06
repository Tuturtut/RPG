_logs = []

def log(message):
    if isinstance(message, list):
        message = " | ".join(message)

    if isinstance(message, dict) or isinstance(message, tuple):
        message = str(message)

    global _logs
    _logs.append(message)
    if len(_logs) > 100:
        _logs.pop(0)

def get_logs(n=10):
    return _logs[-n:]

def clear_logs():    
    _logs.clear()
