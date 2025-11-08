#!/usr/bin/env python3
"""
Script to automatically update papers.md from Google Scholar profile.
"""

import os
import re
from scholarly import scholarly
import time

# Configuration
SCHOLAR_ID = "4bw3LsEAAAAJ"
# Get the repository root (parent of scripts directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(REPO_ROOT, "papers.md")

def format_authors(authors):
    """Format author names."""
    # scholarly returns authors as a string, not a list
    if isinstance(authors, str):
        return authors
    elif isinstance(authors, list):
        return ", ".join(authors)
    return ""

def is_valid_publication(pub):
    """Check if publication data is valid and not malformed."""
    title = pub['bib'].get('title', '')

    # Skip if no title
    if not title or title == 'No title':
        return False

    # Skip if title is suspiciously long (likely malformed data)
    if len(title) > 200:
        return False

    # Skip if title looks like it contains author lists or indexes
    # (e.g., contains ", and" patterns or lots of numbers)
    if ', and ' in title.lower() and len(title) > 100:
        return False

    return True

def format_paper(pub):
    """Format a publication entry for papers.md."""
    title = pub['bib'].get('title', 'No title')
    authors = pub['bib'].get('author', '')
    venue = pub['bib'].get('venue', '')
    year = pub['bib'].get('pub_year', '')
    citation = pub['bib'].get('citation', '')
    url = pub.get('pub_url', '')

    # Build citation info
    citation_parts = []
    if venue:
        citation_parts.append(str(venue))
    if citation:
        citation_parts.append(str(citation))
    if year:
        citation_parts.append(str(year))

    citation_text = ", ".join(filter(None, citation_parts))

    # Format the entry
    if url:
        entry = f"- [{title}]({url})  \n"
    else:
        entry = f"- {title}  \n"

    if authors:
        entry += f"  {format_authors(authors)}  \n"

    if citation_text:
        entry += f"  {citation_text}\n"

    return entry

def fetch_publications(author_id):
    """Fetch publications from Google Scholar."""
    print(f"Fetching publications for author ID: {author_id}")

    try:
        # Retrieve author info
        author = scholarly.search_author_id(author_id)
        author = scholarly.fill(author, sections=['publications'])

        publications = []
        for pub in author['publications']:
            try:
                # Fill publication details
                pub_filled = scholarly.fill(pub)
                publications.append(pub_filled)
                time.sleep(1)  # Be respectful to Google Scholar
            except Exception as e:
                print(f"Warning: Could not fetch details for publication: {e}")
                continue

        # Sort by year (descending)
        publications.sort(
            key=lambda x: int(x['bib'].get('pub_year', '0') or '0'),
            reverse=True
        )

        return publications

    except Exception as e:
        print(f"Error fetching publications: {e}")
        return []

def update_papers_md(publications):
    """Update papers.md file with fetched publications."""
    header = """---
layout: page
title: papers
---
## Papers

[Also see Google Scholar](https://scholar.google.com/citations?user=4bw3LsEAAAAJ)

"""

    content = header

    valid_count = 0
    skipped_count = 0

    for pub in publications:
        if is_valid_publication(pub):
            content += format_paper(pub) + "\n"
            valid_count += 1
        else:
            skipped_count += 1
            print(f"Skipping malformed entry: {pub['bib'].get('title', 'No title')[:80]}...")

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully updated {OUTPUT_FILE} with {valid_count} publications")
    if skipped_count > 0:
        print(f"Skipped {skipped_count} malformed entries")

def main():
    """Main function."""
    print("Starting Google Scholar update...")
    publications = fetch_publications(SCHOLAR_ID)

    if publications:
        update_papers_md(publications)
        print("Update complete!")
    else:
        print("No publications found or error occurred")
        exit(1)

if __name__ == "__main__":
    main()
