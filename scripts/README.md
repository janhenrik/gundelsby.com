# Papers Auto-Update Script

This directory contains automation scripts for maintaining the papers.md file.

## Overview

The `update_papers.py` script automatically fetches your publications from Google Scholar and updates the `papers.md` file in the repository root.

## How It Works

1. **Scheduled Execution**: A GitHub Actions workflow runs every Monday at 9:00 AM UTC
2. **Fetch Publications**: The script queries your Google Scholar profile (ID: 4bw3LsEAAAAJ)
3. **Format & Update**: Publications are formatted and written to papers.md
4. **Auto-Commit**: If changes are detected, they're automatically committed to the main branch

## Manual Usage

To run the script manually:

```bash
cd scripts
pip install -r requirements.txt
python update_papers.py
```

## GitHub Actions Workflow

The workflow is defined in `.github/workflows/update-papers.yml` and can be:
- **Automatically triggered**: Every Monday at 9:00 AM UTC
- **Manually triggered**: Via GitHub Actions UI (workflow_dispatch)

## Configuration

To change the Scholar ID or output file, edit these variables in `update_papers.py`:

```python
SCHOLAR_ID = "4bw3LsEAAAAJ"  # Your Google Scholar author ID
OUTPUT_FILE = "papers.md"     # Output file path
```

## Requirements

- Python 3.11+
- scholarly library (see requirements.txt)

## Troubleshooting

If the script fails:
1. Check GitHub Actions logs for error messages
2. Google Scholar may rate-limit requests - the script includes delays
3. Verify the Scholar ID is correct in the script configuration
