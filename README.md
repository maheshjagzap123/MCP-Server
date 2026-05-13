# GitHub MCP Server

A simple MCP server that exposes GitHub actions as tools: create branch, push file, open PR, and merge PR.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your GitHub token
```

## Run

```bash
python server.py
```

## Tools

| Tool | Description |
|---|---|
| `create_branch` | Create a new branch from an existing one |
| `push_file` | Create or update a file (commit & push) |
| `create_pull_request` | Open a pull request |
| `merge_pull_request` | Merge an open pull request by PR number |

## Example Usage

```python
# Create a branch
create_branch("owner/repo", "feature/my-branch", from_branch="main")

# Push a file
push_file("owner/repo", "feature/my-branch", "hello.txt", "Hello World!", "add hello.txt")

# Open a PR
create_pull_request("owner/repo", "My PR", head="feature/my-branch", base="main")

# Merge PR #1
merge_pull_request("owner/repo", 1)
```

## Requirements

- Python 3.10+
- GitHub Personal Access Token with `repo` scope
