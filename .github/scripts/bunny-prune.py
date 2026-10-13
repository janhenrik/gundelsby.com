"""Delete files from Bunny storage that are not in the freshly built _site.

Runs after the upload step, so the site is never missing files mid-deploy.
Set BUNNY_PRUNE_MODE=delete to delete; any other value only lists what
would be deleted.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

ZONE = "gundelsby-com"
BASE = f"https://storage.bunnycdn.com/{ZONE}/"
KEY = os.environ["BUNNY_STORAGE_PASSWORD"]
MODE = os.environ.get("BUNNY_PRUNE_MODE", "dry-run")
SITE = "_site"
MIN_LOCAL_FILES = 20


def request(method, path):
    url = BASE + urllib.parse.quote(path)
    req = urllib.request.Request(url, method=method, headers={"AccessKey": KEY, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def remote_files(prefix=""):
    for entry in json.loads(request("GET", prefix)):
        name = prefix + entry["ObjectName"]
        if entry["IsDirectory"]:
            yield from remote_files(name + "/")
        else:
            yield name


local = {
    os.path.relpath(os.path.join(root, f), SITE).replace(os.sep, "/")
    for root, _, files in os.walk(SITE)
    for f in files
}
if len(local) < MIN_LOCAL_FILES:
    sys.exit(f"Only {len(local)} files in {SITE}; refusing to prune")

remote = set(remote_files())
stale = sorted(remote - local)
print(f"{len(local)} local files, {len(remote)} remote files, {len(stale)} stale")

for path in stale:
    if MODE == "delete":
        request("DELETE", path)
        print(f"Deleted: {path}")
    else:
        print(f"Would delete: {path}")
