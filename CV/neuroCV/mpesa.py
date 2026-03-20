import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime
import base64

def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return r.json()['access_token']

def send_stk_push(phone_number, amount):
    access_token = get_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    # M-Pesa specific credentials
    business_short_code = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Generate Password: base64(shortcode + passkey + timestamp)
    password_str = business_short_code + passkey + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number, # The phone sending money
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/mpesa/callback/", # Must be a public URL
        "AccountReference": "NeuroCV",
        "TransactionDesc": "CV Generation Fee"
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()