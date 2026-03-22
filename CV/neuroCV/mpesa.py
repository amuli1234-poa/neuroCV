import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

# SANDBOX CREDENTIALS (Use these until Daraja opens)
BUSINESS_SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9cdcf1d1541bf246b4c3f55145627216a8073c8b40971c0b363307"
CONSUMER_KEY = "YOUR_SANDBOX_KEY" # Get this when portal opens
CONSUMER_SECRET = "YOUR_SANDBOX_SECRET"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json()['access_token']

def trigger_stk_push(phone_number, amount, resume_id):
    access_token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((BUSINESS_SHORTCODE + PASSKEY + timestamp).encode()).decode()
    
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number, # e.g., 2547XXXXXXXX
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": f"https://your-domain.com/mpesa-callback/{resume_id}/",
        "AccountReference": f"CV-{resume_id}",
        "TransactionDesc": "Payment for Professional CV"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()