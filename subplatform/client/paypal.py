import requests
import json
from .models import Subscription
from decouple import config


def get_access_token():
    data = {'grant_type': 'client_credentials'}

    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}

    clientID = config('PAYPAL_CLIENT_ID')
    secretID = config('PAYPAL_SECRET_ID')

    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'

    r = requests.post(url, auth=(clientID, secretID), headers=headers, data=data).json()

    access_token = r['access_token']

    return access_token


def cancel_subscription_paypal(access_token, subID):
    bearer_token = 'Bearer ' + access_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/cancel'

    r = requests.post(url, headers=headers)

    print(r.status_code)
