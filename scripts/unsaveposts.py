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
'''

import praw

try:
    r= praw.Reddit(
        client_id="CLIENTID",
        client_secret="CLIENTSECRET",
        password="USERPASSWORD",
        user_agent="Unsave Posts",
        username="USERNAME",
    )

    with open("successfulids", "r") as f:
        for item in f:
            r.submission(id = item.strip()).unsave()

except:
    print("Something went wrong. Did you install PRAW? Did you change the user login fields?")


else:
    print("Done! Thanks for playing!")

