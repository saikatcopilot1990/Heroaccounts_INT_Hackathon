import sys
import os

# Add the backend directory to sys.path to allow importing app modules
sys.path.append(os.path.abspath("e:/intallprojects/heroaccounts/backend"))

try:
    from app.config import get_settings
    settings = get_settings()
    
    print(f"SMTP Host: {settings.smtp_host}")
    print(f"SMTP Port: {settings.smtp_port}")
    print(f"SMTP User: {settings.smtp_user}")
    # Mask password for security in logs
    masked_pass = settings.smtp_pass[:4] + "*" * (len(settings.smtp_pass) - 4) if settings.smtp_pass else "None"
    print(f"SMTP Pass: {masked_pass}")
    
    if settings.smtp_host == "smtp.gmail.com" and settings.smtp_user == "vikas@intglobal.com":
        print("SUCCESS: SMTP configuration verified.")
    else:
        print("FAILURE: SMTP configuration mismatch.")
        
except Exception as e:
    print(f"ERROR: Failed to verify configuration: {e}")
