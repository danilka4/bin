#!/home/lizzy/Documents/venv/bin/python3
import sys
import os
from anki.collection import Collection, ImportCsvRequest, Delimiter
from anki.syncserver import run_sync_server
from anki.sync import SyncAuth
import tempfile
import csv

title = ""
content = ""
lc = 0
for line in sys.stdin:
    lc += 1
    line = line.strip()
    if line and line[0] == "#":
        title = line[2:]
    elif line:
        if content:
            content += f"\n{line}"
        else:
            content = line
if not title:
    print("Title non-existent")
elif lc > 30:
    print("Card too large")
    exit()
try:
    col = Collection("/home/lizzy/.local/share/Anki2/User 1/collection.anki2")
except Exception as e:
    col = Collection("/home/lizzy/.var/app/net.ankiweb.Anki/data/Anki2/User 1/collection.anki2")
deck = col.decks.by_name("vault")

with tempfile.NamedTemporaryFile(mode='w', delete=False) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["title", "content"])
    writer.writeheader()
    writer.writerow({"title": title, "content": content})
fname=csvfile.name
metadata = col.get_csv_metadata(fname, delimiter=Delimiter.COMMA)
request = ImportCsvRequest(path=fname, metadata=metadata)
# print(f"metadata: {metadata}")
# print(f"request: {request}")
response = col.import_csv(request)
# col.close_for_full_sync()
# login = col.sync_login(username="danielpalamarchuk@yahoo.com", password="Danilka123_", endpoint=None)
# col.sync_collection(login, True)
# os.environ["SYNC_USER1"] = "danielpalamarchuk@yahoo.com:Danilka123_"
# run_sync_server()

# print(deck)
# did = col.decks.id("vault")
# if not did:
#     exit()
# col.decks.select(did)
# card = Card(col)
# new_note = col.new_note({"front": 'foo', "back": "bar", "id": "basic"})
# col.add_note(new_note, did)


# model = mw.col.models.by_name("Basic")
# new_note = mw.col.new_note(model)

# new_note["fieldNameA"] = title
# new_note["fieldNameB"] = content
# did = mw.col.decks.id("vault")
# mw.col.add_note(new_note, did)
