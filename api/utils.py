import uuid


def short_uuid():
    """Returns a short UUID - Used as OTP"""
    return str(uuid.uuid4())[:6]
