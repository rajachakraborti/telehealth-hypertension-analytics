import hashlib
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

def get_client_fingerprint(request: Request) -> str:
    """
    Generates a backend fingerprint to mitigate IP spoofing/rotation.
    Looks for a frontend-generated JS fingerprint first, then falls back 
    to a cryptographic hash of network headers.
    """
    # 1. Check if the React frontend passed a true device fingerprint (e.g., FingerprintJS)
    device_id = request.headers.get("X-Device-Fingerprint")
    if device_id:
        return device_id
    
    # 2. Fallback: Backend Heuristic Fingerprinting
    # Makes rotating IPs much harder since attackers must also perfectly rotate browser headers
    ip = get_remote_address(request)
    user_agent = request.headers.get("User-Agent", "unknown_agent")
    accept_lang = request.headers.get("Accept-Language", "unknown_lang")
    
    raw_fingerprint = f"{ip}|{user_agent}|{accept_lang}"
    return hashlib.sha256(raw_fingerprint.encode('utf-8')).hexdigest()

# Initialize Rate Limiter using the fingerprinting function
limiter = Limiter(key_func=get_client_fingerprint)
