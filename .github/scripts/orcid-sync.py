"""Add publications from ORCID that are missing in _bibliography/papers.bib.

Compares DOIs on the public ORCID record with the DOIs already in the
bibliography. For each new DOI, BibTeX is fetched from doi.org (Crossref)
and inserted at the top of the file. Existing entries are never modified,
so hand-curated fields (abbr, author spelling, venue names) are preserved.

Writes a Markdown summary to $SUMMARY_FILE (default: orcid-sync-summary.md)
for use as a pull request body. Usage: orcid-sync.py [path/to/papers.bib]
"""
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

ORCID = "0000-0001-5275-6553"
BIB = sys.argv[1] if len(sys.argv) > 1 else "_bibliography/papers.bib"
SUMMARY_FILE = os.environ.get("SUMMARY_FILE", "orcid-sync-summary.md")
KEEP_FIELDS = ["title", "author", "booktitle", "journal", "series", "volume",
               "number", "pages", "publisher", "year", "doi"]
USER_AGENT = "gundelsby.com-orcid-sync (https://gundelsby.com)"


def fetch(url, accept):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def orcid_works():
    data = json.loads(fetch(f"https://pub.orcid.org/v3.0/{ORCID}/works", "application/json"))
    works = {}
    for group in data.get("group", []):
        summary = group["work-summary"][0]
        title = summary["title"]["title"]["value"]
        for ext in group.get("external-ids", {}).get("external-id", []):
            if ext["external-id-type"] == "doi":
                works[ext["external-id-value"].lower()] = title
    return works


def bib_dois(text):
    return {m.lower() for m in re.findall(r"^\s*doi\s*=\s*[{\"]([^}\"]+)", text, re.M | re.I)}


def bib_keys(text):
    return set(re.findall(r"^@\w+\{([^,\s]+),", text, re.M))


def parse_bibtex(raw):
    """Parse a single Crossref BibTeX entry into (type, {field: value})."""
    head = re.match(r"\s*@(\w+)\{[^,]*,", raw)
    if not head:
        raise ValueError(f"Unexpected BibTeX: {raw[:200]}")
    entry_type, pos, fields = head.group(1).lower(), head.end(), {}
    while True:
        m = re.compile(r"\s*(\w+)\s*=\s*").match(raw, pos)
        if not m:
            break
        name, pos = m.group(1).lower(), m.end()
        if raw[pos] == "{":
            depth, start = 0, pos
            while True:
                depth += {"{": 1, "}": -1}.get(raw[pos], 0)
                pos += 1
                if depth == 0:
                    break
            value = raw[start + 1:pos - 1]
        else:
            m = re.compile(r"[^,}]+").match(raw, pos)
            value, pos = m.group(0).strip(), m.end()
        fields[name] = value
        m = re.compile(r"\s*,?").match(raw, pos)
        pos = m.end()
    return entry_type, fields


def ascii_slug(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", value.lower())


def make_key(fields, taken):
    first_author = fields.get("author", "anon").split(" and ")[0]
    last = first_author.split(",")[0] if "," in first_author else first_author.split()[-1]
    words = [w for w in re.findall(r"[A-Za-z]+", fields.get("title", "")) if len(w) > 3]
    base = f"{ascii_slug(last)}{fields.get('year', '')}{ascii_slug(words[0]) if words else ''}"
    key, n = base, 2
    while key in taken:
        key, n = f"{base}{n}", n + 1
    return key


def format_entry(entry_type, key, fields):
    names = [f for f in KEEP_FIELDS if fields.get(f)]
    width = max(len(n) for n in names)
    lines = [f"  {n.ljust(width)} = {{{fields[n]}}}" for n in names]
    return f"@{entry_type}{{{key},\n" + ",\n".join(lines) + "\n}\n"


def insert_entries(text, entries):
    """Insert entries before the first existing entry (newest first)."""
    m = re.search(r"^@", text, re.M)
    pos = m.start() if m else len(text)
    return text[:pos] + "\n".join(entries) + "\n" + text[pos:]


def main():
    with open(BIB, encoding="utf-8") as f:
        text = f.read()

    works = orcid_works()
    existing = bib_dois(text)
    new = sorted(set(works) - existing)
    only_local = sorted(existing - set(works))

    taken, added, failed = bib_keys(text), [], []
    for doi in new:
        try:
            raw = fetch(f"https://doi.org/{urllib.parse.quote(doi)}", "application/x-bibtex")
            entry_type, fields = parse_bibtex(raw)
            fields["doi"] = doi
            if entry_type in ("inbook", "incollection") and fields.get("booktitle"):
                entry_type = "inproceedings"  # Crossref's type for Springer proceedings chapters
            key = make_key(fields, taken)
            taken.add(key)
            added.append((key, doi, fields, format_entry(entry_type, key, fields)))
        except Exception as error:  # keep going; report in summary
            failed.append((doi, works[doi], str(error)))

    if added:
        added.sort(key=lambda a: a[2].get("year", ""), reverse=True)
        text = insert_entries(text, [a[3] for a in added])
        with open(BIB, "w", encoding="utf-8") as f:
            f.write(text)

    summary = [f"Synced against ORCID [{ORCID}](https://orcid.org/{ORCID}).", ""]
    if added:
        summary += ["### Added", ""]
        summary += [f"- `{k}`: {f.get('title')} ({f.get('year')}) — https://doi.org/{d}" for k, d, f, _ in added]
        summary += ["", "**Before merging:** add `abbr` (venue badge), check the year "
                    "(Crossref often uses the volume's issue year), and tidy author names "
                    "and venue to match the other entries.", ""]
    if failed:
        summary += ["### Could not fetch BibTeX", ""]
        summary += [f"- {t} — `{d}`: {e}" for d, t, e in failed] + [""]
    if only_local:
        summary += ["### In papers.bib but not on ORCID", ""]
        summary += [f"- `{d}`" for d in only_local] + [""]
    if not (added or failed or only_local):
        summary.append("Everything is in sync.")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(summary) + "\n")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
