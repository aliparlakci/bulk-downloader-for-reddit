#! /usr/bin/env python3.9
'''
This script takes a list of submission IDs from a file named "successfulids" created with the 
"extract_successful_ids.sh" script and unsaves them from your account. To make it work you must
fill in the username and password fields below. Make sure you keep the quotes around the fields.
You'll need to make a "user script" in your reddit profile to run this.
Go to https://old.reddit.com/prefs/apps/
Click on "Develop an app" at the bottom.
Make sure you select a "script" not a "web app."
Give it a random name. Doesn't matter.
You need to fill in the "Redirect URI" field with something so go ahead and put 127.0.0.0 in there.
Save it.
The client ID is the 14 character string under the name you gave your script.
It'll look like a bunch of random characters like this: pspYLwDoci9z_A
The client secret is the longer string next to "secret".
Replace those two fields below. Again keep the quotes around the fields.
Create a .env file on the same directory of this script and add the following lines:

REDDIT_CLIENTID='<Reddit Client ID>'
REDDIT_SECRET='<Reddit Client Secret>'
REDDIT_USERAGENT='Unsave Posts'
REDDIT_USERNAME='<Your Reddit Username>'
REDDIT_PASSWORD='<Your Reddit Password>'
REDDIT_OTP='<Your Reddit OTP Key>'
REDDIT_MFA='1' <if you use 2FA on Reddit; otherwise, '0'>

Install with pip the following packages: dotenv pyotp
'''

import praw
import os
from dotenv import load_dotenv
import prawcore
import pyotp
import sys

try:

    load_dotenv()
    reddit_clientid = os.getenv('REDDIT_CLIENTID')
    reddit_clientsecret = os.getenv('REDDIT_SECRET')
    reddit_useragent = os.getenv('REDDIT_USERAGENT')
    reddit_username = os.getenv('REDDIT_USERNAME')
    reddit_password = os.getenv('REDDIT_PASSWORD')

    if os.getenv('REDDIT_MFA') == '1':

        reddit_otp = os.getenv('REDDIT_OTP')

        totp = pyotp.TOTP(reddit_otp)

        r = praw.Reddit(
            client_id=reddit_clientid,
            client_secret=reddit_clientsecret,
            user_agent=reddit_useragent,
            username=reddit_username,
            password="{}:{}".format(reddit_password, totp.now()))

    else:

        r= praw.Reddit(
            client_id=reddit_clientid,
            client_secret=reddit_clientsecret,
            password=reddit_password,
            user_agent=reddit_useragent,
            username=reddit_username
        )

except:
    print("Failed during authentication. Check .env configuration data")

else:

    print("Authenticated as u/" + str(r.user.me()))
    r.read_only = False

    with open("successfulids", "r") as f:
        for item in f:
            r.submission(id = item.strip()).unsave()

    print("Done! Thanks for playing!")

