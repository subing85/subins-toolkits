# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, scripts license source code.


import json
import os
import hmac
import hashlib
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

SUBSCRIPTION_FILE = "subscription.enc"
KEY_FILE = "secret.key"
HMAC_SECRET = b"super-secret-hmac-key"  # Use a strong, unique key for HMAC


# Generate and store encryption key if it doesn't exist
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()

fernet = Fernet(key)


def hmac_hash(data):
    """Generate HMAC hash to verify data integrity."""
    return hmac.new(HMAC_SECRET, data.encode(), hashlib.sha256).hexdigest()


def initialize_subscription():
    """Sets up a new 1-year encrypted subscription."""
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)
    subscription_data = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hmac": "",  # Placeholder for hash
    }

    # Calculate HMAC hash and add to data
    subscription_data["hmac"] = hmac_hash(json.dumps(subscription_data))

    # Encrypt and save data
    encrypted_data = fernet.encrypt(json.dumps(subscription_data).encode())
    with open(SUBSCRIPTION_FILE, "wb") as f:
        f.write(encrypted_data)

    print("Subscription initialized and encrypted.")


def check_subscription():
    """Decrypts and verifies the subscription data."""
    if not os.path.exists(SUBSCRIPTION_FILE):
        print("No subscription found. Please initialize a subscription.")
        return False

    # Load and decrypt the subscription data
    with open(SUBSCRIPTION_FILE, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    subscription_data = json.loads(decrypted_data)

    # Verify integrity with HMAC
    expected_hmac = subscription_data.pop("hmac")
    if hmac_hash(json.dumps(subscription_data)) != expected_hmac:
        print("Subscription data integrity check failed.")
        return False

    end_date = datetime.strptime(subscription_data["end_date"], "%Y-%m-%d")
    if datetime.now() > end_date:
        print("Subscription expired on:", end_date.strftime("%Y-%m-%d"))
        return False

    print("Subscription is active. Expires on:", end_date.strftime("%Y-%m-%d"))
    return True


if __name__ == "__main__":
    # Uncomment the line below to initialize a new subscription (only do this once)
    # initialize_subscription()

    # Check subscription status each time the app starts
    if check_subscription():
        print("Welcome to the app! Subscription is valid.")
        # Proceed with the rest of your application
    else:
        print("Please renew your subscription to continue.")

if __name__ == "__main__":
    pass
