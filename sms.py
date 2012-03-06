"""SMSified logic for the MTA application."""

import os
import requests as req
from three import Three

SEND = "https://api.smsified.com/v1/smsmessaging/outbound/4782467248/requests"


class AuthenticationError(Exception):
    """
    Error should be raised when the SMSified username and password
    aren't known.
    """
    pass


def auth():
    """
    Get SMSified username and password authentication from environment
    variables.
    """
    try:
        username = os.environ['SMS_USER']
        password = os.environ['SMS_PASS']
    except KeyError:
        message = "You haven't set the SMS_USER and SMS_PASS env variables."
        raise AuthenticationError(message)
    return (username, password)


def process(text):
    """Process an incoming text message."""
    address = text['senderAddress'].lstrip('tel:+')
    message = text['message']
    seeclickfix(message)
    return respond(address)


def respond(number):
    """Send an SMS text message."""
    user_pass = auth()
    number = number.replace('-', '')
    message = "Thanks for reporting your issue!"
    params = {'address': number, 'message': message}
    sms = req.post(SEND, auth=user_pass, params=params)
    return sms


def seeclickfix(message):
    """Send a new report/issue to SeeClickFix."""
    print message
