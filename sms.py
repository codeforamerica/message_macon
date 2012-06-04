"""SMSified logic for the MTA application."""

import os
import requests as req
import three


if 'PRODUCTION_ENV' in os.environ:
    # Then we'll use the actual SeeClickFix endpoint.
    macon = three.city('macon')
else:
    # Otherwise, it's testing.
    macon = three.dev('http://seeclicktest.com/open311/v2')


class AddressError(Exception):
    """Can't parse an address from a text message."""
    pass


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
    number = text['senderAddress'].lstrip('tel:+')
    message = text['message']
    address, info = find_address(message)
    post = macon.post('0', address=address, description=info, phone=number)
    # Log the POST request to SeeClickFix.
    print post
    return respond(number)


def find_address(message):
    """Parse the address from a text message."""
    data = message.split('. ')
    length = len(data)
    if length == 1:
        raise AddressError("Can't process the address from your text message.")
    elif length == 2:
        description = data[1]
    else:
        description = '. '.join(data[1:])
    street = data[0]
    address = street + ' Macon, GA'
    return address, description


def respond(number):
    """Send an SMS text message."""
    user_pass = auth()
    number = number.replace('-', '')
    message = "Thanks for reporting your issue!"
    params = {'address': number, 'message': message}
    send = "https://api.smsified.com/v1/smsmessaging/outbound/4782467248/requests"
    sms = req.post(send, auth=user_pass, params=params)
    return sms
