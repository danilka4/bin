#!/home/lizzy/Documents/venv/bin/python3

import openreview
import sys
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("OPENREVIEW_USER")
password = os.getenv("OPENREVIEW_PASSWORD")

client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username=username,
    password=password
)

forum_id = sys.argv[1]

note = client.get_note(forum_id)

j = note.to_json()
b = j['content']['_bibtex']['value']
b = b.replace('\n', '', 1).replace('\n', '\n    ').replace('    }', '}')

print(b)
