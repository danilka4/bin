#!/home/lizzy/Documents/venv/bin/python3

import openreview
import sys
from dotenv import load_dotenv
import os


def get_paper_bibtex(forum_id, username, password):
    # Try API V2
    try:
        client_v2 = openreview.api.OpenReviewClient(
         baseurl='https://api2.openreview.net',
         username=username,
         password=password
        )
        # get_notes returns a list in V2
        notes = client_v2.get_notes(id=forum_id)
        if notes:
            # V2 structure: content['field']['value']
            bib = notes[0].content.get('_bibtex', {}).get('value')
            if bib:
                return bib
    except Exception:
        pass

    # Fallback to API V1
    try:
        client_v1 = openreview.Client(
            baseurl='https://api.openreview.net',
            username=username,
            password=password
        )
        # get_note returns a single note or raises error in V1
        note = client_v1.get_note(forum_id)
        # V1 structure: content['field']
        bib = note.content.get('_bibtex')
        if bib:
            return bib
    except Exception:
        pass

    return f"Error: Paper {forum_id} not found in V1 or V2 APIs."

# Usage
# bib = get_paper_bibtex('YOUR_ID_HERE', 'user@email.com', 'password123')
# print(bib)

load_dotenv()
username = os.getenv("OPENREVIEW_USER")
password = os.getenv("OPENREVIEW_PASSWORD")

client = openreview.Client(
    baseurl='https://api.openreview.net',
    username=username,
    password=password
)



forum_id = sys.argv[1]

b = get_paper_bibtex(forum_id, username, password)

b = b.replace('\n', '', 1).replace('\n', '\n    ').replace('    }', '}')

print(b)
